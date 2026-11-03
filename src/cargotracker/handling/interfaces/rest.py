import json
from datetime import UTC, datetime

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from cargotracker.cargo.domain.tracking_id import TrackingId
from cargotracker.handling.application.accept_registration import accept_registration
from cargotracker.handling.domain.handling_event import HandlingEventType
from cargotracker.handling.domain.registration_attempt import RegistrationAttempt
from cargotracker.handling.infrastructure.attempt_submission_repository import (
    DjangoAttemptSubmissionRepository,
)
from cargotracker.location.domain.un_locode import UnLocode
from cargotracker.voyage.domain.voyage_number import VoyageNumber


@csrf_exempt
@require_POST
def submit_handling_report(request):
    report = json.loads(request.body)
    completion_time = datetime.strptime(report['completionTime'], '%Y-%m-%d %H:%M').replace(
        tzinfo=UTC
    )
    attempt = RegistrationAttempt(
        tracking_id=TrackingId(report['trackingId']),
        completion_time=completion_time,
        registration_time=datetime.now(UTC),
        event_type=HandlingEventType(report['eventType']),
        location=UnLocode(report['unLocode']),
        voyage_number=(
            VoyageNumber(report['voyageNumber']) if report.get('voyageNumber') is not None else None
        ),
    )
    accept_registration(attempt, DjangoAttemptSubmissionRepository())
    return HttpResponse(status=204)
