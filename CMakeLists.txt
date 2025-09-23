cmake_minimum_required(VERSION 3.20)
project(StanfordCPPLib VERSION 2025.1)

# Set C++ standard
set(CMAKE_CXX_STANDARD 11)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Options
option(BUILD_TESTS "Build unit tests" OFF)
option(BUILD_WELCOME "Build Welcome program" OFF)

# Installation prefix - one directory up from source
get_filename_component(PARENT_DIR "${CMAKE_SOURCE_DIR}" DIRECTORY)
set(CMAKE_INSTALL_PREFIX "${PARENT_DIR}" CACHE PATH "Installation prefix" FORCE)

# Set Qt path to the already-built Qt in build/qt-install
set(CMAKE_PREFIX_PATH "${CMAKE_BINARY_DIR}/qt-install" CACHE PATH "Qt installation path")

# Find Qt packages
find_package(Qt6 REQUIRED COMPONENTS Core Gui Widgets Network Multimedia)

# Enable Qt MOC, RCC, UIC
set(CMAKE_AUTOMOC ON)
set(CMAKE_AUTORCC ON)
set(CMAKE_AUTOUIC ON)

# Add library subdirectory
add_subdirectory(Library)

# Optionally build tests
if(BUILD_TESTS)
    add_subdirectory(SPL-unit-tests)
endif()

# Optionally build Welcome program
if(BUILD_WELCOME)
    add_subdirectory(Welcome)
endif()