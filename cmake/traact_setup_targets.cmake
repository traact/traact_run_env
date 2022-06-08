cmake_minimum_required(VERSION 3.16)

include(GenerateExportHeader)
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_VISIBILITY_PRESET hidden)
set(CMAKE_VISIBILITY_INLINES_HIDDEN 1)

message("traact_utils =================================================")

conan_basic_setup(TARGETS)



if (CMAKE_BUILD_TYPE MATCHES Debug)
    add_compile_definitions(SPDLOG_DEBUG_ON SPDLOG_TRACE_ON SPDLOG_ACTIVE_LEVEL=SPDLOG_LEVEL_TRACE)
endif ()

if (CMAKE_CXX_COMPILER_ID STREQUAL "Clang")
    # using Clang
elseif (CMAKE_CXX_COMPILER_ID STREQUAL "GNU")
    # using GCC
    # add_compile_options(-Wall -Wextra -Wshadow -Wnon-virtual-dtor -pedantic -Wcast-align -Wpedantic -Wmisleading-indentation -Wlogical-op -Wnull-dereference)
elseif (CMAKE_CXX_COMPILER_ID STREQUAL "Intel")
    # using Intel C++
elseif (CMAKE_CXX_COMPILER_ID STREQUAL "MSVC")
    # using Visual Studio C++
endif ()




