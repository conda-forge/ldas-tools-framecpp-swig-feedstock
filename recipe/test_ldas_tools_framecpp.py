# -*- coding: utf-8 -*-
# Copyright 2024 Cardiff University <macleoddm@cardiff.ac.uk>

import os
import subprocess

import pytest

from LDAStools import frameCPP


@pytest.fixture
def sample_data(tmp_path):
    curdir = os.getcwd()
    os.chdir(tmp_path)
    try:
        subprocess.check_call(["framecpp_sample"])
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


def test_readfradcdata(sample_data):
    stream = frameCPP.IFrameFStream(str(sample_data))
    adc = stream.ReadFrAdcData(0, "Z0:RAMPED_REAL_4_1")
    assert adc.GetSampleRate() == 1024.
