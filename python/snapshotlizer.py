#!/usr/bin/env python2
# -*- coding: utf-8 -*-
#
# Copyright 2016 Satellogic
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

import logging
from gnuradio import gr, blocks

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


class Snapshotlizer(gr.hier_block2):
    """
    Takes one block of 'block_size' from 'one_in'.
    """

    def __init__(self, block_size, one_in, item_size=gr.sizeof_gr_complex,
                 vector_output=False):

        logger.info('%s will reduce stream to %3.0f%%.' %
                    (self.__class__.__name__, 100.0 / one_in))

        out_sig_item_size = item_size * (block_size if vector_output else 1)

        gr.hier_block2.__init__(self, self.__class__.__name__,
                                gr.io_signature(1, 1, item_size),
                                gr.io_signature(1, 1, out_sig_item_size))

        self.s2v = blocks.stream_to_vector(item_size, block_size)
        self.keeper = blocks.keep_one_in_n(item_size * block_size, one_in)

        self.connect(self, self.s2v, self.keeper)

        if vector_output:
            self.connect(self.keeper, self)
        else:
            self.v2s = blocks.vector_to_stream(item_size, block_size)
            self.connect(self.keeper, self.v2s, self)


if __name__ == '__main__':
    sample_rate = 2e6
    symbol_rate = 40e3
    frame_len = (8 + 64) * 8

    desired_symbol_span = 1
    desired_res_bw = 10e3
    # fft_size = sample_rate / desired_res_bw
    fft_size = int(desired_symbol_span * sample_rate / symbol_rate)

    resulting_res_bw = sample_rate / fft_size

    frame_span = frame_len / symbol_rate

    blocks_per_frame = sample_rate * frame_span / fft_size

    one_in = int(blocks_per_frame / 1.5)

    item_size = 8 # bytes
    network_load = item_size * sample_rate / one_in

    print('\n')
    #print 'For sample_rate = %0.2f MHz, symbol_rate = %0.0f kbps and resolution = %0.0f kHz:' % (sample_rate/1e6, symbol_rate/1e3, desired_res_bw/1e3)
    print('For sample_rate = %0.2f MHz, symbol_rate = %0.0f kbps and symbol_span = %d:' % (sample_rate/1e6, symbol_rate/1e3, desired_symbol_span))
    print('Block size should be %d and only 1 block in %d should be kept.' % (fft_size, one_in))
    print('Resulting resulution bandwidth: %0.1f kHz' % (resulting_res_bw / 1e3))
    print('Resulting network load: %0.1f kBytes' % (network_load / 1024.0))
    print('\n')
