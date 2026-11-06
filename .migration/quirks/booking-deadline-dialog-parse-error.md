# Deadline dialog only prints date parse failures

## Question
Should the source's deadline-dialog parse-error handling be preserved or replaced with a user-visible error?

## Evidence
- Source: `src/main/java/org/eclipse/cargotracker/interfaces/booking/web/ChangeArrivalDeadlineDate.java:62-70` parses the DTO deadline with `SimpleDateFormat("MM/dd/yyyy")`, catches `ParseException`, prints the stack trace and continues without setting `arrivalDeadlineDate`.
- Characterization: on parse failure, the dialog remains active with its date value unset; the exception is not added as a FacesMessage or otherwise returned to the user.
- Why it looks wrong: a date-loading failure is only logged to stderr and is not translated into an actionable UI state.

## Impact
- Ledger capabilities: `booking.deadline-change`, `booking.dialog-deadline`
- Blocks: implementing this parse-error branch in slice `booking` until a human decides.

## Options
1. Preserve exactly (leave the dialog date unset and only print the exception; pin the behavior).
2. Fix (show an explicit validation/error state; record the divergence in the ledger with this ticket as approval).
3. Other
