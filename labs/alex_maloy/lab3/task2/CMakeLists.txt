cmake_minimum_required(VERSION 3.20)
project(Calculator)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Add executable for main
add_executable(calculator main.cpp Calculator.cpp Variable.cpp Function.cpp)

# Add executable for tests
add_executable(tests tests.cpp Calculator.cpp Variable.cpp Function.cpp)

# Include directories
target_include_directories(calculator PRIVATE .)
target_include_directories(tests PRIVATE .)