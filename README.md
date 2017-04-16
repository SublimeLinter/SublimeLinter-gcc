SublimeLinter-contrib-gcc
=========================

This linter plugin for [SublimeLinter](https://github.com/SublimeLinter/SublimeLinter3) provides an interface to [gcc](https://gcc.gnu.org/).
It will be used with files that have the C/C++ syntax.
If you are using [clang](https://clang.llvm.org), you should consider [Sublime​Linter-contrib-clang](https://github.com/nirm03/SublimeLinter-clang).


Installation
============

SublimeLinter 3 must be installed in order to use this plugin.
If SublimeLinter 3 is not installed, please follow the instructions [here](http://sublimelinter.readthedocs.org/en/latest/installation.html).


### Linter installation

Before using this plugin, you must ensure that `gcc` is installed on your system.

You may install `gcc` with the following method:

- Mac OS X: [OSX GCC Installer](https://github.com/kennethreitz/osx-gcc-installer)
- Linux: `gcc` could be installed by using most package managers.
- Windows: [MinGW-w64](https://sourceforge.net/projects/mingw-w64)

Once `gcc` is installed, you must ensure it is in your system PATH so that SublimeLinter can find it.
This may not be as straightforward as you think,
so please read [How linter executables are located](http://sublimelinter.readthedocs.org/en/latest/usage.html#how-linter-executables-are-located) in the documentation.

Once you have installed `gcc` you can proceed to install the `SublimeLinter-contrib-gcc` plugin if it is not yet installed.


## Plugin installation

Please use [Package Control](https://sublime.wbond.net/installation) to install the linter plugin.
This will ensure that the plugin will be updated when new versions are available.
If you want to install from source so you can modify the source code, you probably know what you are doing so we won't cover that here.

To install via Package Control, do the following:

1. Within Sublime Text, bring up the [Command Palette](http://docs.sublimetext.info/en/sublime-text-3/extensibility/command_palette.html) and type `install`.
   Among the commands you should see `Package Control: Install Package`.
   If that command is not highlighted, use the keyboard or mouse to select it.
   There will be a pause of a few seconds while Package Control fetches the list of available plugins.

1. When the plugin list appears, type `gcc`. Among the entries you should see `SublimeLinter-contrib-gcc`.
   If that entry is not highlighted, use the keyboard or mouse to select it.


Settings
========

For general information on how SublimeLinter works with settings, please see [Settings](http://sublimelinter.readthedocs.org/en/latest/settings.html).
For information on generic linter settings, please see [Linter Settings](http://sublimelinter.readthedocs.org/en/latest/linter_settings.html).

In addition to the standard SublimeLinter settings, SublimeLinter-contrib-gcc provides its own settings.

| Setting | Description |
| :------ | :---------- |
| include_dirs | A list of directories to be added to the header search paths (`-I` is not needed). |
| extra_flags | A string with extra flags to pass to gcc. These should be used carefully, as they may cause linting to fail. |

In project-specific settings, `$project_folder` or `${project_folder}` can be used to specify relative path.
```javascript
"SublimeLinter":
{
    "linters":
    {
        "gcc": {
            "extra_flags": "-Wall -std=c++11 -I${project_folder}/foo",
            "include_dirs": [
                "${project_folder}/3rdparty/bar/include",
                "${project_folder}/3rdparty/baz"
            ]
        }
    }
},
```


Demo
====

![linting_example](https://raw.githubusercontent.com/jfcherng/SublimeLinter-contrib-gcc/gh-pages/images/linting_example.png)


Troubleshooting
===============

C/C++ linting is not always straightforward.
A few things to try when there's (almost) no linting information available:

- Try to compile from the command line, and verify it works.
- The linter might be missing some header files. They can be added with `include_dirs`.
- Sometimes gcc fails to locate the C/C++ standard library headers.

Assuming the compilation works when executed via command line, try to compile with `g++ -v`.
This will display all of the hidden flags that gcc uses.
As a last resort, they can all be added as `extra_flags`.


Contributing
============

If you would like to contribute enhancements or fixes, please do the following:

1. Fork the plugin repository.
1. Hack on a separate topic branch created from the latest `master`.
1. Commit and push the topic branch.
1. Make a pull request.
1. Be patient.  ;-)

Please note that modifications should follow these coding guidelines:

- Indent is 4 spaces.
- Code should pass flake8 and pep257 linters.
- Vertical whitespace helps readability, don’t be afraid to use it.
- Please use descriptive variable names, no abbrevations unless they are very well known.

Thank you for helping out!


License
=======

The MIT License (MIT)

Copyright (c) 2017 Jack Cherng

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.


Supporters <a href="https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=ATXYY9Y78EQ3Y" target="_blank"><img src="https://www.paypalobjects.com/en_US/i/btn/btn_donate_LG.gif" /></a>
==========

Thank you guys for sending me some cups of coffee.
