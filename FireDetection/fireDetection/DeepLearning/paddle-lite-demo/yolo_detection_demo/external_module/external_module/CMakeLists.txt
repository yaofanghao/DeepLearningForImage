# add_library(Easylog easylogging++.cc)
# target_include_directories(Easylog
#           INTERFACE ${CMAKE_CURRENT_SOURCE_DIR}
#           )
# add_library(barcode_idf barcode_idf.cpp)
# target_include_directories(Easylog
#           INTERFACE ${CMAKE_CURRENT_SOURCE_DIR}
#           )
# target_include_directories(barcode_idf
#           INTERFACE ${CMAKE_CURRENT_SOURCE_DIR}
#           )
add_library(external_module easylogging++.cc)