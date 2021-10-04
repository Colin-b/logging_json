import collections
import json
import logging
from typing import Any

standard_attributes = (
    "name",
    "msg",
    "args",
    "levelname",
    "levelno",
    "pathname",
    "filename",
    "module",
    "exc_info",
    "exc_text",
    "stack_info",
    "lineno",
    "funcName",
    "created",
    "msecs",
    "relativeCreated",
    "thread",
    "threadName",
    "processName",
    "process",
    "message",
    "asctime",
)


def _extra_attributes(record: logging.LogRecord) -> dict[str, Any]:
    return {
        name: record.__dict__[name]
        for name in set(record.__dict__).difference(standard_attributes)
    }


def _value(record: logging.LogRecord, field_name_or_value: Any) -> Any:
    """
    Retrieve value from record if possible. Otherwise use value.
    :param record: The record to extract a field named as in field_name_or_value.
    :param field_name_or_value: The field name to extract from record or the default value to use if not present.
    """
    try:
        return getattr(record, field_name_or_value)
    except:
        return field_name_or_value


class JSONFormatter(logging.Formatter):
    def __init__(self, *args, fields=None, **kwargs):
        # Allow to provide any formatter setting (useful to provide a custom date format)
        super().__init__(*args, **kwargs)
        self.fields = fields or {}
        self.usesTime = lambda: "asctime" in self.fields.values()

    def format(self, record: logging.LogRecord):
        # Let python set every additional record field
        super().format(record)

        message = {
            field_name: _value(record, field_value)
            for field_name, field_value in self.fields.items()
        }
        if isinstance(record.msg, collections.abc.Mapping):
            message.update(record.msg)
        else:
            message["msg"] = super().formatMessage(record)

        message.update(_extra_attributes(record))

        if record.exc_info:
            message["exception"] = {
                "type": record.exc_info[0].__name__,
                "message": str(record.exc_info[1]),
                "stack": self.formatException(record.exc_info),
            }

        return (
            super().formatMessage(record)
            if (len(message) == 1 and "msg" in message)
            else json.dumps(message)
        )

    def formatMessage(self, record: logging.LogRecord) -> str:
        # Speed up this step by doing nothing
        return ""
