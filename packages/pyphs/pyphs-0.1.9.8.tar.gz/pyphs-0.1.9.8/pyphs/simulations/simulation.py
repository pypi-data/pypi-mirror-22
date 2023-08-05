# -*- coding: utf-8 -*-
"""
Created on Tue May 24 11:20:26 2016

@author: Falaize
"""

from __future__ import absolute_import, division, print_function
from pyphs.config import simulations
from pyphs.cpp.simu2cpp import simu2cpp
from pyphs.numerics.method import PHSNumericalMethod
from pyphs.numerics.numeric import PHSNumericalCore
from .data import PHSData
from pyphs.misc.io import open_files, close_files, dump_files
import subprocess
import progressbar
import time
import os
import numpy as np


class PHSSimulation:
    """
    object that stores data and methods for simulation of PortHamiltonianObject
    """
    def __init__(self, core, config=None):
        """
        Parameters
        -----------

        opts : dic of configuration options

            keys and default values are

              'fs': 48e3,           # Sample rate (Hz)
              'grad': 'discret',    # In {'discret', 'theta', 'trapez'}
              'theta': 0.,          # Theta-scheme for the structure
              'split': False,       # split implicit from explicit part
              'maxit': 10,          # Max number of iterations for NL solvers
              'eps': 1e-16,         # Global numerical tolerance
              'path': None,         # Path to the results folder
              'pbar': True,         # Display a progress bar
              'timer': False,       # Display minimal timing infos
              'lang': 'c++',        # Language in {'python', 'c++'}
              'script': None,       # Call to C++ compiler and exec binary
              'eigen': None,        # Path to Eigen C++ library
              # Options for the data reader. The data are read from index imin
              # to index imax, rendering one element out of the number decim
              'load': {'imin': None,
                       'imax': None,
                       'decim': None}
        """

        # init config with standard configuration options
        self.config = simulations.copy()

        # update with provided opts
        if config is None:
            config = {}
        self.config.update(config)

        if self.config['path'] is None:
            self.config['path'] = os.getcwd()

        # store PHSCore
        setattr(self, '_core', core.__deepcopy__())

        self.fs = 0
        self.it = list()

        assert self.config['lang'] in ['c++', 'python']
        self.init_numericalcore()

###############################################################################

    def init_numericalmethod(self):
        if not self.fs == self.config['fs']:
            Method = PHSNumericalMethod
            self.method = Method(self._core, config=self.config)
            self.fs = self.config['fs']

    def init_numericalcore(self, x0=None):
        self.init_numericalmethod()
        setattr(self, 'nums', PHSNumericalCore(self.method,
                                               config=self.config))
        if x0 is not None:
            x0 = np.array(x0)
            assert len(x0.shape) == 1, \
                'x0 is not a 1D array, got x={}'.format(x0)
            self.nums.set_x(x0)

    def init(self, sequ=None, seqp=None, x0=None, nt=None, config=None):
        if config is None:
            config = {}
        self.config.update(config)
        self._core.M = self.nums.method.core.M
        setattr(self, 'data', PHSData(self._core, self.config))
        if x0 is None:
            x0 = np.zeros(self.nums.method.core.dims.x())
        self.data.init_data(sequ, seqp, x0, nt)
        self.nums.set_x(x0)

    def process(self):
        """
        process simulation for all time steps
        """
        print('Process...')
        if self.config['timer']:
            tstart = time.time()

        # language is 'py' or 'cpp'
        assert self.config['lang'] in ('c++', 'python'),\
            'language "{0!s}" unknown'.format(self.config['language'])

        if self.config['lang'] == 'c++':
            self.process_cpp()

        elif self.config['lang'] == 'python':
            self.process_py()

        if self.config['timer']:
            tstop = time.time()

        if self.config['timer']:
            time_it = ((tstop-tstart)/float(self.data.config['nt']))
            print('time per iteration: {0!s} s'.format(format(time_it, 'f')))
            time_ratio = time_it*self.config['fs']
            print('ratio compared to real-time: {0!s}'.format(format(
                time_ratio, 'f')))
        print('Done')

    def init_pb(self):
        pb_widgets = ['\n', 'Simulation: ',
                      progressbar.Percentage(), ' ',
                      progressbar.Bar(), ' ',
                      progressbar.ETA()
                      ]
        self.pbar = progressbar.ProgressBar(widgets=pb_widgets,
                                            maxval=self.data.config['nt'])
        self.pbar.start()

    def update_pb(self):
        self.pbar.update(self.n)

    def close_pb(self):
        self.pbar.finish()

    def process_py(self):

        # get generators of u and p
        data = self.data
        load = {'imin': 0, 'imax': None, 'decim': 1}
        seq_u = data.u(**load)
        seq_p = data.p(**load)

        files = open_files(self.config['path'] + os.sep + 'data',
                           self.config['files'])

        if self.config['pbar']:
            self.init_pb()

        # init time step
        self.n = 0
        
        # process
        for (u, p) in zip(seq_u, seq_p):
        	# update numerics
            self.nums.update(u=np.array(u), p=np.array(p))
            
            # write to files
            dump_files(self.nums, files)
            
            self.n += 1
            
            # update progressbar
            if self.config['pbar']:
                self.update_pb()
                
        if self.config['pbar']:
            self.close_pb()

        time.sleep(0.1)
        
        close_files(files)

    def process_cpp(self):

        simu2cpp(self)

        if self.config['script'] is None:
            print("\no==========================================================\
==o\n")
            print("Please, execute:\n" + self.config['path'] + os.sep + 'cpp' +
                  os.path.sep + "main.cpp")
            try:
                input("Press enter when done\nWaiting...\n\no=================\
===========================================o\n")
            except SyntaxError:
                pass
        else:
            # Replace generic term 'simulation_path' by actual object path
            script = self.config['script']
            path = self.config['path']
            if path is None:
                path = os.getcwd()
            script = script.replace('simulation_path', path)
            # exec Build and Run script
            system_call(script)


def system_call(cmd):
    p = subprocess.Popen(cmd, shell=True,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.STDOUT)
    for line in iter(p.stdout.readline, b''):
        print(line.decode()),
