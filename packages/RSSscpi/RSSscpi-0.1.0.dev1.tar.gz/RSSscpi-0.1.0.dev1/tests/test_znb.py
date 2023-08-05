# -*- coding: utf-8 -*-
"""

@author: Lukas Sandström
"""

import pytest
from .conftest import VISA  # noqa: F401

from RSSscpi import ZNB  # noqa: F401


def test_init(znb, visa):
    """
    :param ZNB znb:
    :param VISA visa:
    """
    znb.init()
    assert ["*CLS;*ESE 127;*SRE 36",
            "SYSTem:COMMunicate:GPIB:SELF:RTERminator EOI",
            "SYSTem:COMMunicate:CODec UTF8",
            "SYSTem:LANGuage?",
            "SYSTem:LANGuage 'SCPI'",
            ] == visa.cmd


def test_active_channel(dummy_vna, visa):
    """
    :param ZNB dummy_vna:
    :param VISA visa:
    """
    vna = dummy_vna
    x = vna.active_channel
    assert x.n == 1
    vna.active_channel = 3
    vna.active_channel = "2"
    vna.active_channel = x
    assert ["INSTrument:NSELect?",
            "INSTrument:NSELect 3",
            "INSTrument:NSELect 2",
            "INSTrument:NSELect 1",
            ] == visa.cmd


def test_znb_screenshot(dummy_vna, visa):
    """
    :param ZNB dummy_vna:
    :param VISA visa:
    """
    vna = dummy_vna
    scr = vna.save_screenshot("scr.png")
    assert scr.filename == "scr.png"
    assert ["MMEMory:NAME 'scr.png'",
            "HCOPy:DESTination 'MMEM'",
            "HCOPy:DEVice:LANGuage PNG",
            "HCOPy:PAGE:WINDow HARDcopy",
            "HCOPy:IMMediate",
            "MMEMory:CDIRectory?",
            ] == visa.cmd
    pytest.raises(ValueError, 'vna.save_screenshot("scr.docx")')
    assert visa.cmd == []


def test_channel(dummy_vna, visa):
    """
    :param ZNB dummy_vna:
    :param VISA visa:
    """
    ch = dummy_vna.get_channel(3)
    assert ch.name == "1"
    ch.name = "Ch2"
    assert ["CONFigure:CHANnel3:NAME?",
            "CONFigure:CHANnel3:NAME 'Ch2'",
            ] == visa.cmd

    tr = ch.create_trace("Tr1", "S11")
    assert tr.name == "Tr1"
    tr = ch.create_trace("Tr2", "S22", dummy_vna.get_diagram(1))
    assert tr.name == "Tr2"
    assert ["CALCulate3:PARameter:SDEFine 'Tr1', 'S11'",
            "CALCulate3:PARameter:SDEFine 'Tr2', 'S22'",
            "DISPlay:WINDow1:TRACe:EFEed 'Tr2'",
            ] == visa.cmd

    tr = ch.active_trace
    assert tr.name == "1"
    ch.active_trace = "Tr3"
    ch.active_trace = ch.get_trace("Tr2")
    assert ["CALCulate3:PARameter:SELect?",
            "CALCulate3:PARameter:SELect 'Tr3'",
            "CALCulate3:PARameter:SELect 'Tr2'",
            ] == visa.cmd

    ch.power_level = -10.33
    assert ch.power_level == 1.
    assert ["SOURce3:POWer:LEVel:IMMediate:AMPLitude -10.33",
            "SOURce3:POWer:LEVel:IMMediate:AMPLitude?",
            ] == visa.cmd


def test_channel_sweep(dummy_vna, visa):
    """
    :param ZNB dummy_vna:
    :param VISA visa:
    """
    ch = dummy_vna.get_channel(3)
    x = ch.sweep.points.query_default()
    assert isinstance(x, int)
    ch.sweep.points.value = 301
    x = ch.sweep.points.value
    assert isinstance(x, int)
    ch.sweep.points = 301
    ch.sweep.TYPE.w("LIN")
    assert ["SENSe3:SWEep:POINts? DEF",
            "SENSe3:SWEep:POINts 301",
            "SENSe3:SWEep:POINts?",
            "SENSe3:SWEep:POINts 301",
            "SENSe3:SWEep:TYPE LIN",
            ] == visa.cmd
    ch.configure_freq_sweep(10e6, 9e9)
    assert ["SENSe3:SWEep:TYPE LIN",
            "SENSe3:FREQuency:STARt 10000000.0",
            "SENSe3:FREQuency:STOP 9000000000.0",
            ] == visa.cmd
    ch.configure_freq_sweep(10, 10e6, points=101, ifbw=1e3, power=-10, log_sweep=True)
    ch.init_sweep()
    assert ["SENSe3:SWEep:TYPE LOG",
            "SENSe3:FREQuency:STARt 10",
            "SENSe3:FREQuency:STOP 10000000.0",
            "SENSe3:SWEep:POINts 101",
            "SENSe3:BANDwidth 1000.0",
            "SOURce3:POWer:LEVel:IMMediate:AMPLitude -10",
            "INITiate3:IMMediate",
            ] == visa.cmd


