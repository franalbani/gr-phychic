INCLUDE(FindPkgConfig)
PKG_CHECK_MODULES(PC_PHYCHIC phychic)

FIND_PATH(
    PHYCHIC_INCLUDE_DIRS
    NAMES phychic/api.h
    HINTS $ENV{PHYCHIC_DIR}/include
        ${PC_PHYCHIC_INCLUDEDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/include
          /usr/local/include
          /usr/include
)

FIND_LIBRARY(
    PHYCHIC_LIBRARIES
    NAMES gnuradio-phychic
    HINTS $ENV{PHYCHIC_DIR}/lib
        ${PC_PHYCHIC_LIBDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/lib
          ${CMAKE_INSTALL_PREFIX}/lib64
          /usr/local/lib
          /usr/local/lib64
          /usr/lib
          /usr/lib64
)

INCLUDE(FindPackageHandleStandardArgs)
FIND_PACKAGE_HANDLE_STANDARD_ARGS(PHYCHIC DEFAULT_MSG PHYCHIC_LIBRARIES PHYCHIC_INCLUDE_DIRS)
MARK_AS_ADVANCED(PHYCHIC_LIBRARIES PHYCHIC_INCLUDE_DIRS)

