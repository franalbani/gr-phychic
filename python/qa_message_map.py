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


from gnuradio import gr, gr_unittest
from gnuradio import blocks
from message_map import MessageMap
import time
import pmt

class QAMessageMap (gr_unittest.TestCase):

    def setUp (self):
        self.tb = gr.top_block()

    def tearDown (self):
        self.tb = None

    def test_identity(self):

        id_msg_map = MessageMap(lambda x: x)
        msg_debug = blocks.message_debug()

        self.tb.msg_connect(id_msg_map, 'out', msg_debug, 'store')

        self.tb.start()
        time.sleep(.2)

        data = {'a': 1, 'b': 'x', 'c': [1, 2, 3]}
        port = pmt.intern("in")
        id_msg_map.to_basic_block()._post(port, pmt.to_pmt(data))

        time.sleep(.2)
        self.tb.stop()
        self.tb.wait()
        msg = msg_debug.get_message(0)

        obtained = pmt.to_python(msg)

        self.assertEqual(data, obtained)

    def test_nil(self):

        nil_msg_map = MessageMap(lambda x: pmt.PMT_NIL)
        msg_debug = blocks.message_debug()

        self.tb.msg_connect(nil_msg_map, 'out', msg_debug, 'store')

        self.tb.start()
        time.sleep(.2)

        data = {'a': 1, 'b': 'x', 'c': [1, 2, 3]}
        port = pmt.intern("in")
        nil_msg_map.to_basic_block()._post(port, pmt.to_pmt(data))

        time.sleep(.2)
        self.tb.stop()
        self.tb.wait()

        n_msgs = msg_debug.num_messages()

        self.assertEqual(0, n_msgs)


if __name__ == '__main__':
    gr_unittest.run(QAMessageMap, "qa_MessageMap.xml")