def test_segmented_sweep(dummy_vna, visa):
    """
    :param ZNB dummy_vna:
    :param VISA visa:
    """
    ch = dummy_vna.get_channel(2)
    sw = ch.sweep
    sw.TYPE = ch.sweep.SEGMENT
    sw.analog_sweep_is_enabled = True
    sw.analog_sweep_is_enabled = False
    sw.dwell_time = 1.2
    sw.dwell_on_each_partial_measurement = True
    sw.dwell_on_each_partial_measurement = False
    sw.points = 41
    sw.count = 2
    sw.time = 0.1
    sw.use_auto_time = True
    sw.step_size = 1e6
    assert ["SENSe2:SWEep:GENeration ANALog",
            "SENSe2:SWEep:GENeration STEPped",
            "SENSe2:SWEep:DWELl 1.2",
            "SENSe2:SWEep:DWELl:IPOint ALL",
            "SENSe2:SWEep:DWELl:IPOint FIRSt",
            "SENSe2:SWEep:POINts 41",
            "SENSe2:SWEep:COUNt 2",
            "SENSe2:SWEep:TIME 0.1",
            "SENSe2:SWEep:TIME:AUTO ON",
            "SENSe2:SWEep:STEP 1000000.0",
            ] == visa.cmd

    sw.segments.insert_segment(1e6, 1e9, 11, 1e3, -10, position=3)
    sw.segments.insert_segment(1e6, 1e9, 11, 1e3, -10, position=3, analog_sweep=True)
    assert ["SENSe2:SEGMent4:INSert 1000000.0, 1000000000.0, 11, -10, AUTO, 0, 1000.0, AUTO, NORMal, STEPped",
            "SENSe2:SEGMent4:INSert 1000000.0, 1000000000.0, 11, -10, AUTO, 0, 1000.0, AUTO, NORMal, ANALog",
            ] == visa.cmd

    visa.ret = "5"
    assert len(sw.segments) == 5
    assert sw.segments[0].n == 1
    assert len(sw.segments[1:5]) == 4
    assert ["SENSe2:SEGMent:COUNt?",
            "SENSe2:SEGMent:COUNt?",
            ] == visa.cmd

    for (seg, n) in zip(iter(sw.segments), range(5)):
        assert seg.n == n + 1
    visa.clear_cmd()

    del sw.segments[2]
    del sw.segments[0:5:2]
    assert ["SENSe2:SEGMent3:DELete",
            "SENSe2:SEGMent:COUNt?",
            "SENSe2:SEGMent5:DELete",
            "SENSe2:SEGMent3:DELete",
            "SENSe2:SEGMent1:DELete",
            ] == visa.cmd

    sw.segments.remove_all_segments()
    sw.segments.remove_segment(2)
    sw.segments.disable_per_segment_dwell_time()
    sw.segments.disable_per_segment_if_selectivity()
    sw.segments.disable_per_segment_power()
    sw.segments.disable_per_segment_sweep_time()
    sw.segments.query_total_sweep_time()
    assert ["SENSe2:SEGMent:DELete:ALL",
            "SENSe2:SEGMent3:DELete",
            "SENSe2:SEGMent:SWEep:DWELl:CONTrol OFF",
            "SENSe2:SEGMent:BWIDth:RESolution:SELect:CONTrol OFF",
            "SENSe2:SEGMent:POWer:LEVel:CONTrol OFF",
            "SENSe2:SEGMent:SWEep:TIME:CONTrol OFF",
            "SENSe2:SEGMent:SWEep:TIME:SUM?",
            ] == visa.cmd

    seg = sw.segments[5]
    seg.delete()
    assert seg.dwell_time == 5
    assert seg.is_enabled == False
    assert seg.freq_start == 5
    assert seg.freq_stop == 5
    assert seg.if_bandwidth == 5
    assert seg.if_selectivity == "5"
    assert seg.number_of_points == 5
    assert seg.power_level == 5
    assert seg.sweep_time == 5
    seg.analog_sweep_is_enabled = True
    seg.analog_sweep_is_enabled = False
    del seg  # This shouldn't delete the segment
    assert ["SENSe2:SEGMent6:DELete",
            "SENSe2:SEGMent6:SWEep:DWELl?",
            "SENSe2:SEGMent6:STATe?",
            "SENSe2:SEGMent6:FREQuency:STARt?",
            "SENSe2:SEGMent6:FREQuency:STOP?",
            "SENSe2:SEGMent6:BWIDth:RESolution?",
            "SENSe2:SEGMent6:BWIDth:RESolution:SELect?",
            "SENSe2:SEGMent6:SWEep:POINts?",
            "SENSe2:SEGMent6:POWer?",
            "SENSe2:SEGMent6:SWEep:TIME?",
            "SENSe2:SEGMent6:SWEep:GENeration ANALog",
            "SENSe2:SEGMent6:SWEep:GENeration STEPped",
            ] == visa.cmd


