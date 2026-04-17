cmake_minimum_required(VERSION 3.10)
project(task1)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Основная программа
add_executable(main main.cpp TVSet.cpp CommandProcessor.cpp)

# Тесты
add_executable(tests task1_tests.cpp TVSet.cpp CommandProcessor.cpp)