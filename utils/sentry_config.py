import os
import sentry_sdk


def init_sentry():
    """
    Initialize Sentry error and performance monitoring for the application.
    """
    dsn = os.getenv("SENTRY_DSN")
    if not dsn:
        return

    sentry_sdk.init(
        dsn=dsn,
        traces_sample_rate=1.0,
        environment=os.getenv("SENTRY_ENV", "dev"),
    )
