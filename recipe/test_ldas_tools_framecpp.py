# -*- coding: utf-8 -*-
# Copyright 2024 Cardiff University <macleoddm@cardiff.ac.uk>

import os
import subprocess

import numpy

import pytest

from LDAStools import frameCPP


@pytest.fixture
def sample_data(tmp_path):
    curdir = os.getcwd()
    os.chdir(tmp_path)
    try:
        # framecpp 4.x: bare `framecpp_sample` goes through test_frame()
        # which produces TesT_<method>_<level>_... channel names and the
        # filename Z-R_std_test_frame_ver8-... .  Passing any
        # --channel-*-type flag routes through all_type_frame() which
        # emits the historical Z0:RAMPED_<TYPE>_1 channels and writes
        # the historical Z-ilwd_test_frame-... filename.
        # See https://git.ligo.org/computing/ldastools/LDAS_Tools/-/issues/283
        subprocess.check_call([
            "framecpp_sample",
            "--channel-adc-type", "int_2u",
            "--channel-adc-type", "int_2s",
            "--channel-adc-type", "int_4u",
            "--channel-adc-type", "int_4s",
            "--channel-adc-type", "int_8u",
            "--channel-adc-type", "int_8s",
            "--channel-adc-type", "real_4",
            "--channel-adc-type", "real_8",
            "--channel-adc-type", "complex_8",
            "--channel-adc-type", "complex_16",
        ])
        yield tmp_path / "Z-ilwd_test_frame-600000000-1.gwf"
    finally:
        os.chdir(curdir)


def test_gettoc(sample_data):
    stream = frameCPP.IFrameFStream(str(sample_data))
    toc = stream.GetTOC()
    assert sorted(toc.GetADC()) == sorted([
        "Z0:RAMPED_COMPLEX_16_1",
        "Z0:RAMPED_COMPLEX_8_1",
        "Z0:RAMPED_INT_2S_1",
        "Z0:RAMPED_INT_2U_1",
        "Z0:RAMPED_INT_4S_1",
        "Z0:RAMPED_INT_4U_1",
        "Z0:RAMPED_INT_8S_1",
        "Z0:RAMPED_INT_8U_1",
        "Z0:RAMPED_REAL_4_1",
        "Z0:RAMPED_REAL_8_1",
    ])


def test_getdataarray(sample_data):
    stream = frameCPP.IFrameFStream(str(sample_data))
    frdata = stream.ReadFrAdcData(0, "Z0:RAMPED_REAL_4_1")
    for i in range(frdata.data.size()):
        vect = frdata.data[i]
        arr = vect.GetDataArray()
        assert arr.dtype == numpy.float32


def test_readfradcdata(sample_data):
    stream = frameCPP.IFrameFStream(str(sample_data))
    adc = stream.ReadFrAdcData(0, "Z0:RAMPED_REAL_4_1")
    assert adc.GetSampleRate() == 1024.
