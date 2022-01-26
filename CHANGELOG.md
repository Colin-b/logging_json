# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.2.1] - 2022-01-26
### Fixed
- `datetime`, `time` and `date` instances are now represented following [ISO-8601](https://www.iso.org/iso-8601-date-and-time-format.html) format instead of raising a `TypeError`.
- Default to the `str` representation of value instead of raising a `TypeError` for non-standard python types.

## [0.2.0] - 2021-11-24
### Added
- Added `message_field_name` parameter.

## [0.1.0] - 2021-10-04
### Fixed
- Handle `extra` logging parameter.

## [0.0.1] - 2020-10-15
### Added
- Public release.

[Unreleased]: https://github.com/Colin-b/logging_json/compare/v0.2.1...HEAD
[0.2.1]: https://github.com/Colin-b/logging_json/compare/v0.2.0...v0.2.1
[0.2.0]: https://github.com/Colin-b/logging_json/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/Colin-b/logging_json/compare/v0.0.1...v0.1.0
[0.0.1]: https://github.com/Colin-b/logging_json/releases/tag/v0.0.1
