SublimeLinter-gcc
=================

This linter plugin for [SublimeLinter](https://github.com/SublimeLinter/SublimeLinter) provides an interface to [gcc](https://gcc.gnu.org/) or other gcc-like (cross-)compiler.
It will be used with files that have the C/C++ syntax.
If you are using [clang](https://clang.llvm.org), you may want to check [SublimeLinter-clang](https://github.com/SublimeLinter/SublimeLinter-clang).


Installation
============

SublimeLinter must be installed in order to use this plugin.
If SublimeLinter is not installed, please follow the instructions
[here](http://sublimelinter.readthedocs.org/en/latest/installation.html).


Linter installation
-------------------

Before using this plugin, you must ensure that `gcc` or other gcc-like (cross-)compiler is installed on your system.

You may install `gcc` with the following method:

- Mac OS X: [OSX GCC Installer](https://github.com/kennethreitz/osx-gcc-installer)
- Linux: `gcc` could be installed by using most package managers.
- Windows: [MinGW-w64](https://sourceforge.net/projects/mingw-w64)

Once `gcc` is installed, you must ensure it is in your system PATH so that SublimeLinter can find it.
This may not be as straightforward as you think, so please read [How linter executables are located](http://sublimelinter.readthedocs.org/en/latest/usage.html#how-linter-executables-are-located) in the documentation.


Plugin installation
-------------------

Please use [Package Control](https://sublime.wbond.net/installation) to install the linter plugin.
This will ensure that the plugin will be updated when new versions are available.
If you want to install from source so you can modify the source code,
you probably know what you are doing so we won't cover that here.

To install via Package Control, do the following:

1. Within Sublime Text, bring up the [Command Palette](http://docs.sublimetext.info/en/sublime-text-3/extensibility/command_palette.html) and type `install`.
   Among the commands you should see `Package Control: Install Package`.
   If that command is not highlighted, use the keyboard or mouse to select it.
   There will be a pause of a few seconds while Package Control fetches the list of available plugins.

1. When the plugin list appears, type `gcc`. Among the entries you should see `SublimeLinter-gcc`.
   If that entry is not highlighted, use the keyboard or mouse to select it.


Settings
========

For general information on how SublimeLinter works with settings, please see [Settings](http://sublimelinter.readthedocs.org/en/latest/settings.html).
For information on generic linter settings, please see [Linter Settings](http://sublimelinter.readthedocs.org/en/latest/linter_settings.html).

In addition to the standard SublimeLinter settings, SublimeLinter-gcc provides its own settings.

| Setting | Description |
| :------ | :---------- |
| executable | If you are not using `gcc`, you have to set this to your compiler binary. (like `arm-none-eabi-gcc`) |
| include_dirs | A list of directories to be added to the header search paths (`-I` is not needed). |
| extra_flags | A list of extra flags to pass to the compiler. These should be used carefully, as they may cause linting to fail. |

- All settings above could be `C` or `C++` specific as well.
  To do that, simply add `c_` or `c++_` prefix to a setting's key.

- For project-specific settings, `${project_folder}` can be used to specify relative path.

Here is an example settings:

```javascript
{
    "linters":
    {
        "gcc": {
            "disable": false,
            // C-specific settings
            "c_executable": "gcc",
            "c_extra_flags": [
                "-fsyntax-only",
                "-std=c90",
            ],
            // C++-specific settings
            "c++_executable": "g++",
            "c++_extra_flags": [
                "-fsyntax-only",
                "-std=c++11",
            ],
            // include_dirs for both C and C++
            "include_dirs": [
                "${project_folder}/include",
                "/usr/local/include",
            ],
        },
    },
}
```


Notes
=====

- [Here](https://gcc.gnu.org/onlinedocs/gcc-7.3.0/gcc/Warning-Options.html#Warning-Options)
  is the official list of warning options in gcc 7.3.0. I prefer turn on all warnings
  via `-Wall` (this is default for this plugin) and then suppress unwanted warnings via `-Wno-` prefix.

- Flag `-fsyntax-only` gives a much faster syntax-only checking but
  [some warnings](https://github.com/SublimeLinter/SublimeLinter-gcc/issues/4)
  which are emitted in the code optimization phase would not be caught.


Demo
====

![linting_example](https://raw.githubusercontent.com/SublimeLinter/SublimeLinter-gcc/gh-pages/images/linting_example_sl4.png)


Troubleshooting
===============

C/C++ linting is not always straightforward.
A few things to try when there's (almost) no linting information available:

- Try to compile from the command line, and verify it works.
- The linter might be missing some header files. They can be added with `include_dirs`.
- Sometimes gcc fails to locate the C/C++ standard library headers.

Assuming the compilation works when executed via command line, try to compile with `g++ -v`.
This will display all of the hidden flags that gcc uses.
As a last resort, they can all be added in `extra_flags`.


Contributing
============

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
- Vertical whitespace helps readability, don’t be afraid to use it.
- Please use descriptive variable names, no abbreviations unless they are very well known.

Thank you for helping out!


Supporters <a href="https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=ATXYY9Y78EQ3Y" target="_blank"><img src="https://www.paypalobjects.com/en_US/i/btn/btn_donate_LG.gif" /></a>
==========

Thank you guys for sending me some cups of coffee.
