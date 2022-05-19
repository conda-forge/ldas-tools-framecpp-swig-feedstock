#!/bin/bash

set -ex
mkdir -p _build
pushd _build

# configure
cmake \
	${SRC_DIR} \
	${CMAKE_ARGS} \
	-DCMAKE_BUILD_TYPE:STRING=Release \
	-DDISABLE_INSTALLATION_OF_SWIG_HEADERS:BOOL=yes \
	-DENABLE_SWIG_PYTHON2:BOOL=no \
	-DENABLE_SWIG_PYTHON3:BOOL=yes \
	-DPYTHON3_EXECUTABLE:FILE=${PYTHON} \
	-DPYTHON3_VERSION:STRING=${PY_VER} \
;

# override the PYTHON3 LIBRARY cache variable to stop
# attempting to link against the static libpython library
if [[ "${target_platform}" == "linux"* ]]; then
	cmake -DPYTHON3_LIBRARIES="" ${SRC_DIR}
fi

# build
cmake --build python --parallel ${CPU_COUNT} --verbose

# install
cmake --build python --parallel ${CPU_COUNT} --verbose --target install

# test
if [[ "${CONDA_BUILD_CROSS_COMPILATION:-}" != "1" ]]; then
	ctest --parallel ${CPU_COUNT} --verbose
fi
