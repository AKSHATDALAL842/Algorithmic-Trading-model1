cmake_minimum_required(VERSION 3.10)

project(HFTSystem LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Add subdirectories for each C++ component. CMake will find the
# CMakeLists.txt in each of these directories and build them.

# Pillar 2: Data Plane
# add_subdirectory(02_data_plane/market_data_handler)
add_subdirectory(02_data_plane/book_builder)

# Pillar 3: Execution Plane
# add_subdirectory(03_execution_plane/order_manager)

# Pillar 4: Risk & Control Plane
# add_subdirectory(04_risk_control_plane/pre_trade_risk)
# add_subdirectory(04_risk_control_plane/compliance_logger)

