# gr-phychic

Phychic: physical layer esoteric sensing tool

## Motivation

* We needed to diagnose the physical layer of a remote system.
* We wanted to see with our own eyes frames arrival, SNR, doppler shift, etc.
* Transmitting raw IQ through internet was out of the question due to bandwidth limitations.
* Naive downsampling would create aliasing or miss frames.

## Solution

* In the remote host:
    * modified our system to output a copy of raw iq through a IPC ZMQ socket.
      `0uhd` is included as an example if you want to use an USRP remotely.
    * run [inner_eye](apps/inner_eye) to:
        * read the socket
        * clever downsampling
        * offer that through a TCP ZMQ socket
* In the local host:
    * run [seer.grc](apps/seer.grc) with `gnuradio-companion` to:
        * connect to remote TCP socket
        * show spectrum
        * save to a file

## Installation

### Arch Linux

Use `tools/arch_build_helper`.
