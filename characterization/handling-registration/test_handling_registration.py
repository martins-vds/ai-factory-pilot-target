import copy
import importlib.util
import json
import os
import time
from datetime import date, datetime, timedelta
from pathlib import Path

import pytest
import requests


HERE = Path(__file__).resolve().parent
GOLDEN_DIR = HERE / "golden"
BASE_URL = os.environ.get(
    "LEGACY_BASE_URL", "http://localhost:8080/cargo-tracker"
).rstrip("/")
RECORD_GOLDENS = os.environ.get("AFS_RECORD_HANDLING_GOLDEN") == "1"
OBSERVATION_SECONDS = 6
QUIET_SECONDS = 2

TRACKING_TEST = HERE.parent / "track-cargo" / "test_tracking.py"
TRACKING_SPEC = importlib.util.spec_from_file_location(
    "track_cargo_characterization", TRACKING_TEST
)
TRACKING = importlib.util.module_from_spec(TRACKING_SPEC)
TRACKING_SPEC.loader.exec_module(TRACKING)

BASE_REPORT = {
    "completionTime": "2026-01-01 12:00",
    "trackingId": "ABC123",
    "eventType": "LOAD",
    "unLocode": "USNYC",
    "voyageNumber": "0200T",
}

VALIDATION_CASES = {
    "missing_completion_time": {
        "report": {key: value for key, value in BASE_REPORT.items() if key != "completionTime"},
        "status": 400,
    },
    "missing_tracking_id": {
        "report": {key: value for key, value in BASE_REPORT.items() if key != "trackingId"},
        "status": 400,
    },
    "missing_event_type": {
        "report": {key: value for key, value in BASE_REPORT.items() if key != "eventType"},
        "status": 400,
    },
    "missing_unlocode": {
        "report": {key: value for key, value in BASE_REPORT.items() if key != "unLocode"},
        "status": 400,
    },
    "completion_time_too_short": {
        "report": {**BASE_REPORT, "completionTime": "2026-01-01"},
        "status": 400,
    },
    "completion_time_too_long": {
        "report": {**BASE_REPORT, "completionTime": "2026-01-01 12:000"},
        "status": 400,
    },
    "tracking_id_too_short": {
        "report": {**BASE_REPORT, "trackingId": "ABC"},
        "status": 400,
    },
    "event_type_too_short": {
        "report": {**BASE_REPORT, "eventType": "LOD"},
        "status": 400,
    },
    "event_type_too_long": {
        "report": {**BASE_REPORT, "eventType": "RECEIVED"},
        "status": 400,
    },
    "unlocode_too_short": {
        "report": {**BASE_REPORT, "unLocode": "USNY"},
        "status": 400,
    },
    "unlocode_too_long": {
        "report": {**BASE_REPORT, "unLocode": "USNYC1"},
        "status": 400,
    },
    "voyage_number_too_short": {
        "report": {**BASE_REPORT, "voyageNumber": "020"},
        "status": 400,
    },
    "voyage_number_too_long": {
        "report": {**BASE_REPORT, "voyageNumber": "0200T1"},
        "status": 400,
    },
    "unparseable_time": {
        "report": {**BASE_REPORT, "completionTime": "not-a-date-time!"},
        "status": 500,
    },
    "unknown_event_type": {
        "report": {**BASE_REPORT, "eventType": "UNKNOWN"},
        "status": 500,
    },
}


def report_time(day_offset, clock):
    day = date.today() + timedelta(days=day_offset)
    return f"{day:%Y-%m-%d} {clock}"


def masked_report(report):
    result = copy.deepcopy(report)
    value = result.get("completionTime")
    if value:
        try:
            day, clock = value.split(" ", 1)
            offset = (date.fromisoformat(day) - date.today()).days
        except ValueError:
            return result
        token = "<TODAY>" if offset == 0 else f"<TODAY{offset:+d}>"
        result["completionTime"] = f"{token} {clock}"
    return result


def masked_input(value):
    if isinstance(value, list):
        return [masked_report(report) for report in value]
    return masked_report(value)


def cargo_state(tracking_id):
    response = requests.get(f"{BASE_URL}/rest/cargo", timeout=30)
    response.raise_for_status()
    return next(
        (cargo for cargo in response.json() if cargo["trackingId"] == tracking_id),
        None,
    )


def snapshot(tracking_id):
    return {
        "cargo": cargo_state(tracking_id),
        "tracking": TRACKING.observe(tracking_id),
    }


def history_rows(observed):
    return observed["tracking"]["history"]["rows"]


def poll_for_rows(tracking_id, minimum_rows, baseline, expected_cargo=None):
    deadline = time.monotonic() + OBSERVATION_SECONDS
    latest = baseline
    while time.monotonic() < deadline:
        latest = snapshot(tracking_id)
        cargo_matches = (
            expected_cargo is None
            or (
                latest["cargo"] is not None
                and all(
                    latest["cargo"].get(key) == value
                    for key, value in expected_cargo.items()
                )
            )
        )
        if len(history_rows(latest)) >= minimum_rows and cargo_matches:
            return latest
        time.sleep(0.15)
    return latest


