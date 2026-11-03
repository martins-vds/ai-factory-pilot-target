from cargotracker.handling.infrastructure.attempt_submission_repository import (
    DjangoAttemptSubmissionRepository,
)
from cargotracker.handling.interfaces.rest import create_handling_report_view


def compose_handling_report_view():
    return create_handling_report_view(DjangoAttemptSubmissionRepository())