def test_channel_cal(dummy_vna, visa):
    """
    :param ZNB dummy_vna:
    :param VISA visa:
    """
    ch = dummy_vna.get_channel(2)
    ch.cal_auto((1, 2, 3, 4))
    assert ["SENSe2:CORRection:COLLect:AUTO:TYPE FNPort, '', 1, 2, 3, 4",
            ] == visa.cmd
    ch.cal_auto((1, 2, 3, 4), (3, 4, 1, 2), cal_type="FOPort")
    assert ["SENSe2:CORRection:COLLect:AUTO:PORTs:TYPE FOPort, '', 1, 3, 2, 4, 3, 1, 4, 2",
            ] == visa.cmd
    ch.cal_auto((1, 2, 3, 4), cal_unit_characterization="user2.calkit")
    assert ["SENSe2:CORRection:COLLect:AUTO:TYPE FNPort, 'user2.calkit', 1, 2, 3, 4",
            ] == visa.cmd


def test_channel_save_touchstone(dummy_vna, visa):
    """
    :param ZNB dummy_vna:
    :param VISA visa:
    """
    ch = dummy_vna.get_channel(2)
    f = ch.save_touchstone("file.s3p", (1, 2, 3))
    assert f.filename == "file.s3p"
    assert ["MMEMory:STORe:TRACe:PORTs 2, 'file.s3p', LOGPhase, CIMPedance, 1, 2, 3",
            "MMEMory:CDIRectory?",
            ] == visa.cmd


def test_diagram(dummy_vna, visa):
    """
    :param ZNB dummy_vna:
    :param VISA visa:
    """
    dia = dummy_vna.get_diagram(1)
    f = dia.save_screenshot("hej.png")
    assert str(f) == "1\hej.png"
    assert ["MMEMory:NAME 'hej.png'",
            "HCOPy:DESTination 'MMEM'",
            "HCOPy:DEVice:LANGuage PNG",
            "DISPlay:WINDow1:MAXimize?",
            "DISPlay:WINDow1:MAXimize ON",
            "HCOPy:PAGE:WINDow ACTive",
            "HCOPy:IMMediate",
            "MMEMory:CDIRectory?",
            ] == visa.cmd
    assert dia.is_maximized
    dia.is_maximized = False
    dia.select_diagram()
    assert dia.n == 1
    dia.delete()
    assert dia.name == "1"
    dia.name = "Name2"
    assert dia.title == "1"
    dia.title = "Title2"
    assert dia.title_is_visible is True
    assert ["DISPlay:WINDow1:MAXimize?",
            "DISPlay:WINDow1:MAXimize OFF",
            "DISPlay:WINDow1:MAXimize?",
            "DISPlay:WINDow1:MAXimize ON",
            "DISPlay:WINDow1:STATe OFF",
            "DISPlay:WINDow1:NAME?",
            "DISPlay:WINDow1:NAME 'Name2'",
            "DISPlay:WINDow1:TITLe:DATA?",
            "DISPlay:WINDow1:TITLe:DATA 'Title2'",
            "DISPlay:WINDow1:TITLe:STATe?",
            ] == visa.cmd


def test_diagram_assigned_traces(dummy_vna, visa):
    """
    :param ZNB dummy_vna:
    :param VISA visa:
    """
    dia = dummy_vna.get_diagram(2)
    traces = []
    for a in range(1, 3):
        for b in range(1, 3):
            n = (a - 1) * 2 + b
            traces.append((n, "S%i%i" % (b, a)))

    visa.ret_dict["DISPlay:WINDow2:TRACe:CATalog?"] = "'1,S11,2,S21,3,S12,4,S22'"
    cnt = 0
    for (tr, (n, name)) in zip(dia.query_assigned_traces(), traces):
        assert tr.name == name
        cnt += 1
    assert cnt == 4
    assert ["DISPlay:WINDow2:TRACe:CATalog?",
            "CONFigure:TRACe:CHANnel:NAME:ID? 'S11'",
            "CONFigure:TRACe:CHANnel:NAME:ID? 'S21'",
            "CONFigure:TRACe:CHANnel:NAME:ID? 'S12'",
            "CONFigure:TRACe:CHANnel:NAME:ID? 'S22'",
            ] == visa.cmd


