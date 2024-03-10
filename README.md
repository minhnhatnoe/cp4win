# cp4win

cp4win helps you set up common tools used in competitive programming for Windows, such that your next step is coding! It is portable and comprehensive, and is intended for use for setting up contest environments.

Each component is standalone unless otherwise noted, and can be disabled to conform with contests' rulebook.

## Components

### IDE

cp4win supports four most common IDEs, including:

1. Visual Studio Code
2. Sublime Text 4
3. Code::Blocks
4. Dev-C++

### C++ compilers

cp4win recommends installing all of the following C++ compilers for competitive programming:

1. WinLibs GCC 13.2.0 with POSIX threads, LLVM and MinGW-w64, UCRT
    - Contains bugs related to target directives. See [here](https://gcc.gnu.org/bugzilla/show_bug.cgi?id=109753) and [here](https://codeforces.com/blog/entry/118261).
    - Is the latest release and supports newest language features.
2. WinLibs GCC 11.2.0, UCRT
    - Standard GCC of Codeforces, the #1 competitive programming platform. Switched to UCRT because of deficiencies in MSVCRT. See [here](https://codeforces.com/blog/entry/126677) and [here (warning: language)](https://web.archive.org/web/20220702095817/https://erikmcclure.com/blog/windows-malloc-implementation-is-a-trash-fire/).
3. SourceForge GCC 8.1.0, POSIX, seh
    - Commonly used version of GCC. Runs fast on most machines, in contrary to newer versions.
    - MSVCRT to support Windows versions older than 10.

### Python interpreters

Python 3.11

### VSCode extensions

cphelper
pylance, python debugger, python
c++, c++ theme
code runner

### Python packages

gurobi and friends

### Sublime Text build system

### Misc

geogebra

# Use for testing and quick deployment
vscode_ext_urls = {
    "python": [
        "https://marketplace.visualstudio.com/_apis/public/gallery/publishers/ms-python/vsextensions/python/2024.3.10681011/vspackage",
        "https://marketplace.visualstudio.com/_apis/public/gallery/publishers/ms-python/vsextensions/debugpy/2024.3.10661804/vspackage?targetPlatform=win32-x64",
        "https://marketplace.visualstudio.com/_apis/public/gallery/publishers/ms-python/vsextensions/vscode-pylance/2024.2.106/vspackage"
    ],
    "cpp": [
        "https://marketplace.visualstudio.com/_apis/public/gallery/publishers/ms-vscode/vsextensions/cpptools/1.19.6/vspackage?targetPlatform=win32-x64",
        "https://marketplace.visualstudio.com/_apis/public/gallery/publishers/ms-vscode/vsextensions/cpptools-themes/2.0.0/vspackage"
    ],
    "cph": ["https://marketplace.visualstudio.com/_apis/public/gallery/publishers/DivyanshuAgrawal/vsextensions/competitive-programming-helper/6.1.0/vspackage"],
    "runner": ["https://marketplace.visualstudio.com/_apis/public/gallery/publishers/formulahendry/vsextensions/code-runner/0.12.1/vspackage"]
}