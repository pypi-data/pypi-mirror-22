#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 27 12:40:03 2016

@author: Falaize
"""

from __future__ import absolute_import, division, print_function

import os
from pyphs import PHSNetlist
from pyphs.config import datum as config_datum
config_datum = "'"+config_datum+"'"


def NetlistThieleSmallNL(label='TSnl', clear=True,
                         R=1e3, L=5e-2, Bl=50, M=0.1, K=5e3, A=1):
    """
    Write the netlist for a nonlinear version of the thieleSmall modeling of \
    loudspeakers.
    """

    netlist = PHSNetlist(os.getcwd() + os.sep + label + '.net', clear=clear)

    datum = netlist.datum

    # input voltage
    source = {'dictionary': 'electronics',
              'component': 'source',
              'label': 'IN',
              'nodes': ('A', datum),
              'arguments': {'type': "voltage"}}
    netlist.add_line(source)

    # resistor 1
    resistance = {'dictionary': 'electronics',
                  'component': 'resistor',
                  'label': 'R',
                  'nodes': ('A', 'B'),
                  'arguments': {'R': ('R', R)}}
    netlist.add_line(resistance)

    # inductor
    inductor = {'dictionary': 'electronics',
                'component': 'inductor',
                'label': 'L',
                'nodes': ('B', 'C'),
                'arguments': {'L': ('L', L)}}
    netlist.add_line(inductor)

    # gyrator
    gyrator = {'dictionary': 'connectors',
               'component': 'gyrator',
               'label': 'G',
               'nodes': ('C', datum, 'D', datum),
               'arguments': {'alpha': ('Bl', Bl)}}
    netlist.add_line(gyrator)

    # masse
    mass = {'dictionary': 'mechanics_dual',
            'component': 'mass',
            'label': 'M',
            'nodes': ('D', 'E'),
            'arguments': {'M': ('M', M)}}
    netlist.add_line(mass)

    # ressort cubic
    stifness = {'dictionary': 'mechanics_dual',
                'component': 'springcubic',
                'label': 'K',
                'nodes': ('E', 'F'),
                'arguments': {'K0': ('K0', K),
                              'K2': ('K2', 1e20)}
                }
    netlist.add_line(stifness)

    # amortissement
    damper = {'dictionary': 'mechanics_dual',
              'component': 'damper',
              'label': 'A',
              'nodes': ('F', datum),
              'arguments': {'A': ('A', A)}}
    netlist.add_line(damper)

    netlist.write()

    return netlist
netlist = NetlistThieleSmallNL()
target_netlist = "electronics.source IN ('A', "+config_datum+"): type=voltage;\nelectronics.resistor R ('A', 'B'): R=('R', 1000.0);\nelectronics.inductor L ('B', 'C'): L=('L', 0.05);\nconnectors.gyrator G ('C', "+config_datum+", 'D', "+config_datum+"): alpha=('Bl', 50);\nmechanics_dual.mass M ('D', 'E'): M=('M', 0.1);\nmechanics_dual.springcubic K ('E', 'F'): K2=('K2', 1e+20); K0=('K0', 5000.0);\nmechanics_dual.damper A ('F', "+config_datum+"): A=('A', 1);"
