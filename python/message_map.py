#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# 
# Copyright 2019 Francisco Albani.
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
# 

import pmt
from gnuradio import gr


class MessageMap(gr.basic_block):
    """
    Applies a function to a message.

    For each message received, sends another with 'function(msg)' inside.

    The function must accept and return a pmt.

    If the function return None or pmt.PMT_NIL, nothing is sent.
    """
    def __init__(self, function):
        gr.basic_block.__init__(self,
                                self.__class__.__name__,
                                in_sig=None,
                                out_sig=None)
        self.function = function
        self.message_port_register_in(pmt.intern('in'))
        self.message_port_register_out(pmt.intern('out'))
        self.set_msg_handler(pmt.intern('in'), self.process_incoming)

    def process_incoming(self, msg):

        out = self.function(msg)
        if out not in [pmt.PMT_NIL, None]:
            self.message_port_pub(pmt.intern('out'), out)
