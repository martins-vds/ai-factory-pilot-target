import json
import math
import os
import random
import re
from datetime import date, datetime
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import parse_qs, urljoin, urlsplit

import pytest
import requests


HERE = Path(__file__).resolve().parent
GOLDEN_DIR = HERE / "golden"
BASE_URL = os.environ.get(
    "LEGACY_BASE_URL", "http://localhost:8080/cargo-tracker"
).rstrip("/")
RECORD_GOLDENS = os.environ.get("AFS_RECORD_TRACK_CARGO_GOLDEN") == "1"

CASES = {
    "abc123": {
        "input": "ABC123",
        "predicted": "Found, in port Helsinki; last known location New York; "
        "ETA today+14; next load is New York to Dallas; all three events expected.",
    },
    "jkl567": {
        "input": "JKL567",
        "predicted": "Found, onboard voyage 0100S; misdirected after the last load; "
        "no ETA or next activity; the final handling event is unexpected.",
    },
    "def789": {
        "input": "DEF789",
        "predicted": "Found with no itinerary or history; not received; ETA unknown; "
        "no next activity; map status is NOT_ROUTED.",
    },
    "mno456": {
        "input": "MNO456",
        "predicted": "Found and claimed; ETA unknown; no next activity; "
        "the five handling events are ordered by completion time.",
    },
    "padded-id": {
        "input": " ABC123 ",
        "predicted": "The backing bean trims surrounding whitespace and finds ABC123.",
    },
    "lowercase-id": {
        "input": "abc123",
        "predicted": "Tracking IDs remain case-sensitive; the cargo is not found.",
    },
    "empty-id": {
        "input": "",
        "predicted": "Required validation prevents the tracking action; no result or map is shown.",
    },
    "unknown-id": {
        "input": "NOPE000",
        "predicted": "The cargo is not found; the FacesMessage is not rendered by this page.",
    },
}


class Node:
    def __init__(self, tag, attrs):
        self.tag = tag
        self.attrs = dict(attrs)
        self.children = []

    def walk(self):
        yield self
        for child in self.children:
            if isinstance(child, Node):
                yield from child.walk()

    def text(self):
        return "".join(
            child.text() if isinstance(child, Node) else child
            for child in self.children
        )


class PageParser(HTMLParser):
    VOID_TAGS = {
        "area",
        "base",
        "br",
        "col",
        "embed",
        "hr",
        "img",
        "input",
        "link",
        "meta",
        "param",
        "source",
        "track",
        "wbr",
    }

    def __init__(self, page):
        super().__init__(convert_charrefs=True)
        self.root = Node("document", [])
        self.stack = [self.root]
        self.feed(page)
        self.close()

    def handle_starttag(self, tag, attrs):
        node = Node(tag, attrs)
        self.stack[-1].children.append(node)
        if tag not in self.VOID_TAGS:
            self.stack.append(node)

    def handle_startendtag(self, tag, attrs):
        node = Node(tag, attrs)
        self.stack[-1].children.append(node)

    def handle_endtag(self, tag):
        for index in range(len(self.stack) - 1, 0, -1):
            if self.stack[index].tag == tag:
                del self.stack[index:]
                return

    def handle_data(self, data):
        self.stack[-1].children.append(data)


def compact(text):
    return " ".join(text.replace("\xa0", " ").split())


def normalize_dates(text):
    def replace(match):
        observed = datetime.strptime(match.group(), "%m/%d/%Y").date()
        offset = (observed - date.today()).days
        if offset == 0:
            return "<TODAY>"
        return f"<TODAY{offset:+d}>"

    return re.sub(r"\b\d{2}/\d{2}/\d{4}\b", replace, text)


def first(nodes, predicate):
    return next((node for node in nodes if predicate(node)), None)


def submit_tracking_id(tracking_id):
    session = requests.Session()
    page_url = f"{BASE_URL}/public/track.xhtml"
    response = session.get(page_url, timeout=30)
    response.raise_for_status()
    parser = PageParser(response.text)
    form = first(
        parser.root.walk(),
        lambda node: node.tag == "form" and node.attrs.get("id") == "trackingForm",
    )
    assert form is not None, "public tracking form was not rendered"

    fields = {
        node.attrs["name"]: node.attrs.get("value", "")
        for node in form.walk()
        if node.tag == "input" and node.attrs.get("name")
    }
    assert fields.get("javax.faces.ViewState"), "JSF ViewState was not rendered"
    fields["trackingForm:trackingIdInput"] = tracking_id
    submit = first(
        form.walk(),
        lambda node: node.tag == "input"
        and node.attrs.get("type") == "submit"
        and node.attrs.get("value") == "Track!",
    )
    assert submit is not None and submit.attrs.get("name")
    fields[submit.attrs["name"]] = submit.attrs.get("value", "")

    action = form.attrs.get("action") or response.url
    response = session.post(
        urljoin(response.url, action),
        data=fields,
        headers={"Referer": response.url},
        timeout=30,
    )
    response.raise_for_status()
    return response


