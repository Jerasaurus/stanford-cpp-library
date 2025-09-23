#!/bin/bash

# Build script for Stanford C++ Library with Qt bundled
# This script builds the library and installs it to the parent directory

set -e

echo "Building Stanford C++ Library with bundled Qt..."

# Create build directory
mkdir -p build
cd build

# Configure with CMake
echo "Configuring project..."
cmake .. -DCMAKE_BUILD_TYPE=Release

# Build the project
echo "Building library (this may take a while due to Qt compilation)..."
cmake --build . --parallel $(nproc 2>/dev/null || sysctl -n hw.ncpu 2>/dev/null || echo 4)

# Install to parent directory
echo "Installing library to parent directory..."
cmake --install .

echo "Build complete! Library installed to: $(dirname $(pwd))"
echo "Headers: ../include/cs106"
echo "Library: ../lib/libcs106.a"
echo "Resources: ../share/cs106/"