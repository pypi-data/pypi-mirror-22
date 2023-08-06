#----------------------------------------------------------------
# Generated CMake target import file.
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "casadi" for configuration ""
set_property(TARGET casadi APPEND PROPERTY IMPORTED_CONFIGURATIONS NOCONFIG)
set_target_properties(casadi PROPERTIES
  IMPORTED_LINK_INTERFACE_LIBRARIES_NOCONFIG "dl"
  IMPORTED_LOCATION_NOCONFIG "/home/travis/build/casadi/binaries/casadi/python_install/casadi/libcasadi.so"
  IMPORTED_SONAME_NOCONFIG "libcasadi.so"
  )

list(APPEND _IMPORT_CHECK_TARGETS casadi )
list(APPEND _IMPORT_CHECK_FILES_FOR_casadi "/home/travis/build/casadi/binaries/casadi/python_install/casadi/libcasadi.so" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)
