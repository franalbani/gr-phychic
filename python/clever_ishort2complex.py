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

from gnuradio import gr
from clever_complex2ishort import C2IS_SCALE_FACTOR


class clever_ishort2complex(gr.hier_block2):

    def __init__(self, scale_factor=1.0 / C2IS_SCALE_FACTOR):

        gr.hier_block2.__init__(self, self.__class__.__name__,
                                gr.io_signature(1, 1, gr.sizeof_short),
                                gr.io_signature(1, 1, gr.sizeof_gr_complex))


        self.is2c = blocks.interleaved_short_to_complex(vector_input=False, swap=False)
        self.scaler = blocks.multiply_const_cc(scale_factor)

        self.connect(self, self.is2c, self.scaler, self)
