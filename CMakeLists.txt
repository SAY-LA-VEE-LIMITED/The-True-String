cmake_minimum_required(VERSION 3.14)
project(spectral_t LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Executable from top-level spectral_t.cpp (contains main)
add_executable(spectral_t spectral_t.cpp)

# Executable from src/prime_spectrum.cpp (simple T generator)
add_executable(prime_spectrum src/prime_spectrum.cpp)

# Enable testing (no tests currently defined)
enable_testing()
