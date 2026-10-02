"""Shared error reporting for Nova billing/usage services.

Wraps the legacy logging API (v1), which only accepts a level and a
message string. Structured context passed in here (customer_id,
event_id, retry_attempts, last_error, trace context, etc.) has
nowhere to go but the message string, so it is not reliably
searchable or correlatable after the fact. This is why trace_id
shows up empty on RETRY_LOG_FAILURE log lines raised through this
path: v1 has no field to carry it.
"""

from nova.logging.legacy import log_event  # legacy logging API v1


RETRY_LOG_FAILURE = "RETRY_LOG_FAILURE"


# Retry_Log_Failure: emits error_code=RETRY_LOG_FAILURE once retries
# against the usage ledger are exhausted.
def log_retry_log_failure(
    service: str,
    sink: str,
    customer_id: str,
    event_id: str,
    retry_attempts: int,
    max_retries: int,
    last_error: str,
) -> None:
    """Log that retries were exhausted writing/logging a usage event.

    error_code: RETRY_LOG_FAILURE. All context below is folded into
    a single message string, since v1's log_event(level, message)
    has no structured fields to carry it through.
    """
    log_event(
        "ERROR",
        f"error_code={RETRY_LOG_FAILURE} service={service} sink={sink} "
        f"customer_id={customer_id} event_id={event_id} "
        f"retry_attempts={retry_attempts} max_retries={max_retries} "
        f"last_error={last_error}",
    )
