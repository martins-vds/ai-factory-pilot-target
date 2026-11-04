import json
from collections.abc import Callable
from datetime import UTC, datetime

from django import forms
from django.core.exceptions import ValidationError
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from cargotracker.cargo.domain.tracking_id import TrackingId
from cargotracker.handling.application.accept_registration import accept_registration
from cargotracker.handling.domain.handling_event import HandlingEventType
from cargotracker.handling.domain.registration_attempt import RegistrationAttempt
from cargotracker.handling.domain.repository import RegistrationAttemptRepository
from cargotracker.location.domain.un_locode import UnLocode
from cargotracker.voyage.domain.voyage_number import VoyageNumber


class _StringField(forms.CharField):
    def to_python(self, value):
        if value in self.empty_values:
            return self.empty_value
        if not isinstance(value, str):
            raise ValidationError('Enter a valid string.', code='invalid')
        return super().to_python(value)


class HandlingReportForm(forms.Form):
    completionTime = _StringField(min_length=16, max_length=16, strip=False)
    trackingId = _StringField(min_length=4, strip=False)
    eventType = _StringField(min_length=4, max_length=7, strip=False)
    unLocode = _StringField(min_length=5, max_length=5, strip=False)
    voyageNumber = _StringField(required=False, min_length=4, max_length=5, strip=False)

    def clean_completionTime(self):
        value = self.cleaned_data['completionTime']
        try:
            completion_time = datetime.strptime(value, '%Y-%m-%d %H:%M')
        except ValueError as exc:
            raise ValidationError('Enter a valid completion time.', code='invalid') from exc
        if completion_time.isoformat(sep=' ', timespec='minutes') != value:
            raise ValidationError('Enter a valid completion time.', code='invalid')
        return completion_time.replace(tzinfo=UTC)

    def clean_trackingId(self):
        return TrackingId(self.cleaned_data['trackingId'])

    def clean_eventType(self):
        value = self.cleaned_data['eventType']
        try:
            return HandlingEventType(value)
        except ValueError as exc:
            raise ValidationError('Select a valid event type.', code='invalid') from exc

    def clean_unLocode(self):
        value = self.cleaned_data['unLocode']
        try:
            return UnLocode(value)
        except ValueError as exc:
            raise ValidationError('Enter a valid UN/LOCODE.', code='invalid') from exc

    def clean_voyageNumber(self):
        value = self.cleaned_data['voyageNumber']
        if not value:
            if 'voyageNumber' in self.data and self.data['voyageNumber'] is not None:
                raise ValidationError(
                    'Ensure this value has at least 4 characters.', code='min_length'
                )
            return None
        return VoyageNumber(value)


def _bad_request(errors):
    return JsonResponse({'errors': errors}, status=400)


def create_handling_report_view(
    repository: RegistrationAttemptRepository,
) -> Callable[[HttpRequest], HttpResponse]:
    @csrf_exempt
    @require_POST
    def submit_handling_report(request):
        try:
            report = json.loads(request.body)
        except (json.JSONDecodeError, UnicodeDecodeError):
            return _bad_request({'non_field_errors': ['Request body must be valid JSON.']})
        if not isinstance(report, dict):
            return _bad_request({'non_field_errors': ['Request body must be a JSON object.']})

        form = HandlingReportForm(report)
        if not form.is_valid():
            errors = {
                field: [error['message'] for error in field_errors]
                for field, field_errors in form.errors.get_json_data().items()
            }
            return _bad_request(errors)

        data = form.cleaned_data
        attempt = RegistrationAttempt(
            tracking_id=data['trackingId'],
            completion_time=data['completionTime'],
            registration_time=datetime.now(UTC),
            event_type=data['eventType'],
            location=data['unLocode'],
            voyage_number=data['voyageNumber'],
        )
        accept_registration(attempt, repository)
        response = HttpResponse(status=204)
        del response['Content-Type']
        return response

    return submit_handling_report
