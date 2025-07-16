cmake_minimum_required(VERSION 3.10)

project(OrderManager LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

add_executable(order_manager main.cpp)

# In a real system, this would link against libraries for FIX protocol encoding
# and network communication.
# target_link_libraries(order_manager PRIVATE fix_encoder network_client)
