# Change Log

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/)
and this project adheres to [Semantic Versioning](http://semver.org/).

## [Unreleased](https://github.com/python-social-auth/social-storage-sqlalchemy/commits/master)

## [1.1.0](https://github.com/python-social-auth/social-storage-sqlalchemy/releases/tag/1.1.0) - 2017-05-06

### Changed
- Fixed `SQLAlchemyUserMixin.extra_data` not saving updated values (Issue #2)

## [1.0.1](https://github.com/python-social-auth/social-storage-sqlalchemy/releases/tag/1.0.1) - 2017-01-29

### Changed
- Fixed partial instance deletion

## [1.0.0](https://github.com/python-social-auth/social-storage-sqlalchemy/releases/tag/1.0.0) - 2017-01-22

### Added
- Added partial pipeline db storage solution

### Changed
- Fixed the JSON pickler implementation to complain SQLAlchemy
  invocation of the `dumps` method

## [0.0.1](https://github.com/python-social-auth/social-storage-sqlalchemy/releases/tag/0.0.1) - 2016-11-27

### Changed

- Split from the monolitic [python-social-auth](https://github.com/omab/python-social-auth)
  codebase
