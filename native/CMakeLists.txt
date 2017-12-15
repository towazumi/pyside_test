cmake_minimum_required(VERSION 3.0)

project(cppmod)

set(PYBIND11_CPP_STANDARD -std=c++14)
set(CMAKE_CXX_FLAGS "-Wall -W4 -O2")
set(CMAKE_CONFIGURATION_TYPES "Debug;Release" )
#set(CMAKE_SUPPRESS_REGENERATION true)

add_subdirectory(${CMAKE_CURRENT_SOURCE_DIR}/../third_party/pybind11 ${CMAKE_CURRENT_BINARY_DIR}/pybind11)

pybind11_add_module(cppmod SHARED cppmod.cpp)  
