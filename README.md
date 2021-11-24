<h2 align="center">JSON formatter for logging</h2>

<p align="center">
<a href="https://pypi.org/project/logging_json/"><img alt="pypi version" src="https://img.shields.io/pypi/v/logging_json"></a>
<a href="https://github.com/Colin-b/logging_json/actions"><img alt="Build status" src="https://github.com/Colin-b/logging_json/workflows/Release/badge.svg"></a>
<a href="https://github.com/Colin-b/logging_json/actions"><img alt="Coverage" src="https://img.shields.io/badge/coverage-100%25-brightgreen"></a>
<a href="https://github.com/psf/black"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>
<a href="https://github.com/Colin-b/logging_json/actions"><img alt="Number of tests" src="https://img.shields.io/badge/tests-17 passed-blue"></a>
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

This dictionary will contains 3 keys:
* `type`: The name of the exception class (useful when the message is blank).
* `message`: The str representation of the exception (usually the provided error message).
* `stack`: The stack trace, formatted as a string.

### Logging with a dictionary

This formatter allows you to log dictionary as in the following:

```python
import logging

logging.info({"key": "value", "other key": "other value"})
```

The resulting JSON dictionary will be the one you provided (with the [additional fields](#adding-additional-fields-and-values)).

### Logging with anything else (such as a string)

Anything not logged using a dictionary will be handled by the standard formatter and it can result in one of the 2 output:
* A JSON dictionary, if [additional fields](#adding-additional-fields-and-values) are set or if `extra` parameter is used while logging, with the message available in the `msg` key of the resulting JSON dictionary.
  Default `msg` key name can be changed by `message_field_name` parameter of the `logging_json.JSONFormatter` instance.
* The formatted record, if no [additional fields](#adding-additional-fields-and-values) are set. 

This handles the usual string logging as in the following:

```python
import logging

logging.info("This is my message")
```

## Configuration

You can create a formatter instance yourself as in the following or you can use a logging configuration.

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
1. [python 3.6+](https://www.python.org/downloads/) must be installed
2. Use pip to install module:
```sh
python -m pip install logging_json
```
