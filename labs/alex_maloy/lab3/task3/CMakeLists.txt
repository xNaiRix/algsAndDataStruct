cmake_minimum_required(VERSION 3.15)
project(EconomySimulation CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Include directories
include_directories(${CMAKE_CURRENT_SOURCE_DIR}/src)

# Source files for main library
set(LIBRARY_SOURCES
    src/bank.cpp
    src/actors.cpp
    src/economy.cpp
)

# Header files
set(LIBRARY_HEADERS
    src/bank.hpp
    src/actors.hpp
    src/economy.hpp
)

# Main executable
add_executable(economy src/main.cpp ${LIBRARY_SOURCES} ${LIBRARY_HEADERS})

# Tests executable
add_executable(tests src/tests.cpp ${LIBRARY_SOURCES} ${LIBRARY_HEADERS})

# Enable testing
enable_testing()
add_test(NAME BankTests COMMAND tests)
