#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Inner Eye Relay
# Author: Fran Albani
# GNU Radio version: 3.8.1.0

from gnuradio import blocks
from gnuradio import gr
from gnuradio.filter import firdes
import sys
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio import zeromq


class inner_eye_relay(gr.top_block):

    def __init__(self, input_address='tcp://localhost:34000', output_address='tcp://0.0.0.0:35000'):
        gr.top_block.__init__(self, "Inner Eye Relay")

        ##################################################
        # Parameters
        ##################################################
        self.input_address = input_address
        self.output_address = output_address

        ##################################################
        # Blocks
        ##################################################
        self.zeromq_sub_source_0 = zeromq.sub_source(gr.sizeof_short, 1, input_address, 100, True, -1)
        self.zeromq_pub_sink_0 = zeromq.pub_sink(gr.sizeof_short, 1, output_address, 100, True, -1)
        self.blocks_probe_rate_0 = blocks.probe_rate(gr.sizeof_short*1, 3000, 0.15)
        self.blocks_message_debug_0 = blocks.message_debug()



        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.blocks_probe_rate_0, 'rate'), (self.blocks_message_debug_0, 'print'))
        self.connect((self.zeromq_sub_source_0, 0), (self.blocks_probe_rate_0, 0))
        self.connect((self.zeromq_sub_source_0, 0), (self.zeromq_pub_sink_0, 0))


    def get_input_address(self):
        return self.input_address

    def set_input_address(self, input_address):
        self.input_address = input_address

    def get_output_address(self):
        return self.output_address

    def set_output_address(self, output_address):
        self.output_address = output_address




def argument_parser():
    parser = ArgumentParser()
    parser.add_argument(
        "-i", "--input-address", dest="input_address", type=str, default='tcp://localhost:34000',
        help="Set Input address [default=%(default)r]")
    parser.add_argument(
        "-o", "--output-address", dest="output_address", type=str, default='tcp://0.0.0.0:35000',
        help="Set Output address [default=%(default)r]")
    return parser


def main(top_block_cls=inner_eye_relay, options=None):
    if options is None:
        options = argument_parser().parse_args()
    tb = top_block_cls(input_address=options.input_address, output_address=options.output_address)

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()

        sys.exit(0)

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    tb.start()

    try:
        input('Press Enter to quit: ')
    except EOFError:
        pass
    tb.stop()
    tb.wait()


if __name__ == '__main__':
    main()
