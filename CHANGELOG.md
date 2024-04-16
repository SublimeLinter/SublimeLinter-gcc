# SublimeLinter-gcc


## 2.0.1

No changes. Just to annotate that this is the last version for Sublime Text 3.
The next release will only run in Sublime Text 4 (or later) with its Python 3.8 plugin host.

## 2.0.0

This is a BC break version. Please read the new settings format from the
[README](https://github.com/SublimeLinter/SublimeLinter-gcc/blob/2.0.0/README.md#settings).

- `gcc` and `g++` are separated into two linters.
- Drop support for SublimeLinter 3.
- Adapt SublimeLinter 4 APIs and settings.


## 1.3.9

- Fix a typo.


## 1.3.8

- SublimeLinter 4.3.1 compatible.


## 1.3.7

- Automatically append the directory of the current file to the include directory.


## 1.3.5

- Change package names from `SublimeLinter-contrib-gcc` to `SublimeLinter-gcc`.


## 1.3.4

- Fix SublimeLinter version checking.


## 1.3.3

- Fix typos.


## 1.3.2

- Get SublimeLinter's version number via SublimeLinter 4 API.


## 1.3.1

- Allow `extra_flags` to be a list.


## 1.3.0

- Compatible with SublimeLinter 4.


## 1.2.2

- Remove `-fsyntax-only` from common flags.
  See https://github.com/jfcherng/SublimeLinter-contrib-gcc/issues/4 for details.


## 1.2.1

- Fix `col` is not always presented in `gcc` output.


## 1.2.0

- Add `C` or `C++` specific settings.


## 1.1.0

- Add a new setting: `executable`.


## 1.0.1

- Fix linting of unsaved files.


## 1.0.0

- Initial release.
