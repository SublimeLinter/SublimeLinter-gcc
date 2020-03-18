# SublimeLinter-gcc

[![Package Control](https://img.shields.io/packagecontrol/dt/SublimeLinter-gcc)](https://packagecontrol.io/packages/SublimeLinter-gcc)
[![GitHub tag (latest SemVer)](https://img.shields.io/github/tag/SublimeLinter/SublimeLinter-gcc?logo=github)](https://github.com/SublimeLinter/SublimeLinter-gcc/tags)
[![Project license](https://img.shields.io/github/license/SublimeLinter/SublimeLinter-gcc?logo=github)](https://github.com/SublimeLinter/SublimeLinter-gcc/blob/master/LICENSE)
[![GitHub stars](https://img.shields.io/github/stars/SublimeLinter/SublimeLinter-gcc?logo=github)](https://github.com/SublimeLinter/SublimeLinter-gcc/stargazers)
[![Donate to this project using Paypal](https://img.shields.io/badge/paypal-donate-blue.svg?logo=paypal)](https://www.paypal.me/SublimeLinter/5usd)

This linter plugin for [SublimeLinter](https://github.com/SublimeLinter/SublimeLinter)
provides an interface to [gcc](https://gcc.gnu.org/) or other gcc-like (cross-)compiler.
It will be used with files that have the C/C++ syntax.
If you are using [clang](https://clang.llvm.org), you may want to check
[SublimeLinter-clang](https://github.com/SublimeLinter/SublimeLinter-clang).


## Installation

SublimeLinter must be installed in order to use this plugin.
If SublimeLinter is not installed, please follow the instructions
[here](https://sublimelinter.readthedocs.org/en/stable/installation.html).


### Linter installation

Before using this plugin, you must ensure that `gcc` or other gcc-like compiler is installed on your system.

You may install `gcc` with the following method:

- Mac OS X: [OSX GCC Installer](https://github.com/kennethreitz/osx-gcc-installer)
- Linux: `gcc` could be installed by using most package managers.
- Windows: [MinGW-w64](https://sourceforge.net/projects/mingw-w64)

Once `gcc` is installed, you must ensure it is in your system PATH so that SublimeLinter can find it.
This may not be as straightforward as you think, so please read [Debugging PATH problems](https://sublimelinter.readthedocs.org/en/stable/troubleshooting.html#debugging-path-problems) in the documentation.


### Plugin installation

Please use [Package Control](https://sublime.wbond.net/installation) to install the linter plugin.
This will ensure that the plugin will be updated when new versions are available.
If you want to install from source so you can modify the source code,
you probably know what you are doing so we won't cover that here.

To install via Package Control, do the following:

1. Within Sublime Text, bring up the `Command Palette` by <kbd>Ctrl + Shift + P</kbd> and type `install`.
   Among the commands you should see `Package Control: Install Package`.
   If that command is not highlighted, use the keyboard or mouse to select it.
   There will be a pause of a few seconds while Package Control fetches the list of available plugins.

1. When the plugin list appears, type `gcc`. Among the entries you should see `SublimeLinter-gcc`.
   If that entry is not highlighted, use the keyboard or mouse to select it.


## Settings

Here are some most frequently used custom settings.

| Setting | Description |
| :------ | :---------- |
| executable | The compiler's binary path. This is `["gcc"]` or `["g++"]` by default. If you are not using them, you have to set this to your compiler binary such as `["arm-none-eabi-gcc"]`. |
| I | A list of directories to be added to the header's searching paths. I.e., paths for `-I` flags. |
| args | A list of extra flags to be passed to the compiler. These should be used carefully as they may cause linting to fail. |


Here is an example settings:

```javascript
{
    "linters":
    {
        "gcc": {
            "disable": false,
            "executable": ["gcc"],
            "args": ["-fsyntax-only", "-std=c90"],
            "I": [
                "${file_path}/include",
                "${folder}/include",
                "/usr/local/include",
            ],
            "excludes": [],
        },
        "g++": {
            "disable": false,
            "executable": ["g++"],
            "args": ["-fsyntax-only", "-std=c++17"],
            "I": [
                "${file_path}/include",
                "${folder}/include",
                "/usr/local/include",
            ],
            "excludes": [],
        },
    },
}
```

Here are some useful docs for SublimeLinter settings.

- [General information on how SublimeLinter works with settings](https://sublimelinter.readthedocs.org/en/stable/settings.html).
- [Variables that can be used in settings](https://sublimelinter.readthedocs.org/en/stable/settings.html#settings-expansion).
- [Information on generic linter settings](https://sublimelinter.readthedocs.org/en/stable/linter_settings.html).


## Notes

- [Here](https://gcc.gnu.org/onlinedocs/gcc-9.3.0/gcc/Warning-Options.html#Warning-Options)
  is the official list of warning options in gcc 9.3.0. I prefer turn on all warnings
  via `-Wall` (this is default for this plugin) and then suppress unwanted warnings via `-Wno-` prefix.

- Use the `-fsyntax-only` flag in `args` gives a much faster syntax-only checking but
  [some warnings](https://github.com/SublimeLinter/SublimeLinter-gcc/issues/4)
  which are emitted in the code optimization phase would not be caught.


## Demo

![linting_example](https://raw.githubusercontent.com/SublimeLinter/SublimeLinter-gcc/gh-pages/images/linting_example_sl4.png)


## Troubleshooting

C/C++ linting is not always straightforward.
A few things to try when there's (almost) no linting information available:

- Try to compile from the command line, and verify it works.
- The linter might be missing some header files. They can be added with settings `I`.
- Sometimes gcc fails to locate the C/C++ standard library headers.

Assuming the compilation works when executed via command line, try to compile with `g++ -v`.
This will display all of the hidden flags that gcc uses.
As a last resort, they can all be added in settings `args`.


## Contributing

If you would like to contribute enhancements or fixes, please do the following:

1. Fork the plugin repository.
1. Hack on a separate topic branch created from the latest `master`.
1. Commit and push the topic branch.
1. Make sure your modification could pass unittests.
1. Make a pull request.
1. Be patient.

Please note that modifications should follow these coding guidelines:

- Indent is 4 spaces.
- Code should pass flake8 and pep257 linters.
- Probably format codes with [black](https://github.com/psf/black) code formatter.
- Vertical whitespace helps readability, don’t be afraid to use it.
- Please use descriptive variable names, no abbreviations unless they are very well known.

Thank you for helping out!
