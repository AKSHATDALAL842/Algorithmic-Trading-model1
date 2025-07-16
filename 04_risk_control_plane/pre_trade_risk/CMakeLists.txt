cmake_minimum_required(VERSION 3.10)

project(PreTradeRisk LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

add_executable(pre_trade_risk main.cpp)

# In a real system, this component would be a library linked into the
# OrderManager, not a separate executable. The logic would be called
# in-line with every order.
