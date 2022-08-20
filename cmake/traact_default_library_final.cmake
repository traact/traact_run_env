

generate_export_header(${CONAN_PACKAGE_NAME} EXPORT_FILE_NAME ${CMAKE_BINARY_DIR}/traact/${CONAN_PACKAGE_NAME}_export.h)

target_include_directories(${CONAN_PACKAGE_NAME} INTERFACE
        $<BUILD_INTERFACE:${CMAKE_BINARY_DIR}>
        PRIVATE
        ${CMAKE_CURRENT_SOURCE_DIR}/src
        )

target_include_directories(${CONAN_PACKAGE_NAME} PUBLIC
        ${CMAKE_CUDA_TOOLKIT_INCLUDE_DIRECTORIES}
        )
if(NOT CUDA_ARCHITECTURES)
    set_property(TARGET ${cuda_example} PROPERTY CUDA_ARCHITECTURES OFF)
endif()
set_target_properties(${CONAN_PACKAGE_NAME} PROPERTIES
        CUDA_SEPARABLE_COMPILATION ON)

target_compile_options(
        ${CONAN_PACKAGE_NAME}
        BEFORE
        INTERFACE
        $<$<COMPILE_LANGUAGE:CUDA>:--extended-lambda -Xcompiler=-Wall,-Wextra,-Wfatal-errors>
)

install(TARGETS ${CONAN_PACKAGE_NAME}
        ARCHIVE DESTINATION ${CMAKE_INSTALL_LIBDIR}
        LIBRARY DESTINATION ${CMAKE_INSTALL_LIBDIR}
        RUNTIME DESTINATION ${CMAKE_INSTALL_BINDIR}
        )