# CMake Build Instructions for Stanford C++ Library

This project now supports CMake build system with automatic Qt downloading and building.

## Features
- Automatically downloads and builds Qt 6.9.0 (no system Qt required)
- Installs library to parent directory (../lib, ../include, ../share)
- Self-contained build with no system dependencies

## Quick Build

```bash
# Simple build with bundled Qt (recommended)
./build.sh
```

## Manual Build

```bash
# Create build directory
mkdir build
cd build

# Configure (this will download Qt automatically)
cmake .. -DCMAKE_BUILD_TYPE=Release

# Build (this will take a while on first run due to Qt compilation)
cmake --build . --parallel

# Install to parent directory
cmake --install .
```

## Build Options

- `BUILD_TESTS`: Build unit tests (default: OFF)
- `BUILD_WELCOME`: Build Welcome program (default: OFF)
- `USE_SYSTEM_QT`: Use system Qt instead of downloading (default: OFF)

Example with options:
```bash
cmake .. -DBUILD_TESTS=ON -DBUILD_WELCOME=ON
```

## Using System Qt (not recommended)

If you already have Qt 6.9+ installed:
```bash
cmake .. -DUSE_SYSTEM_QT=ON
```

## Installation Layout

After installation, files will be in the parent directory:
```
../
├── lib/
│   ├── libcs106.a
│   └── version2025.1
├── include/
│   └── cs106/
│       ├── *.h (all public headers)
└── share/
    └── cs106/
        ├── resources/
        └── stanfordtypes.py
```

## Notes

- First build will download Qt (~800MB) and compile it, which may take 30-60 minutes
- Subsequent builds will be much faster as Qt is cached
- The Qt build is configured with minimal modules to reduce build time
- All dependencies are built statically for maximum portability