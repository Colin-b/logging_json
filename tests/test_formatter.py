import logging
import json
import time

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
    assert actual == {"msg": "message 1"}


def test_str_with_args_message_with_asctime(caplog, monkeypatch):
    monkeypatch.setattr(time, "time", lambda: 1599736353.0076675)
    caplog.set_level("INFO")
    logging.info("message %s", "1")
    actual = dict_fmt(caplog, fields={"date_time": "asctime"})
    assert time.strptime(actual.pop("date_time"), "%Y-%m-%d %H:%M:%S,007")
    assert actual == {"msg": "message 1"}


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


def test_str_message_at_exception_level(caplog):
    caplog.set_level("INFO")
    try:
        raise MyException("this is the exception message")
    except MyException:
        logging.exception("message 1")
    actual = dict_fmt(caplog)
    actual["exception"].pop("stack")
    assert actual == {
        "msg": "message 1",
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
        "msg": "message 1",
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
            "record_message": "message",
            "extra": "this is a value",
        },
    )
    actual.pop("file_path")
    actual.pop("thread_id")
    actual.pop("process_id")
    actual.pop("relative_timestamp")
    actual.pop("line_number")
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
        "timestamp": 1599736353.0076675,
        "timestamp_milliseconds": 7.66754150390625,
    }


def fmt(caplog, *formatter_args, **formatter_kwargs) -> str:
    return logging_json.JSONFormatter(*formatter_args, **formatter_kwargs).format(
        caplog.records[0]
    )


def dict_fmt(caplog, *formatter_args, **formatter_kwargs) -> dict:
    return json.loads(fmt(caplog, *formatter_args, **formatter_kwargs))
