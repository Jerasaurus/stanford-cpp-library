# CS106 Library CMake configuration
set(LIBRARY_VERSION 2025.1)

# Gather source files from subdirectories
set(LIB_SUBDIRS collections console graphics io system util testing)

# Collect public headers and sources
set(PUBLIC_HEADERS)
set(SOURCES)

foreach(dir ${LIB_SUBDIRS})
    file(GLOB dir_headers "${CMAKE_CURRENT_SOURCE_DIR}/${dir}/*.h")
    file(GLOB dir_sources "${CMAKE_CURRENT_SOURCE_DIR}/${dir}/*.cpp")
    list(APPEND PUBLIC_HEADERS ${dir_headers})
    list(APPEND SOURCES ${dir_sources})
endforeach()

# Collect private headers and sources
file(GLOB PRIVATE_HEADERS "${CMAKE_CURRENT_SOURCE_DIR}/private/*.h")
file(GLOB PRIVATE_SOURCES "${CMAKE_CURRENT_SOURCE_DIR}/private/*.cpp")

# Create build.h with version info
string(TIMESTAMP BUILD_DATE "%Y-%m-%d %H:%M:%S")
file(WRITE "${CMAKE_CURRENT_BINARY_DIR}/private/build.h"
"#ifndef SPL_BUILD_H
#define SPL_BUILD_H

#define SPL_VERSION \"${LIBRARY_VERSION}\"
#define SPL_BUILD_DATE \"${BUILD_DATE}\"
#define SPL_BUILD_USER \"cmake\"

#endif
")

# Add the generated header to private headers
list(APPEND PRIVATE_HEADERS "${CMAKE_CURRENT_BINARY_DIR}/private/build.h")

# Combine all headers and sources
set(ALL_HEADERS ${PUBLIC_HEADERS} ${PRIVATE_HEADERS})
list(APPEND SOURCES ${PRIVATE_SOURCES})

# Create the static library
add_library(cs106 STATIC ${SOURCES} ${ALL_HEADERS})

# Set library properties
set_target_properties(cs106 PROPERTIES
    VERSION ${LIBRARY_VERSION}
    OUTPUT_NAME cs106
    ARCHIVE_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/lib
)

# Configure include directories
target_include_directories(cs106
    PUBLIC
        $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}>
        $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/collections>
        $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/console>
        $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/graphics>
        $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/io>
        $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/system>
        $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/util>
        $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/testing>
        $<INSTALL_INTERFACE:include>
    PRIVATE
        ${CMAKE_CURRENT_SOURCE_DIR}/private
        ${CMAKE_CURRENT_BINARY_DIR}
)

# Link Qt libraries
target_link_libraries(cs106
    PUBLIC
        Qt6::Core
        Qt6::Gui
        Qt6::Widgets
        Qt6::Network
        Qt6::Multimedia
)

# Platform-specific settings
if(WIN32 OR WIN64)
    target_compile_options(cs106 PRIVATE -fno-ipa-ra)
endif()

# Installation rules - install to parent directory
install(TARGETS cs106
    ARCHIVE DESTINATION lib
    LIBRARY DESTINATION lib
)

# Install public headers
install(FILES ${PUBLIC_HEADERS}
    DESTINATION include/cs106
)

# Install resources
install(DIRECTORY resources/
    DESTINATION share/cs106/resources
    FILES_MATCHING
    PATTERN "*"
)

# Install debug helper
install(FILES stanfordtypes.py
    DESTINATION share/cs106
)

# Create version file
file(WRITE "${CMAKE_CURRENT_BINARY_DIR}/version${LIBRARY_VERSION}" "Stanford C++ Library version ${LIBRARY_VERSION}\n")
install(FILES "${CMAKE_CURRENT_BINARY_DIR}/version${LIBRARY_VERSION}"
    DESTINATION lib
)