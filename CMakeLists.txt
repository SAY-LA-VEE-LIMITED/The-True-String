cmake_minimum_required(VERSION 3.14)
project(spectral_t LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Core library
add_library(spectral_t src/spectral_t.cpp)
target_include_directories(spectral_t PUBLIC include)

# Example executable
add_executable(spectral_t_demo src/spectral_t.cpp)
target_link_libraries(spectral_t_demo PRIVATE spectral_t)

# Tests
enable_testing()
add_executable(test_spectral_t tests/test_spectral_t.cpp)
target_link_libraries(test_spectral_t PRIVATE spectral_t)
add_test(NAME spectral_t_test COMMAND test_spectral_t)
