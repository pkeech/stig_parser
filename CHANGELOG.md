# CHANGELOG
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2020-09-24

### Added 

* Initial Release of STIG Parser

## [1.0.1] - 2020-12-31

### Added

* Updated logic to handle parsing of new STIG schema. Resolved Issue [#3](https://github.com/pkeech/stig_parser/issues/3).


## [1.0.2] - 2021-06-14

### Added

* Updated README
* Additional fields to final JSON object;
    * Release Info
    * Source
    * Notice
    * Classification
    * CCI Number
    * STIG ID
    * Rule ID

## [1.1.0] - 2021-06-14

### Added

* Included `generate-ckl` function to generate a blank checklist (ckl) based upon the STIG passed to it.

### Changed

* Applied Standards to Variable Names
* 
