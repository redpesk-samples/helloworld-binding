CMAKE_MINIMUM_REQUIRED(VERSION 3.10)

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

# generation of compiled version of info
set(infoj ${CMAKE_SOURCE_DIR}/src/info_verb.json)
set(infoc ${CMAKE_BINARY_DIR}/info_verb.c)
add_custom_command(
    OUTPUT ${infoc}
    COMMAND echo "const char *info_verb_json = " > ${infoc}
    COMMAND sed 's/\"/\\\\\"/g\;s/^[ \t]*/&\"/\;s/[ \t]*$$/\"/' ${infoj} >> ${infoc}
    COMMAND echo '\;' >> ${infoc}
    DEPENDS ${infoj}
)

# Process option "CPP": use the CPP implementation if true, use the C one if false
if(CPP)
    set(SRC ./src/helloworld.cpp)
else()
    set(SRC ./src/helloworld.c)
endif(CPP)

# Specify the directory for .gcno and .gcda
set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} --coverage -fprofile-dir=/usr/libexec/redtest/${PROJECT_NAME}")
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} --coverage -fprofile-dir=/usr/libexec/redtest/${PROJECT_NAME}")


add_library(helloworld-binding SHARED ${SRC} ${infoc})
target_compile_options(helloworld-binding PRIVATE ${deps_CFLAGS})
target_link_libraries(helloworld-binding ${deps_LDFLAGS})
set_target_properties(helloworld-binding PROPERTIES PREFIX "")


# This version script is a linker script which exports all symbols named "afbBinding*" and makes all the other symbols local only
pkg_get_variable(vscript afb-binding version_script)
if(vscript)
    target_link_options(helloworld-binding PRIVATE -Wl,--version-script=${vscript})
endif(vscript)


# Install
install(TARGETS helloworld-binding DESTINATION ${APP_DIR}/lib)
install(FILES rpconfig/manifest.yml DESTINATION ${APP_DIR}/.rpconfig)
install(PROGRAMS ${CMAKE_SOURCE_DIR}/redtest/run-redtest
	DESTINATION /usr/libexec/redtest/${PROJECT_NAME}/)
install(FILES ${CMAKE_SOURCE_DIR}/tests/tests.py
    DESTINATION /usr/libexec/redtest/${PROJECT_NAME}/)
