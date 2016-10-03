Moto Watch Gesture Emulator and Receiver

The Moto watch code may be found at https://github.com/Zziwei/GestureUDP.git

This directory contains scripts that emulate the Moto watch Gesture
program and a server that receives the data.

* SendPkgExample.py constructs data packages and sends all the packages through UDPSocket (It is
considered as an Watch emulator here).

* SendPkgExample.js A JavaScript version that sends the data as above.

* ReceivePkgExample.py listens to the UDP port, receive data and parse the data.

How to use
=========
Below is how to use the two scripts using Python

1. Find your IP address.  Under Mac OS X, use ifconfig -a
2. Edit SendPkgExample.py and ReceivePkgExample.py and substitute in the IP address
3. In one window, run <pre>python SendPkgExample.py</pre>
4. In another window, run <pre>python ReceivePkgExample.py</pre>

To use the JavaScript version:

1. Find your IP address.  Under Mac OS X, use ifconfig -a
2. Edit SendPkgExample.js and ReceivePkgExample.py and substitute in the IP address
3. In one window, run <pre>node SendPkgExample.js</pre>
4. In another window, run <pre>python ReceivePkgExample.py</pre>



