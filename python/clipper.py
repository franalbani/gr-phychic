#!/usr/bin/env python2
# -*- coding: utf-8 -*-
#
# Copyright 2017 Satellogic
#
# This is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3, or (at your option)
# any later version.
#
# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this software; see the file COPYING.  If not, write to
# the Free Software Foundation, Inc., 51 Franklin Street,
# Boston, MA 02110-1301, USA.

import numpy as np
from gnuradio import gr, blocks


class Clipper(gr.sync_block):

    def __init__(self, lower, upper):
        gr.sync_block.__init__(self, self.__class__.__name__,
                               in_sig=[np.complex64],
                               out_sig=[np.complex64])
        self.lower = lower
        self.upper = upper

    def clip(self, xs):
        return np.clip(xs, self.lower, self.upper)

    def work(self, input_items, output_items):

        output_items[0].real = self.clip(input_items[0].real)
        output_items[0].imag = self.clip(input_items[0].imag)

        return len(output_items[0])

