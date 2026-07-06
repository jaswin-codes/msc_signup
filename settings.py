import os
from datetime import datetime

try:
    import local_settings as _local_settings
except ImportError:
    _local_settings = None


def _get_value(name, env_name, default=""):
    if _local_settings is not None and hasattr(_local_settings, name):
        return getattr(_local_settings, name)
    return os.getenv(env_name, default)


STUDENT_NUMBER = _get_value("STUDENT_NUMBER", "MSC_STUDENT_NUMBER")
FULL_NAME = _get_value("FULL_NAME", "MSC_FULL_NAME")
EMAIL = _get_value("EMAIL", "MSC_EMAIL")
CELL = _get_value("CELL", "MSC_CELL")
EMERGENCY = _get_value("EMERGENCY", "MSC_EMERGENCY")
COMMENTS = _get_value("COMMENTS", "MSC_COMMENTS")
UCT_USERNAME = _get_value("UCT_USERNAME", "MSC_UCT_USERNAME")
UCT_PASSWORD = _get_value("UCT_PASSWORD", "MSC_UCT_PASSWORD")
SIGNUP_TIME = _get_value("SIGNUP_TIME", "MSC_SIGNUP_TIME")
NO_X = int(_get_value("NO_X", "MSC_NO_X", "902"))
NO_Y = int(_get_value("NO_Y", "MSC_NO_Y", "971"))
PAGE_URL = _get_value(
    "PAGE_URL",
    "MSC_PAGE_URL",
    "https://amathuba.uct.ac.za/d2l/le/lessons/19864/topics/3194308",
)


def require_runtime_settings():
    missing = []

    for label, value in (
        ("STUDENT_NUMBER", STUDENT_NUMBER),
        ("FULL_NAME", FULL_NAME),
        ("EMAIL", EMAIL),
        ("CELL", CELL),
        ("EMERGENCY", EMERGENCY),
        ("COMMENTS", COMMENTS),
        ("UCT_USERNAME", UCT_USERNAME),
        ("UCT_PASSWORD", UCT_PASSWORD),
        ("SIGNUP_TIME", SIGNUP_TIME),
    ):
        if not value:
            missing.append(label)

    if missing:
        raise RuntimeError(
            "Missing required signup values: "
            + ", ".join(missing)
            + ". Add them to local_settings.py or set the matching MSC_* environment variables."
        )

    try:
        parsed_signup_time = datetime.strptime(SIGNUP_TIME, "%Y-%m-%d %H:%M:%S")
    except ValueError as exc:
        raise RuntimeError(
            f"SIGNUP_TIME must use YYYY-MM-DD HH:MM:SS format, got {SIGNUP_TIME!r}"
        ) from exc

    if parsed_signup_time <= datetime.now():
        raise RuntimeError(
            f"SIGNUP_TIME must be in the future before you run the signup script, got {SIGNUP_TIME!r}"
        )