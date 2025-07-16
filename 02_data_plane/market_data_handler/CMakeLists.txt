cmake_minimum_required(VERSION 3.10)

project(MarketDataHandler LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

add_executable(market_data_handler main.cpp)

# In a real scenario, we would link against the Solarflare Onload library
# and a shared ring buffer library.
# target_link_libraries(market_data_handler PRIVATE onload ring_buffer)
