import collections
import datetime
import json
import logging
from typing import Any, Dict, Optional

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


def _extra_attributes(record: logging.LogRecord) -> Dict[str, Any]:
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


def default_converter(obj: Any) -> str:
    if isinstance(obj, datetime.datetime):
        return obj.isoformat()
    return str(obj)


class JSONFormatter(logging.Formatter):
    def __init__(
        self,
        *args,
        fields: Dict[str, Any] = None,
        message_field_name: str = "msg",
        exception_field_name: Optional[str] = "exception",
        **kwargs,
    ):
        # Allow to provide any formatter setting (useful to provide a custom date format)
        super().__init__(*args, **kwargs)
        self.fields = fields or {}
        self.usesTime = lambda: "asctime" in self.fields.values()
        self.message_field_name = message_field_name
        self.exception_field_name = exception_field_name

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
            message[self.message_field_name] = super().formatMessage(record)

        message.update(_extra_attributes(record))

        if self.exception_field_name and record.exc_info:
            message[self.exception_field_name] = {
                "type": record.exc_info[0].__name__,
                "message": str(record.exc_info[1]),
                "stack": self.formatException(record.exc_info),
            }

        if len(message) == 1 and self.message_field_name in message:
            return super().formatMessage(record)

        return json.dumps(message, default=default_converter)

    def formatMessage(self, record: logging.LogRecord) -> str:
        # Speed up this step by doing nothing
        return ""
