import logging
import json
import time
import datetime
import pytest
import sys

import logging_json


class MyException(Exception):
    pass


def test_empty_dict_message(caplog):
    caplog.set_level("INFO")
    logging.info({})
    assert fmt(caplog) == "{}"


def test_dict_message(caplog):
    caplog.set_level("INFO")
    logging.info({"key 1": "value 1", "key 2": 2})
    assert fmt(caplog) == '{"key 1": "value 1", "key 2": 2}'


def test_str_message(caplog):
    caplog.set_level("INFO")
    logging.info("message 1")
    assert fmt(caplog) == "message 1"


def test_str_with_args_message(caplog):
    caplog.set_level("INFO")
    logging.info("message %s", "1")
    assert fmt(caplog) == "message 1"


def test_str_with_message_field_name(caplog):
    caplog.set_level("INFO")
    logging.info("message 1")
    assert fmt(caplog, message_field_name="msg") == "message 1"


def test_str_with_extra_message(caplog):
    caplog.set_level("INFO")
    logging.info("message 1", extra={"key1": "value 1"})
    assert dict_fmt(caplog) == {"message": "message 1", "key1": "value 1"}


def test_str_with_message_field_name_and_fields(caplog):
    caplog.set_level("INFO")
    logging.info("message 1")
    assert dict_fmt(
        caplog, message_field_name="msg", fields={"level": "levelname"}
    ) == {"msg": "message 1", "level": "INFO"}


def test_str_with_args_and_extra_message(caplog):
    caplog.set_level("INFO")
    logging.info("message %s", "1", extra={"key1": "value 1"})
    assert dict_fmt(caplog) == {"message": "message 1", "key1": "value 1"}


def test_dict_message_with_asctime(caplog, monkeypatch):
    monkeypatch.setattr(time, "time", lambda: 1599736353.0076675)
    caplog.set_level("INFO")
    logging.info({"key 1": "value 1", "key 2": 2})
    actual = dict_fmt(caplog, fields={"date_time": "asctime"})
    assert time.strptime(actual.pop("date_time"), "%Y-%m-%d %H:%M:%S,007")
    assert actual == {"key 1": "value 1", "key 2": 2}


def test_str_message_with_asctime(caplog, monkeypatch):
    monkeypatch.setattr(time, "time", lambda: 1599736353.0076675)
    caplog.set_level("INFO")
    logging.info("message 1")
    actual = dict_fmt(caplog, fields={"date_time": "asctime"})
    assert time.strptime(actual.pop("date_time"), "%Y-%m-%d %H:%M:%S,007")
    assert actual == {"message": "message 1"}


def test_str_with_args_message_with_asctime(caplog, monkeypatch):
    monkeypatch.setattr(time, "time", lambda: 1599736353.0076675)
    caplog.set_level("INFO")
    logging.info("message %s", "1")
    actual = dict_fmt(caplog, fields={"date_time": "asctime"})
    assert time.strptime(actual.pop("date_time"), "%Y-%m-%d %H:%M:%S,007")
    assert actual == {"message": "message 1"}


def test_str_with_args_and_extra_message_with_asctime(caplog, monkeypatch):
    monkeypatch.setattr(time, "time", lambda: 1599736353.0076675)
    caplog.set_level("INFO")
    logging.info("message %s", "1", extra={"key1": "value 1"})
    actual = dict_fmt(caplog, fields={"date_time": "asctime"})
    assert time.strptime(actual.pop("date_time"), "%Y-%m-%d %H:%M:%S,007")
    assert actual == {"message": "message 1", "key1": "value 1"}


def test_dict_message_at_exception_level(caplog):
    caplog.set_level("INFO")
    try:
        raise MyException("this is the exception message")
    except MyException:
        logging.exception({"key 1": "value 1", "key 2": 2})
    actual = dict_fmt(caplog)
    actual["exception"].pop("stack")
    assert actual == {
        "key 1": "value 1",
        "key 2": 2,
        "exception": {
            "message": "this is the exception message",
            "type": "MyException",
        },
    }


def test_dict_message_at_exception_level_with_different_field_name(caplog):
    caplog.set_level("INFO")
    try:
        raise MyException("this is the exception message")
    except MyException:
        logging.exception({"key 1": "value 1", "key 2": 2})
    actual = dict_fmt(caplog, exception_field_name="info_about_exception")
    actual["info_about_exception"].pop("stack")
    assert actual == {
        "key 1": "value 1",
        "key 2": 2,
        "info_about_exception": {
            "message": "this is the exception message",
            "type": "MyException",
        },
    }


