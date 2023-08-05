# Change Log
## 2.0.1 - 2017-05-17
### Changed
- Fixes `--help`. 

## 2.0.0 - 2017-05-15
### Changed
- Prints help if no arguments are given.
- Moves the responsibility of getting variables from GitLab away from the wrapper (changes signature of `run_wrapped`).
- Removes merging of `--env-file` as Docker supports multiple `env-file` arguments. 

## 1.0.0 - 2017-05-12
### Added
- Ability to run Docker interactively.

## 0.1.2 - 2017-05-12
### Changed
- Further Improved documentation.
- Stops wrapper interfering with `docker exec`.

## 0.1.1 - 2017-05-12
### Changed
- Improved documentation.

## 0.1.0 - 2017-05-12
### Added
- First stable release/