def poll_until_quiet(tracking_id, baseline):
    deadline = time.monotonic() + QUIET_SECONDS
    latest = baseline
    while time.monotonic() < deadline:
        latest = snapshot(tracking_id)
        if (
            len(history_rows(latest)) > len(history_rows(baseline))
            or latest["cargo"] != baseline["cargo"]
        ):
            return latest
        time.sleep(0.15)
    return latest


def response_observation(response, tracking_id=None, state=None):
    return {
        "post": {
            "status": response.status_code,
            "content_type": response.headers.get("Content-Type", "").split(";")[0],
        },
        "cargo": state["cargo"] if state else None,
        "tracking": state["tracking"] if state else None,
    }


def record_or_compare(name, report, predicted, observed, matches):
    golden = {
        "input": masked_input(report),
        "predicted": predicted,
        "prediction_matches_observation": bool(matches),
        "observed": observed,
    }
    if not matches:
        golden["finding"] = "Observed output differs from the prediction; see the characterization report."

    path = GOLDEN_DIR / f"{name}.json"
    if RECORD_GOLDENS:
        GOLDEN_DIR.mkdir(parents=True, exist_ok=True)
        path.write_text(
            json.dumps(golden, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )
        return

    recorded = json.loads(path.read_text(encoding="utf-8"))
    assert recorded["input"] == golden["input"]
    assert recorded["predicted"] == predicted
    assert recorded["prediction_matches_observation"] == bool(matches)
    if not matches:
        assert recorded.get("finding")
    assert recorded["observed"] == observed


@pytest.mark.parametrize("case_name", tuple(VALIDATION_CASES))
def test_rest_validation_failures_match_observed_goldens(case_name):
    case = VALIDATION_CASES[case_name]
    response = requests.post(
        f"{BASE_URL}/rest/handling/reports",
        json=case["report"],
        timeout=30,
    )
    observed = response_observation(response)
    record_or_compare(
        case_name,
        case["report"],
        f"REST validation returns HTTP {case['status']}.",
        observed,
        response.status_code == case["status"],
    )


def test_seeded_cargo_events_and_off_itinerary_misdirection_match_goldens():
    tracking_id = "ABC123"
    before = snapshot(tracking_id)
    row_count = len(history_rows(before))
    cases = [
        (
            "event_receive",
            {
                "completionTime": report_time(-9, "12:00"),
                "trackingId": tracking_id,
                "eventType": "RECEIVE",
                "unLocode": "CNHKG",
            },
            "A receive at the itinerary origin is accepted and appears in history before the existing load.",
            {"transportStatus": "IN_PORT", "lastKnownLocation": "USNYC"},
        ),
        (
            "event_customs",
            {
                "completionTime": report_time(-8, "12:00"),
                "trackingId": tracking_id,
                "eventType": "CUSTOMS",
                "unLocode": "CNHKG",
            },
            "Customs at the itinerary origin is accepted and is ordered before the existing load.",
            {"transportStatus": "IN_PORT", "lastKnownLocation": "USNYC"},
        ),
        (
            "event_load",
            {
                "completionTime": report_time(1, "12:00"),
                "trackingId": tracking_id,
                "eventType": "LOAD",
                "unLocode": "USNYC",
                "voyageNumber": "0200T",
            },
            "Loading in New York on the next itinerary voyage changes the cargo to onboard.",
            {"transportStatus": "ONBOARD_CARRIER", "lastKnownLocation": "USNYC"},
        ),
        (
            "event_unload",
            {
                "completionTime": report_time(2, "12:00"),
                "trackingId": tracking_id,
                "eventType": "UNLOAD",
                "unLocode": "USDAL",
                "voyageNumber": "0200T",
            },
            "Unloading in Dallas on the current voyage leaves the cargo in port.",
            {"transportStatus": "IN_PORT", "lastKnownLocation": "USDAL"},
        ),
        (
            "event_load_dallas",
            {
                "completionTime": report_time(3, "12:00"),
                "trackingId": tracking_id,
                "eventType": "LOAD",
                "unLocode": "USDAL",
                "voyageNumber": "0300A",
            },
            "Loading in Dallas on the final itinerary voyage changes the cargo to onboard.",
            {"transportStatus": "ONBOARD_CARRIER", "lastKnownLocation": "USDAL"},
        ),
        (
            "unload_at_destination",
            {
                "completionTime": report_time(4, "12:00"),
                "trackingId": tracking_id,
                "eventType": "UNLOAD",
                "unLocode": "FIHEL",
                "voyageNumber": "0300A",
            },
            "Unloading in Helsinki marks the cargo as unloaded at its destination.",
            {
                "transportStatus": "IN_PORT",
                "lastKnownLocation": "FIHEL",
                "atDestination": True,
            },
        ),
        (
            "event_claim",
            {
                "completionTime": report_time(5, "12:00"),
                "trackingId": tracking_id,
                "eventType": "CLAIM",
                "unLocode": "FIHEL",
            },
            "Claiming the cargo in Helsinki changes its transport status to claimed.",
            {"transportStatus": "CLAIMED", "lastKnownLocation": "FIHEL"},
        ),
    ]

    for case_name, report, predicted, expected_cargo in cases:
        response = requests.post(
            f"{BASE_URL}/rest/handling/reports", json=report, timeout=30
        )
        state = poll_for_rows(
            tracking_id, row_count + 1, before, expected_cargo
        )
        observed = response_observation(response, tracking_id, state)
        matches = (
            response.status_code == 204
            and len(history_rows(state)) >= row_count + 1
            and state["cargo"] is not None
            and all(state["cargo"].get(key) == value for key, value in expected_cargo.items())
        )
        record_or_compare(case_name, report, predicted, observed, matches)
        row_count = len(history_rows(state))
        before = state

    report = {
        "completionTime": report_time(6, "12:00"),
        "trackingId": tracking_id,
        "eventType": "UNLOAD",
        "unLocode": "JNTKO",
        "voyageNumber": "0300A",
    }
    response = requests.post(
        f"{BASE_URL}/rest/handling/reports", json=report, timeout=30
    )
    state = poll_for_rows(
        tracking_id,
        row_count + 1,
        before,
        {"misdirected": True, "lastKnownLocation": "JNTKO"},
    )
    observed = response_observation(response, tracking_id, state)
    matches = (
        response.status_code == 204
        and len(history_rows(state)) >= row_count + 1
        and state["cargo"] is not None
        and state["cargo"]["misdirected"] is True
        and state["cargo"]["lastKnownLocation"] == "JNTKO"
    )
    record_or_compare(
        "misdirected_off_itinerary",
        report,
        "An unload in Tokyo, which is not on ABC123's itinerary, is recorded as misdirected.",
        observed,
        matches,
    )


def test_two_quick_reports_are_ordered_by_completion_time():
    tracking_id = "DEF789"
    before = snapshot(tracking_id)
    row_count = len(history_rows(before))
    reports = [
        {
            "completionTime": report_time(2, "12:00"),
            "trackingId": tracking_id,
            "eventType": "CUSTOMS",
            "unLocode": "CNHKG",
        },
        {
            "completionTime": report_time(1, "12:00"),
            "trackingId": tracking_id,
            "eventType": "RECEIVE",
            "unLocode": "CNHKG",
        },
    ]
    responses = [
        requests.post(
            f"{BASE_URL}/rest/handling/reports", json=report, timeout=30
        )
        for report in reports
    ]
    state = poll_for_rows(tracking_id, row_count + 2, before)
    observed = {
        "posts": [response.status_code for response in responses],
        "cargo": state["cargo"],
        "tracking": state["tracking"],
    }
    rows = history_rows(state)
    ordered = len(rows) >= row_count + 2 and rows[-2]["time"] < rows[-1]["time"]
    matches = all(response.status_code == 204 for response in responses) and ordered
    record_or_compare(
        "two_reports_ordered_by_completion_time",
        reports,
        "Both quick reports are accepted and the public history orders them by completion time, not submission order.",
        observed,
        matches,
    )


@pytest.mark.parametrize(
    ("case_name", "report", "tracking_id"),
    [
        (
            "unknown_tracking_id",
            {
                "completionTime": report_time(7, "12:00"),
                "trackingId": "NOPE000",
                "eventType": "RECEIVE",
                "unLocode": "CNHKG",
            },
            "NOPE000",
        ),
        (
            "unknown_voyage",
            {
                "completionTime": report_time(7, "12:00"),
                "trackingId": "DEF789",
                "eventType": "LOAD",
                "unLocode": "CNHKG",
                "voyageNumber": "9999Z",
            },
            "DEF789",
        ),
        (
            "unknown_location",
            {
                "completionTime": report_time(7, "12:00"),
                "trackingId": "DEF789",
                "eventType": "RECEIVE",
                "unLocode": "ZZZZZ",
            },
            "DEF789",
        ),
        (
            "load_without_voyage",
            {
                "completionTime": report_time(7, "12:00"),
                "trackingId": "DEF789",
                "eventType": "LOAD",
                "unLocode": "USNYC",
            },
            "DEF789",
        ),
    ],
)
def test_unknown_references_and_load_without_voyage_leave_no_trace(
    case_name, report, tracking_id
):
    before = snapshot(tracking_id)
    response = requests.post(
        f"{BASE_URL}/rest/handling/reports", json=report, timeout=30
    )
    state = poll_until_quiet(tracking_id, before)
    observed = response_observation(response, tracking_id, state)
    matches = (
        response.status_code == 204
        and state["cargo"] == before["cargo"]
        and state["tracking"]["history"] == before["tracking"]["history"]
    )
    record_or_compare(
        case_name,
        report,
        "The REST endpoint accepts the format-valid report, but the worker leaves no visible cargo or history trace.",
        observed,
        matches,
    )