@pytest.mark.parametrize("value", [None, ""])
def test_dict_message_at_exception_level_without_exception_field(caplog, value):
    caplog.set_level("INFO")
    try:
        raise MyException("this is the exception message")
    except MyException:
        logging.exception({"key 1": "value 1", "key 2": 2})
    actual = dict_fmt(caplog, exception_field_name=value)
    assert actual == {
        "key 1": "value 1",
        "key 2": 2,
    }


def test_str_message_at_exception_level(caplog):
    caplog.set_level("INFO")
    try:
        raise MyException("this is the exception message")
    except MyException:
        logging.exception("message 1")
    actual = dict_fmt(caplog)
    actual["exception"].pop("stack")
    assert actual == {
        "message": "message 1",
        "exception": {
            "message": "this is the exception message",
            "type": "MyException",
        },
    }


def test_str_with_args_message_at_exception_level(caplog):
    caplog.set_level("INFO")
    try:
        raise MyException("this is the exception message")
    except MyException:
        logging.exception("message %s", "1")
    actual = dict_fmt(caplog)
    actual["exception"].pop("stack")
    assert actual == {
        "message": "message 1",
        "exception": {
            "message": "this is the exception message",
            "type": "MyException",
        },
    }


def test_documented_record_attributes(caplog, monkeypatch):
    monkeypatch.setattr(time, "time", lambda: 1599736353.0076675)
    caplog.set_level("INFO")
    logging.info({})
    actual = dict_fmt(
        caplog,
        fields={
            "logger_name": "name",
            "level_number": "levelno",
            "level_name": "levelname",
            "file_path": "pathname",
            "file_name": "filename",
            "module_name": "module",
            "line_number": "lineno",
            "function_name": "funcName",
            "timestamp": "created",
            "timestamp_milliseconds": "msecs",
            "relative_timestamp": "relativeCreated",
            "thread_id": "thread",
            "thread_name": "threadName",
            "process_id": "process",
            "process_name": "processName",
            "task_name": "taskName",
            "record_message": "message",
            "extra": "this is a value",
        },
    )
    actual.pop("file_path")
    actual.pop("thread_id")
    actual.pop("process_id")
    actual.pop("relative_timestamp")
    actual.pop("line_number")
    python310 = sys.version_info.minor >= 10
    assert actual == {
        "extra": "this is a value",
        "file_name": "test_formatter.py",
        "function_name": "test_documented_record_attributes",
        "level_name": "INFO",
        "level_number": 20,
        "logger_name": "root",
        "module_name": "test_formatter",
        "process_name": "MainProcess",
        "record_message": "{}",
        "thread_name": "MainThread",
        "task_name": None,
        "timestamp": 1599736353.0076675,
        "timestamp_milliseconds": 7.0 if python310 else 7.66754150390625,
    }


def test_with_extra_in_fields_and_message(caplog):
    caplog.set_level("INFO")
    logging.info("message 1", extra={"key1": "value 1"})
    assert dict_fmt(caplog, fields={"extra": "key1", "key2": "value 2",},) == {
        "extra": "value 1",
        "key1": "value 1",
        "key2": "value 2",
        "message": "message 1",
    }


def test_json_dumps_error(caplog):
    class CustomWithoutStr:
        pass

    custom = CustomWithoutStr()

    class CustomWithStr:
        def __str__(self):
            return "Custom instance"

    caplog.set_level("INFO")
    logging.info(
        {
            "my_datetime": datetime.datetime(
                2020, 1, 10, 3, 14, 11, tzinfo=datetime.timezone.utc
            ),
            "my_date": datetime.date(2020, 1, 10),
            "my_time": datetime.time(3, 14, 11, tzinfo=datetime.timezone.utc),
            "my_custom_obj": custom,
            "my_custom_obj_with_str": CustomWithStr(),
        }
    )
    assert dict_fmt(caplog,) == {
        "my_custom_obj": str(custom),
        "my_custom_obj_with_str": "Custom instance",
        "my_date": "2020-01-10",
        "my_datetime": "2020-01-10T03:14:11+00:00",
        "my_time": "03:14:11+00:00",
    }


def fmt(caplog, *formatter_args, **formatter_kwargs) -> str:
    return logging_json.JSONFormatter(*formatter_args, **formatter_kwargs).format(
        caplog.records[0]
    )


def dict_fmt(caplog, *formatter_args, **formatter_kwargs) -> dict:
    return json.loads(fmt(caplog, *formatter_args, **formatter_kwargs))
