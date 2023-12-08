CMAKE_MINIMUM_REQUIRED(VERSION 3.6)

project(helloworld-binding
    VERSION 2.0.0
    DESCRIPTION "Provides a simple API showcasing the basics of binding development"
    HOMEPAGE_URL "https://git.ovh.iot/redpesk/redpesk-samples/helloworld-binding"
    LANGUAGES C CXX
)

# Declare options
option(CPP "Set to true to build the C++ version" OFF)
set(AFM_APP_DIR ${CMAKE_INSTALL_PREFIX}/redpesk CACHE PATH "Applications directory")
set(APP_DIR ${AFM_APP_DIR}/${PROJECT_NAME})

# Check dependencies
include(FindPkgConfig)
pkg_check_modules(deps REQUIRED
    json-c
    afb-binding>=4.1.0
)

# Process option "CPP": use the CPP implementation if true, use the C one if false
if(CPP)
    set(SRC ./src/helloworld.cpp)
else()
    set(SRC ./src/helloworld.c)
endif(CPP)

# Build
add_library(helloworld-binding SHARED ${SRC})
# This version script is a linker script which exports all symbols named "afbBinding*" and makes all the other symbols local only
pkg_get_variable(vscript afb-binding version_script)
if(vscript)
    target_link_options(helloworld-binding PRIVATE -Wl,--version-script=${vscript})
endif(vscript)

# Install
install(TARGETS helloworld-binding DESTINATION ${APP_DIR}/lib)
install(FILES rpconfig/manifest.yml DESTINATION ${APP_DIR}/.rpconfig)
