import time

from nova.logging.legacy import log_event  # legacy logging API v1
from nova_errors import log_retry_log_failure


MAX_RETRIES = 3
RETRY_BACKOFF_SECONDS = 2


def submit_usage_record(customer_id: str, usage_record: dict) -> bool:
    """Submit a single usage record to the billing pipeline with retries.

    Retry attempts are logged through the legacy v1 API, which only
    accepts a level and a message string. It cannot carry the retry
    count, customer_id, or usage_record id as structured fields, so a
    failed retry is easy to miss in log search and does not correlate
    back to the originating usage record.
    """
    attempt = 0
    last_error = None
    while attempt < MAX_RETRIES:
        attempt += 1
        try:
            return _send_to_billing_pipeline(customer_id, usage_record)
        except BillingPipelineError as exc:
            last_error = exc
            log_event("WARN", f"billing usage submit failed, retrying: {exc}")
            time.sleep(RETRY_BACKOFF_SECONDS * attempt)

    # Retry_Log_Failure: legacy log_event(level, message) drops
    # retry_count / customer_id / usage_record id, no structured
    # context survives past this line.
    log_retry_log_failure(
        service="usage-metering-service",
        sink="usage_ledger_write",
        customer_id=customer_id,
        event_id=usage_record.get("id"),
        retry_attempts=attempt,
        max_retries=MAX_RETRIES,
        last_error=str(last_error),
    )
    return False


def _send_to_billing_pipeline(customer_id: str, usage_record: dict) -> bool:
    """Send a usage record to the billing pipeline. Raises BillingPipelineError on failure."""
    raise NotImplementedError


class BillingPipelineError(Exception):
    """Raised when the billing pipeline rejects or fails to accept a usage record."""
