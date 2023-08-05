# -*- coding: utf-8 -*-
#
# Copyright 2015-2017 European Commission (JRC);
# Licensed under the EUPL (the 'Licence');
# You may not use this work except in compliance with the Licence.
# You may obtain a copy of the Licence at: http://ec.europa.eu/idabc/eupl

"""
It contains functions that model the basic mechanics of the clutch and torque
converter.

Sub-Modules:

.. currentmodule:: co2mpas.model.physical.clutch_tc

.. autosummary::
    :nosignatures:
    :toctree: clutch_tc/

    clutch
    torque_converter
"""

import schedula.utils as dsp_utl
import schedula as dsp
import scipy.interpolate as sci_itp
import numpy as np


def define_k_factor_curve(stand_still_torque_ratio=1.0, lockup_speed_ratio=0.0):
    """
    Defines k factor curve.

    :param stand_still_torque_ratio:
        Torque ratio when speed ratio==0.

        .. note:: The ratios are defined as follows:

           - Torque ratio = `gear box torque` / `engine torque`.
           - Speed ratio = `gear box speed` / `engine speed`.
    :type stand_still_torque_ratio: float

    :param lockup_speed_ratio:
        Minimum speed ratio where torque ratio==1.

        ..note::
            torque ratio==1 for speed ratio > lockup_speed_ratio.
    :type lockup_speed_ratio: float

    :return:
        k factor curve.
    :rtype: function
    """

    x = [0, lockup_speed_ratio, 1]
    y = [stand_still_torque_ratio, 1, 1]

    return sci_itp.InterpolatedUnivariateSpline(x, y, k=1)


def calculate_clutch_tc_powers(
        clutch_tc_speeds_delta, k_factor_curve, gear_box_speeds_in,
        gear_box_powers_in, engine_speeds_out):
    """
    Calculates the power that flows in the clutch or torque converter [kW].

    :param clutch_tc_speeds_delta:
        Engine speed delta due to the clutch or torque converter [RPM].
    :type clutch_tc_speeds_delta: numpy.array

    :param k_factor_curve:
        k factor curve.
    :type k_factor_curve: function

    :param gear_box_speeds_in:
        Gear box speed vector [RPM].
    :type gear_box_speeds_in: numpy.array

    :param gear_box_powers_in:
        Gear box power vector [kW].
    :type gear_box_powers_in: numpy.array

    :param engine_speeds_out:
        Engine speed [RPM].
    :type engine_speeds_out: numpy.array

    :return:
        Clutch or torque converter power [kW].
    :rtype: numpy.array
    """

    is_not_eng2gb = gear_box_speeds_in >= engine_speeds_out
    speed_out = np.where(is_not_eng2gb, engine_speeds_out, gear_box_speeds_in)
    speed_in = np.where(is_not_eng2gb, gear_box_speeds_in, engine_speeds_out)

    ratios = np.ones_like(gear_box_powers_in, dtype=float)
    b = (speed_in > 0) & (clutch_tc_speeds_delta != 0)
    ratios[b] = speed_out[b] / speed_in[b]

    eff = k_factor_curve(ratios) * ratios
    eff[is_not_eng2gb] = np.nan_to_num(1 / eff[is_not_eng2gb])

    powers = gear_box_powers_in.copy()
    b = eff > 0
    powers[b] = gear_box_powers_in[b] / eff[b]

    return powers


def default_has_torque_converter(gear_box_type):
    """
    Returns the default has torque converter value [-].

    :param gear_box_type:
        Gear box type (manual or automatic or cvt).
    :type gear_box_type: str

    :return:
        Does the vehicle use torque converter? [-]
    :rtype: bool
    """

    return gear_box_type == 'automatic'


def clutch_domain(kwargs):
    return not kwargs['has_torque_converter'] or kwargs['gear_box_type'] == 'cvt'


def torque_converter_domain(kwargs):
    return kwargs['has_torque_converter'] and kwargs['gear_box_type'] != 'cvt'


def clutch_torque_converter():
    """
    Defines the clutch and torque-converter model.

    .. dispatcher:: d

        >>> d = clutch_torque_converter()

    :return:
        The clutch and torque-converter model.
    :rtype: schedula.Dispatcher
    """

    d = dsp.Dispatcher(
        name='Clutch and torque-converter',
        description='Models the clutch and torque-converter.'
    )

    d.add_function(
        function=default_has_torque_converter,
        inputs=['gear_box_type'],
        outputs=['has_torque_converter']
    )

    d.add_function(
        function=calculate_clutch_tc_powers,
        inputs=['clutch_tc_speeds_delta', 'k_factor_curve',
                'gear_box_speeds_in', 'gear_box_powers_in',
                'engine_speeds_out'],
        outputs=['clutch_tc_powers']
    )

    from .clutch import clutch

    d.add_dispatcher(
        include_defaults=True,
        input_domain=clutch_domain,
        dsp=clutch(),
        dsp_id='clutch',
        inputs={
            'times': 'times',
            'accelerations': 'accelerations',
            'has_torque_converter': dsp_utl.SINK,
            'gear_box_type': dsp_utl.SINK,
            'clutch_model': 'clutch_model',
            'clutch_window': 'clutch_window',
            'clutch_tc_speeds_delta': 'clutch_speeds_delta',
            'gear_shifts': 'gear_shifts',
            'stand_still_torque_ratio': 'stand_still_torque_ratio',
            'lockup_speed_ratio': 'lockup_speed_ratio',
            'max_clutch_window_width': 'max_clutch_window_width',
            'engine_speeds_out': 'engine_speeds_out',
            'engine_speeds_out_hot': 'engine_speeds_out_hot',
            'cold_start_speeds_delta': 'cold_start_speeds_delta',
            'velocities': 'velocities',
            'gear_box_speeds_in': 'gear_box_speeds_in',
            'gears': 'gears',
            'stop_velocity': 'stop_velocity'
        },
        outputs={
            'clutch_speeds_delta': 'clutch_tc_speeds_delta',
            'clutch_window': 'clutch_window',
            'clutch_model': 'clutch_model',
            'k_factor_curve': 'k_factor_curve',
            'clutch_phases': 'clutch_phases'
        }
    )

    from .torque_converter import torque_converter

    d.add_dispatcher(
        include_defaults=True,
        input_domain=torque_converter_domain,
        dsp=torque_converter(),
        dsp_id='torque_converter',
        inputs={
            'times': 'times',
            'lock_up_tc_limits': 'lock_up_tc_limits',
            'calibration_tc_speed_threshold': 'calibration_tc_speed_threshold',
            'stop_velocity': 'stop_velocity',
            'velocities': 'velocities',
            'accelerations': 'accelerations',
            'has_torque_converter': dsp_utl.SINK,
            'gear_box_type': dsp_utl.SINK,
            'gears': 'gears',
            'clutch_tc_speeds_delta': 'torque_converter_speeds_delta',
            'engine_speeds_out_hot': ('gear_box_speeds_in',
                                      'engine_speeds_out_hot'),
            'torque_converter_model': 'torque_converter_model',
            'stand_still_torque_ratio': 'stand_still_torque_ratio',
            'lockup_speed_ratio': 'lockup_speed_ratio',
            'engine_speeds_out': 'engine_speeds_out',
            'cold_start_speeds_delta': 'cold_start_speeds_delta'
        },
        outputs={
            'torque_converter_speeds_delta': 'clutch_tc_speeds_delta',
            'torque_converter_model': 'torque_converter_model',
            'k_factor_curve': 'k_factor_curve'
        }
    )

    return d
