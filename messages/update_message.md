SublimeLinter-gcc has been updated. To see the changelog, visit
Preferences » Package Settings » SublimeLinter-gcc » Changelog


## 1.4.0

- Make sure to update your configuration by pressing Meta+shift+P, <Preferences: SublimeLinter Settings>, and use
gcc : { executable : 'gcc' },
g++ : { executable : 'g++' }
instead of
gcc { c_executable : 'gcc', cpp_executable : 'g++' }