# -*- coding: utf-8 -*-
from datetime import datetime
from gnuradio import blocks
from gnuradio import gr
from gnuradio import zeromq
from phychic import clever_ishort2complex


class ModularSeer(gr.hier_block2):

    def __init__(self, block_size=40,
                       input_address='tcp://localhost',
                       input_port=35000,
                       one_in=24,
                       origin='some_gs'):
        gr.hier_block2.__init__(self, self.__class__.__name__,
                                      gr.io_signature(0, 0, 0),
                                      gr.io_signature(1, 1, gr.sizeof_gr_complex))

        self.block_size = block_size
        self.input_address = input_address
        self.input_port = input_port
        self.one_in = one_in
        self.origin = origin

        zmq_input = '%s:%d' % (input_address, input_port)
        self.src = zeromq.sub_source(gr.sizeof_short, 1, zmq_input, 100, True, -1)
        self.cis2c = clever_ishort2complex()

        dest_filename = datetime.now().strftime('%Y.%m.%d.%H.%M.%S_seer_' + origin + '_block_size_' + str(block_size) + '_one_in_' + str(one_in) + '.int16')
        self.file_sink = blocks.file_sink(gr.sizeof_short, dest_filename, False)
        self.file_sink.set_unbuffered(False)

        self.connect(self.cis2c, self)
        self.connect(self.src, self.file_sink)
        self.connect(self.src, self.cis2c)
