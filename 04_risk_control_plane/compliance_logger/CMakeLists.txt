cmake_minimum_required(VERSION 3.10)

project(ComplianceLogger LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

add_executable(compliance_logger main.cpp)

# In a real system, this would likely be a static library linked into
# all other components that need to log events.
# add_library(compliance_logger_lib STATIC main.cpp)
