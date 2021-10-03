#!/bin/bash

mkdir -p _build
pushd _build

# configure
cmake \
	${SRC_DIR} \
	${CMAKE_ARGS} \
	-DCMAKE_BUILD_TYPE:STRING=Release \
	-DENABLE_SWIG_PYTHON2:BOOL=no \
	-DENABLE_SWIG_PYTHON3:BOOL=no \
;

# build
cmake --build . --parallel ${CPU_COUNT} --verbose

# test
if [[ "${CONDA_BUILD_CROSS_COMPILATION:-}" != "1" ]]; then
	ctest --parallel ${CPU_COUNT} --verbose
fi

# install
cmake --build . --parallel ${CPU_COUNT} --verbose --target install
