# CMakeLists.txt for building C projects with ALYODCLI
# Usage: cmake . && make

cmake_minimum_required(VERSION 3.10)
project(alyodcli_client C)

set(CMAKE_C_STANDARD 99)
set(CMAKE_C_STANDARD_REQUIRED ON)

# Add platform-specific socket libraries
if(WIN32)
    set(SOCKET_LIBS ws2_32)
else()
    set(SOCKET_LIBS)
endif()

# ALYODCLI Client Library
add_library(alyodcli alyodcli.c)
target_link_libraries(alyodcli PUBLIC ${SOCKET_LIBS})
target_include_directories(alyodcli PUBLIC .)

# Example Client Program
add_executable(example_client example_client.c)
target_link_libraries(example_client PRIVATE alyodcli)

# Installation
install(TARGETS alyodcli LIBRARY DESTINATION lib ARCHIVE DESTINATION lib)
install(FILES alyodcli.h DESTINATION include)

# Optional: Build as shared library
option(BUILD_SHARED_LIBS "Build ALYODCLI as shared library" OFF)

if(BUILD_SHARED_LIBS)
    set_target_properties(alyodcli PROPERTIES POSITION_INDEPENDENT_CODE ON)
endif()

# Compiler optimizations
if(MSVC)
    target_compile_options(alyodcli PRIVATE /O2 /W4)
    target_compile_options(example_client PRIVATE /O2)
else()
    target_compile_options(alyodcli PRIVATE -O3 -Wall -Wextra -pedantic)
    target_compile_options(example_client PRIVATE -O3)
endif()

# Print configuration
message(STATUS "ALYODCLI C Bindings Configuration:")
message(STATUS "  Platform: ${CMAKE_SYSTEM_NAME}")
message(STATUS "  Compiler: ${CMAKE_C_COMPILER}")
message(STATUS "  Build Type: ${CMAKE_BUILD_TYPE}")
message(STATUS "  Socket Libs: ${SOCKET_LIBS}")

# Instructions
add_custom_target(show_build_info ALL
    COMMAND ${CMAKE_COMMAND} -E echo ""
    COMMAND ${CMAKE_COMMAND} -E echo "Build Complete!"
    COMMAND ${CMAKE_COMMAND} -E echo ""
    COMMAND ${CMAKE_COMMAND} -E echo "To use ALYODCLI in your C project:"
    COMMAND ${CMAKE_COMMAND} -E echo "  1. Start the server: alyodcli-server --host 127.0.0.1 --port 5555"
    COMMAND ${CMAKE_COMMAND} -E echo "  2. Link alyodcli library to your project"
    COMMAND ${CMAKE_COMMAND} -E echo "  3. #include \"alyodcli.h\" in your code"
    COMMAND ${CMAKE_COMMAND} -E echo ""
    COMMAND ${CMAKE_COMMAND} -E echo "Run example: ./example_client"
    COMMAND ${CMAKE_COMMAND} -E echo ""
)
