"""Opt-in real Payara/Derby experiment for HR-04E-TIME, never a golden rewrite."""

import importlib.util
import json
import os
import time
from datetime import UTC, datetime, timedelta
from pathlib import Path

import pytest
import requests

HERE = Path(__file__).resolve().parent
pytestmark = pytest.mark.skipif(
    "HR_04E_TIME_DOMAIN" not in os.environ,
    reason="requires the dedicated run-timestamp-reload.sh fixture",
)


def test_timestamps_across_source_cache_clear():
    spec = importlib.util.spec_from_file_location(
        "timestamp_tracking", HERE.parent / "track-cargo" / "test_tracking.py"
    )
    tracking = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(tracking)
    tracking.normalize_dates = lambda text: text
    base = os.environ["LEGACY_BASE_URL"]
    probe = os.environ["HR_04E_TIME_PROBE"]
    reference = datetime.now(UTC)
    completion = (reference - timedelta(days=1)).strftime("%Y-%m-%d 12:34")
    observation = {
        "source_sha": "f3beacf78de4f6d34edc4971ac87e38a5c6fe59d",
        "reference_utc": reference.isoformat(),
        "domain": os.environ["HR_04E_TIME_DOMAIN"],
        "database_directory": os.environ["HR_04E_TIME_DATABASE"],
        "base_url": base,
        "predicted": {
            "immediate_history": "12:34 PM UTC, as in the prior noon goldens",
            "stored": "DATE columns for completion and registration",
            "after_clear": "12:00 AM UTC; registration loses time-of-day",
            "ties": "distinct registration instants may collapse to one stored date",
        },
        "baseline": tracking.observe("DEF789"),
        "submissions": [],
    }
    assert observation["baseline"]["history"]["rows"] == []
    for event_type in ("RECEIVE", "CUSTOMS"):
        report = {
            "completionTime": completion,
            "trackingId": "DEF789",
            "eventType": event_type,
            "unLocode": "CNHKG",
        }
        sent = datetime.now(UTC).isoformat()
        response = requests.post(f"{base}/rest/handling/reports", json=report, timeout=30)
        observation["submissions"].append(
            {
                "input": report,
                "sent_utc": sent,
                "response_utc": datetime.now(UTC).isoformat(),
                "status": response.status_code,
            }
        )
        assert response.status_code == 204
        deadline = time.monotonic() + 30
        while time.monotonic() < deadline:
            immediate = tracking.observe("DEF789")
            if len(immediate["history"]["rows"]) == len(observation["submissions"]):
                break
            time.sleep(0.15)
        else:
            pytest.fail("accepted report did not appear in processed public history")
        # Wait after confirmed processing, not between two unobserved JMS submissions.
        time.sleep(1.1)

    observation["immediate_history"] = immediate
    before = requests.get(probe, timeout=30)
    before.raise_for_status()
    observation["before_clear"] = before.json()
    clear = requests.post(probe, timeout=30)
    clear.raise_for_status()
    observation["clear_boundary"] = clear.json()
    assert observation["clear_boundary"]["cache_empty"] is True
    log_path = Path(os.environ["HR_04E_TIME_DOMAIN"]) / "logs" / "server.log"
    log_offset = log_path.stat().st_size
    observation["after_clear_history"] = tracking.observe("DEF789")
    with log_path.open(encoding="utf-8") as log:
        log.seek(log_offset)
        observation["reload_sql"] = [
            line.strip() for line in log
            if "SELECT" in line and "FROM HANDLINGEVENT" in line
        ]
    after = requests.get(probe, timeout=30)
    after.raise_for_status()
    observation["after_clear"] = after.json()
    observation["finished_utc"] = datetime.now(UTC).isoformat()
    output = Path(os.environ["HR_04E_TIME_OUTPUT"])
    with output.open("x", encoding="utf-8") as stream:
        json.dump(observation, stream, indent=2)
        stream.write("\n")
    print(f"Timestamp observations: {output}")

    assert observation["reload_sql"], "no source HandlingEvent SELECT after cache clear"
    assert observation["before_clear"]["session"] == observation["after_clear"]["session"]
    assert observation["before_clear"]["columns"] == [
        {"name": "COMPLETIONTIME", "sql_type": "DATE"},
        {"name": "REGISTRATION", "sql_type": "DATE"},
    ]
    assert observation["before_clear"]["rows"] == observation["after_clear"]["rows"]
    assert observation["before_clear"]["rows"] == observation["clear_boundary"]["rows"]
    assert len(observation["before_clear"]["rows"]) == 2
    assert all(
        row["time"].endswith("12:34 PM UTC")
        for row in immediate["history"]["rows"]
    )
    assert all(
        row["time"].endswith("12:00 AM UTC")
        for row in observation["after_clear_history"]["history"]["rows"]
    )
    cached_before = observation["before_clear"]["cached"]
    cached_after = observation["after_clear"]["cached"]
    assert len(cached_before) == len(cached_after) == 2
    assert [row["id"] for row in cached_before] == [row["id"] for row in cached_after]
    assert len({row["registration"] for row in cached_before}) == 2
    assert len({row["registration"] for row in cached_after}) == 1
    assert all(row["completion"].endswith("T00:00:00Z") for row in cached_after)
    assert all(row["registration"].endswith("T00:00:00Z") for row in cached_after)
