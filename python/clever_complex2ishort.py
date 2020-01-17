#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# 
# Copyright 2018 Satellogic.
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

from gnuradio import gr, blocks
from .clipper import Clipper


C2IS_SCALE_FACTOR = float(2 ** (gr.sizeof_short * 8 - 1) - 1)

# TODO: parametrize clipping levels (with corresponding C2IS_SCALE_FACTOR)


class clever_complex2ishort(gr.hier_block2):
    '''
    * Clip to [-1; 1]
    * Scale to 2**15 - 1
    * complex to ishort
    '''
    def __init__(self):

        gr.hier_block2.__init__(self, self.__class__.__name__,
                                gr.io_signature(1, 1, gr.sizeof_gr_complex),
                                gr.io_signature(1, 1, gr.sizeof_short))

        self.clipper = Clipper(-1.0, 1.0)
        self.scaler = blocks.multiply_const_cc(C2IS_SCALE_FACTOR)
        self.c2is = blocks.complex_to_interleaved_short(vector=False)

        self.connect(self, self.clipper, self.scaler, self.c2is, self)