def observe(tracking_id):
    response = submit_tracking_id(tracking_id)
    parser = PageParser(response.text)
    nodes = list(parser.root.walk())
    result_node = first(
        nodes,
        lambda node: node.tag == "div" and node.attrs.get("id") == "result",
    )
    paragraphs = (
        [
            compact(node.text())
            for node in result_node.walk()
            if node.tag == "p"
        ]
        if result_node
        else []
    )

    result = None
    if result_node:
        status_match = re.match(
            r"Cargo\s+(\S+)\s+is currently\s+(.+)", paragraphs[0]
        )
        eta_match = re.match(
            r"Estimated time of arrival in\s+(.+?):\s*(.*)", paragraphs[1]
        )
        assert status_match and eta_match, paragraphs
        result = {
            "tracking_id": status_match.group(1),
            "status_text": status_match.group(2),
            "destination": eta_match.group(1),
            "eta": normalize_dates(eta_match.group(2)),
            "next_activity": next(
                (
                    paragraph
                    for paragraph in paragraphs
                    if paragraph.startswith("Next expected activity is to ")
                ),
                None,
            ),
            "misdirected": any("Cargo is misdirected." in p for p in paragraphs),
        }

    history_label = first(
        nodes,
        lambda node: node.tag == "label"
        and compact(node.text()).startswith("There are no events recorded"),
    )
    history_rows = []
    for node in nodes:
        if node.tag != "div":
            continue
        icons = [
            child
            for child in node.children
            if isinstance(child, Node)
            and child.tag in {"i", "em"}
            and {"fa-check", "fa-flag"}.intersection(
                child.attrs.get("class", "").split()
            )
        ]
        if not icons:
            continue
        text = compact(node.text()).lstrip()
        match = re.match(
            r"(.*), at (\d{2}/\d{2}/\d{4} .+)$",
            text,
        )
        assert match, text
        icon_classes = icons[0].attrs.get("class", "").split()
        history_rows.append(
            {
                "expected": "fa-check" in icon_classes,
                "description": match.group(1).lstrip(),
                "time": normalize_dates(match.group(2)),
            }
        )

    iframe = first(
        nodes,
        lambda node: node.tag == "iframe"
        and "mapFrame" in node.attrs.get("class", "").split(),
    )
    map_query = None
    if iframe:
        query = parse_qs(urlsplit(iframe.attrs["src"]).query, keep_blank_values=True)
        map_query = {key: values[0] for key, values in query.items()}

    tracking_input = first(
        nodes,
        lambda node: node.tag == "input"
        and node.attrs.get("name") == "trackingForm:trackingIdInput",
    )
    return {
        "submitted_id": tracking_input.attrs.get("value", "") if tracking_input else "",
        "result": result,
        "history": {
            "empty_label": compact(history_label.text()) if history_label else None,
            "rows": history_rows,
        },
        "map_query": map_query,
    }


def assert_case(case_name):
    case = CASES[case_name]
    observed = observe(case["input"])
    path = GOLDEN_DIR / f"{case_name}.json"
    if RECORD_GOLDENS:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(
            json.dumps(
                {
                    "input": case["input"],
                    "predicted": case["predicted"],
                    "prediction_matches_observation": None,
                    "observed": observed,
                },
                indent=2,
                ensure_ascii=False,
            )
            + "\n",
            encoding="utf-8",
        )
        return observed

    golden = json.loads(path.read_text(encoding="utf-8"))
    assert golden["input"] == case["input"]
    assert golden["predicted"] == case["predicted"]
    if golden["prediction_matches_observation"] is False:
        assert golden.get("finding")
    else:
        assert golden["prediction_matches_observation"] is True
    assert observed == golden["observed"]
    return observed


@pytest.mark.parametrize(
    "case_name", ("abc123", "jkl567", "def789", "mno456")
)
def test_seeded_cargo_matches_observed_golden(case_name):
    assert_case(case_name)


def test_empty_history_for_unrouted_seed():
    observed = assert_case("def789")
    assert observed["history"]["rows"] == []


def test_tracking_id_entry_trims_surrounding_whitespace():
    observed = assert_case("padded-id")
    assert observed["result"]["tracking_id"] == "ABC123"


def test_tracking_id_entry_remains_case_sensitive():
    observed = assert_case("lowercase-id")
    assert observed["result"] is None


def test_empty_tracking_id_is_rejected_by_required_validation():
    observed = assert_case("empty-id")
    assert observed["result"] is None
    assert observed["map_query"] is None


def test_quirk12_unknown_id_message_is_not_rendered():
    observed = assert_case("unknown-id")
    assert observed["result"] is None
    assert observed["map_query"] is None
    assert observed["history"]["empty_label"] is not None


def test_quirk13_in_port_names_route_destination():
    observed = assert_case("abc123")
    assert observed["result"]["status_text"] == "In port Helsinki"
    assert observed["map_query"]["lastKnownLocationName"] == "New York"


def test_quirk_claimed_cargo_retains_past_eta():
    observed = assert_case("mno456")
    golden = json.loads((GOLDEN_DIR / "mno456.json").read_text(encoding="utf-8"))
    assert golden["prediction_matches_observation"] is False
    assert observed["result"]["eta"] == "<TODAY-28> 12:00 AM UTC"


def test_quirk14_map_offsets_are_random_and_in_range():
    response = requests.get(f"{BASE_URL}/public/mapFrame.xhtml", timeout=30)
    response.raise_for_status()
    expression = re.compile(
        r"Math\.floor\(\s*\(\s*Math\.random\(\)\s*\*\s*3\s*\)\s*-\s*3\s*\)"
    )
    assert len(expression.findall(response.text)) == 6

    source_random = random.SystemRandom()
    loads = [
        tuple(math.floor(source_random.random() * 3 - 3) for _ in range(6))
        for _ in range(20)
    ]
    assert all(-3 <= offset <= -1 for load in loads for offset in load)
    assert len(set(loads)) > 1
