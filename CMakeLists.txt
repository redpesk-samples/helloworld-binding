CMAKE_MINIMUM_REQUIRED(VERSION 3.6)

project(helloworld-binding)

if(CPP)
    add_library(helloworld-binding SHARED ./src/helloworld.cpp)
else()
    add_library(helloworld-binding SHARED ./src/helloworld.c)
endif(CPP)
unset(CPP)

include(FindPkgConfig)
pkg_check_modules(deps REQUIRED
    json-c
    afb-binding>=4.1.0
)

pkg_get_variable(vscript afb-binding version_script)
if(vscript)
    target_link_options(helloworld-binding PRIVATE -Wl,--version-script=${vscript})
endif(vscript)
