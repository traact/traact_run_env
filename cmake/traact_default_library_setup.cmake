cmake_minimum_required(VERSION 3.16)

include(GenerateExportHeader)
set(CMAKE_CXX_STANDARD 17)
#set(CMAKE_CXX_VISIBILITY_PRESET hidden)
#set(CMAKE_VISIBILITY_INLINES_HIDDEN 1)

conan_basic_setup(TARGETS)

option(WITH_TESTS "Build tests" ON)
option(TRACE_LOGS_IN_RELEASE "Build with trace and debug log messages in release" ON)

if (CMAKE_BUILD_TYPE MATCHES Debug OR TRACE_LOGS_IN_RELEASE)
    add_compile_definitions(SPDLOG_DEBUG_ON SPDLOG_TRACE_ON SPDLOG_ACTIVE_LEVEL=SPDLOG_LEVEL_TRACE)
endif ()

if (CMAKE_CXX_COMPILER_ID STREQUAL "Clang")
    # using Clang
elseif (CMAKE_CXX_COMPILER_ID STREQUAL "GNU")
    # using GCC
    #add_compile_options(-fno-gnu-unique)
    # add_compile_options(-Wall -Wextra -Wshadow -Wnon-virtual-dtor -pedantic -Wcast-align -Wpedantic -Wmisleading-indentation -Wlogical-op -Wnull-dereference)
elseif (CMAKE_CXX_COMPILER_ID STREQUAL "Intel")
    # using Intel C++
elseif (CMAKE_CXX_COMPILER_ID STREQUAL "MSVC")
    # using Visual Studio C++
endif ()

# don't set version number so that (linux) only one file exists
#set_target_properties(${CONAN_PACKAGE_NAME} PROPERTIES VERSION ${CONAN_PACKAGE_VERSION})

include(CheckLanguage)
check_language(CUDA)
enable_language(CUDA)
if(NOT DEFINED CMAKE_CUDA_ARCHITECTURES)
    set(CMAKE_CUDA_ARCHITECTURES 75)
endif()

if(NOT DEFINED CMAKE_CUDA_STANDARD)
    set(CMAKE_CUDA_STANDARD 17)
    set(CMAKE_CUDA_STANDARD_REQUIRED ON)
endif()