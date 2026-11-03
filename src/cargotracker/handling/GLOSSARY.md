# Handling

The record of what physically happened to a cargo. Reports of handling arrive from outside (the handling
report API, the event logger, uploaded event files) and become handling events once they are verified.

## Language

**Handling event**:
A verified, stored fact that a cargo was handled in a specific way, at a location, at a completion time.
_Avoid_: Event (unqualified), handling record

**Registration attempt**:
A report that a handling event happened, as submitted through a front door, before it has been verified.
_Avoid_: Handling report (for the attempt itself), registration

**Accepted**:
A registration attempt that a front door has validated and queued for processing. This is what the
submitter is told. An accepted attempt is always processed: it ends registered or rejected, never lost.
_Avoid_: Submitted, registered (for an attempt that is only queued)

**Registered**:
A registration attempt that became a handling event and was stored. Only from then on does it appear in a
cargo's handling history.
_Avoid_: Accepted, processed

**Rejected**:
An accepted registration attempt that can never become a handling event: its cargo, voyage or location is
unknown, or its data is invalid. A rejection is recorded with its reason. An attempt that only failed
temporarily is retried, not rejected.
_Avoid_: Failed, dropped, dead-lettered
