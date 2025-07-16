cmake_minimum_required(VERSION 3.10)

project(BookBuilder LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

add_executable(book_builder main.cpp)

# In a real scenario, we would link against a shared ring buffer library
# and an order book library.
# target_link_libraries(book_builder PRIVATE ring_buffer order_book)