def test_marker(dummy_vna, visa):
    """
    Test that the Marker class works as expected.

    :param ZNB dummy_vna: This can be either a ZVA or ZNB instance with visa_res = visa dummy.
    :param VISA visa:
    """
    ch = dummy_vna.get_channel(2)
    tr = ch.get_trace("Tr1")
    m1 = tr.get_marker(3)
    assert [] == visa.cmd

    x = m1.tracking
    m1.tracking = False
    assert ["CALCulate2:PARameter:SELect 'Tr1'",
            "CALCulate2:MARKer3:SEARch:TRACking?",
            "CALCulate2:MARKer3:SEARch:TRACking OFF"] == visa.cmd
    assert isinstance(x, bool)

    tr.name = "Tr2"  # Change the trace name to force an "active trace" select
    visa.clear_cmd()
    m1.is_enabled = True
    x = m1.is_enabled
    m1.is_enabled = "OFF"
    assert ["CALCulate2:PARameter:SELect 'Tr2'",
            "CALCulate2:MARKer3:STATe ON",
            "CALCulate2:MARKer3:STATe?",
            "CALCulate2:MARKer3:STATe OFF"] == visa.cmd
    assert isinstance(x, bool)

    m1.x = 3.3
    x = m1.x
    assert ["CALCulate2:MARKer3:X 3.3",
            "CALCulate2:MARKer3:X?"] == visa.cmd
    assert isinstance(x, float)

    x = m1.y
    assert ["CALCulate2:MARKer3:Y?"] == visa.cmd
    assert isinstance(x, float)

    with pytest.raises(AttributeError, message="Assignment to marker y value is not possible."):
        m1.y = 2


def test_trace(dummy_vna, visa):
    """
    :param ZNB dummy_vna:
    :param VISA visa:
    """
    ch = dummy_vna.get_channel(2)
    tr = ch.get_trace("Tr7")
    tr.ref_level = 8
    visa.ret = "REAL"
    x = tr.trace_format
    assert x == "REAL"
    tr.trace_format = 2
    assert ["DISPlay:WINDow:TRACe:Y:SCALe:RLEVel 8, 'Tr7'",
            "CALCulate2:PARameter:SELect 'Tr7'",
            "CALCulate2:FORMat?",
            "CALCulate2:FORMat 2",
            ] == visa.cmd

    tr.copy_data_to_mem("Mem1")
    tr.copy_math_to_mem("MathMem1")
    assert ["TRACe:COPY 'Mem1', 'Tr7'",
            "TRACe:COPY:MATH 'MathMem1', 'Tr7'",
            ] == visa.cmd

    visa.ret = "1"
    assert tr.n == 1
    assert tr.n == 1
    pytest.raises(AttributeError, 'tr.n = 2')
    tr.delete()
    assert ["CONFigure:TRACe:NAME:ID? 'Tr7'",
            "CALCulate2:PARameter:DELete 'Tr7'",
            ] == visa.cmd

    visa.ret = "Tr7\r\n"
    assert tr.is_active()
    visa.ret = "Tr6\r\n"
    assert not tr.is_active()
    del tr
    assert ["CALCulate2:PARameter:SELect?",
            "CALCulate2:PARameter:SELect?",
            ] == visa.cmd


def test_trace_scaling(dummy_vna, visa):
    """
    :param ZNB dummy_vna:
    :param VISA visa:
    """
    tr = dummy_vna.get_channel(2).get_trace("Tr3")
    tr.scale_per_div = 10
    tr.scale_top = 8
    tr.scale_bottom = 2
    tr.ref_level = 0.8
    tr.ref_pos = 50  # Position in percent
    assert ["DISPlay:WINDow:TRACe:Y:SCALe:PDIVision 10, 'Tr3'",
            "DISPlay:WINDow:TRACe:Y:SCALe:TOP 8, 'Tr3'",
            "DISPlay:WINDow:TRACe:Y:SCALe:BOTTom 2, 'Tr3'",
            "DISPlay:WINDow:TRACe:Y:SCALe:RLEVel 0.8, 'Tr3'",
            "DISPlay:WINDow:TRACe:Y:SCALe:RPOSition 50, 'Tr3'",
            ] == visa.cmd
    assert tr.scale_per_div == 1
    assert tr.scale_top == 1
    assert tr.scale_bottom == 1
    assert tr.ref_level == 1
    assert tr.ref_pos == 1
    assert ["DISPlay:WINDow:TRACe:Y:SCALe:PDIVision? 'Tr3'",
            "DISPlay:WINDow:TRACe:Y:SCALe:TOP? 'Tr3'",
            "DISPlay:WINDow:TRACe:Y:SCALe:BOTTom? 'Tr3'",
            "DISPlay:WINDow:TRACe:Y:SCALe:RLEVel? 'Tr3'",
            "DISPlay:WINDow:TRACe:Y:SCALe:RPOSition? 'Tr3'",
            ] == visa.cmd
