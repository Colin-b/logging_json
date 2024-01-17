<h2 align="center">JSON formatter for logging</h2>

<p align="center">
<a href="https://pypi.org/project/logging_json/"><img alt="pypi version" src="https://img.shields.io/pypi/v/logging_json"></a>
<a href="https://github.com/Colin-b/logging_json/actions"><img alt="Build status" src="https://github.com/Colin-b/logging_json/workflows/Release/badge.svg"></a>
<a href="https://github.com/Colin-b/logging_json/actions"><img alt="Coverage" src="https://img.shields.io/badge/coverage-100%25-brightgreen"></a>
<a href="https://github.com/psf/black"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>
<a href="https://github.com/Colin-b/logging_json/actions"><img alt="Number of tests" src="https://img.shields.io/badge/tests-24 passed-blue"></a>
<a href="https://pypi.org/project/logging_json/"><img alt="Number of downloads" src="https://img.shields.io/pypi/dm/logging_json"></a>
</p>

This module provides a JSON formatter for the python [`logging`](https://docs.python.org/3/library/logging.html) module that will format to JSON formatted string.

Using this formatter allows to have the proper format for logging to `Splunk` or `ElasticSearch`, but it can also be used for logging to stdout as a string is issued.

- [Features](#features)
  - [Custom fields](#adding-additional-fields-and-values)
  - [dict logging](#logging-with-a-dictionary)
  - [str logging](#logging-with-anything-else-such-as-a-string)
- [Configuration](#configuration)
  - [Using dictConfig](#using-loggingconfigdictconfig)

## Features

### Adding additional fields and values

You can add fields to every message that is being logged.
To do so, specify the `fields` parameter to the `logging_json.JSONFormatter` instance.

It must be a dictionary where keys are the keys to be appended to the resulting JSON dictionary (if not already present) and the values can be one of the following:
* An attribute of the logging record (non-exhaustive list can be found on [the python logging documentation](https://docs.python.org/3/library/logging.html#logrecord-attributes)).
* If not found on the record, the value will be linked to the key.

#### Logging exceptions, a specific case

If an exception is logged, the `exception` key will be appended to the resulting JSON dictionary.

This dictionary will contain 3 keys:
* `type`: The name of the exception class (useful when the message is blank).
* `message`: The str representation of the exception (usually the provided error message).
* `stack`: The stack trace, formatted as a string.

You can rename the exception field key by setting the `exception_field_name` parameter with a new name for the key.
It is also possible to disable this behaviour by setting the `exception_field_name` parameter to `None` or an empty string

### Logging with a dictionary

This formatter allows you to log dictionary as in the following:

```python
import logging

logging.info({"key": "value", "other key": "other value"})
```

The resulting JSON dictionary will be the one you provided (with the [additional fields](#adding-additional-fields-and-values)).

### Logging with anything else (such as a string)

Anything not logged using a dictionary will be handled by the standard formatter, and it can result in one of the 2 output:
* A JSON dictionary, if [additional fields](#adding-additional-fields-and-values) are set or if `extra` parameter is used while logging, with the message available in the `message` key of the resulting JSON dictionary.
  Default `message` key name can be changed by `message_field_name` parameter of the `logging_json.JSONFormatter` instance.
* The formatted record, if no [additional fields](#adding-additional-fields-and-values) are set.

This handles the usual string logging as in the following:

```python
import logging

logging.info("This is my message")
```

### Changing asctime representation

You can override the default representation of asctime (`2003-07-08 16:49:45,896`) based on two different scenarii:

#### Without milliseconds

Two options are at your disposal depending on your need:

1) Option 1: The default representation for everything besides milliseconds suits you.
   Set `default_msec_format` parameter to None.
   It would result in a representation like `2003-07-08 16:49:45`.

2) Option 2: You want to change the default representation (without milliseonds).
   Set `datefmt` parameter to something else than `%Y-%m-%d %H:%M:%S`.
   It would result in a representation like `2003-07-08T16:49:45` for `%Y-%m-%dT%H:%M:%S`.

#### With milliseconds

Set `default_time_format` to something else than `%Y-%m-%d %H:%M:%S` to change the representation part without milliseconds.
Set `default_msec_format` to something else than `%s,%03d` to change the representation milliseconds.
Note that `%s` in `default_msec_format` is going to be replaced by the representation without milliseconds.

Setting `default_time_format` to `%Y-%m-%dT%H:%M:%S` and `default_msec_format` to `%s.%03d` would result in `2003-07-08T16:49:45.896`.

## Configuration

You can create a formatter instance yourself as in the following, or you can use a logging configuration.

```python
import logging_json

formatter = logging_json.JSONFormatter(fields={
    "level_name": "levelname",
    "thread_name": "threadName",
    "process_name": "processName"
})
```

### Using logging.config.dictConfig

You can configure your logging as advertise by python, by using the `logging.config.dictConfig` function.

#### dict configuration

```python
import logging.config

logging.config.dictConfig({
    "version": 1,
    "formatters": {
        "json": {
            '()': 'logging_json.JSONFormatter',
            'fields':{
                "level_name": "levelname",
                "thread_name": "threadName",
                "process_name": "processName"
            }
        }
    },
    "handlers": {
        "standard_output": {
            'class': 'logging.StreamHandler',
            'formatter': 'json',
            'stream': 'ext://sys.stdout'
        },
    },
    "loggers": {
        "my_app": {"level": "DEBUG"}
    },
    "root": {
        "level": "INFO",
        "handlers": ["standard_output"]
    }
})
```

#### YAML logging configuration

You can use YAML to store your logging configuration, as in the following sample:

```python
import logging.config
import yaml

with open("path/to/logging_configuration.yaml", "r") as config_file:
    logging.config.dictConfig(yaml.load(config_file))
```

Where `logging_configuration.yaml` can be a file containing the following sample:

```yaml
version: 1
formatters:
  json:
    '()': logging_json.JSONFormatter
    fields:
      level_name: levelname
      thread_name: threadName
      process_name: processName
handlers:
  standard_output:
    class: logging.StreamHandler
    formatter: json
    stream: ext://sys.stdout
loggers:
  my_app:
    level: DEBUG
root:
  level: INFO
  handlers: [standard_output]
```

## How to install
1. [python 3.7+](https://www.python.org/downloads/) must be installed
2. Use pip to install module:
```sh
python -m pip install logging_json
```
