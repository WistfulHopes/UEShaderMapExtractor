cmake_minimum_required (VERSION 3.10)
project (decompress_shader)

add_executable (decompress_shader decompress_shader.cpp)

target_sources (decompress_shader PRIVATE lz4.cpp)

target_include_directories (decompress_shader PUBLIC ${CMAKE_CURRENT_SOURCE_DIR} ${CMAKE_CURRENT_SOURCE_DIR}/zlib-1.2.5 ${CMAKE_CURRENT_SOURCE_DIR}/oodle/include)

target_link_libraries (decompress_shader ${CMAKE_CURRENT_SOURCE_DIR}/zlib-1.2.5/Lib/Win64/zlib_64.lib ${CMAKE_CURRENT_SOURCE_DIR}/oodle/lib/Win64/oo2core_win64.lib ${CMAKE_CURRENT_SOURCE_DIR}/zstd-v1.5.6-win64/dll/libzstd.dll.a)