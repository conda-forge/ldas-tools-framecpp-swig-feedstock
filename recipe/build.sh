#!/bin/bash

mkdir -p _build
pushd _build

# configure
cmake \
  ${CMAKE_ARGS} \
  -DCMAKE_OSX_ARCHITECTURES:STRING="${OSX_ARCH}" \
  -DENABLE_SWIG_PYTHON2:BOOL=no \
  -DENABLE_SWIG_PYTHON3:BOOL=no \
  ${SRC_DIR} \
;

# build
cmake --build . --parallel ${CPU_COUNT} --verbose

# test
if [[ "${CONDA_BUILD_CROSS_COMPILATION:-}" != "1" || "${CROSSCOMPILING_EMULATOR}" != "" ]]; then
  ctest --parallel ${CPU_COUNT} --verbose
fi

# install
cmake --build . --parallel ${CPU_COUNT} --verbose --target install
