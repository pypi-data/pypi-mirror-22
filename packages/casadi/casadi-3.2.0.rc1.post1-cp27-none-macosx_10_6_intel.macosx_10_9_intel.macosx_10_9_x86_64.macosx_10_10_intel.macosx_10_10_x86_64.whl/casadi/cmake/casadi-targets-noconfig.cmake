#----------------------------------------------------------------
# Generated CMake target import file.
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "casadi" for configuration ""
set_property(TARGET casadi APPEND PROPERTY IMPORTED_CONFIGURATIONS NOCONFIG)
set_target_properties(casadi PROPERTIES
  IMPORTED_LOCATION_NOCONFIG "/Users/travis/build/casadi/binaries/casadi/python_install/casadi/libcasadi.3.3.dylib"
  IMPORTED_SONAME_NOCONFIG "@rpath/libcasadi.3.3.dylib"
  )

list(APPEND _IMPORT_CHECK_TARGETS casadi )
list(APPEND _IMPORT_CHECK_FILES_FOR_casadi "/Users/travis/build/casadi/binaries/casadi/python_install/casadi/libcasadi.3.3.dylib" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)
