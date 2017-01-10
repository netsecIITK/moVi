MoVi
===============================

## Mobile Video Protocol
Undergraduate project under Prof. Sandeep Shukla of IIT Kanpur.

* Apache License
* [Final report](http://home.iitk.ac.in/~sakshams/cs395a/report.pdf)
* [Presentation used at talk](http://home.iitk.ac.in/~sakshams/cs395a/pres.pdf) (24th November, 2016)
* Initial Blog post at [acehack.org](http://www.acehack.org/posts/2016-10-08-movi.html)

## Features
* Video chat for erratic networks.
* Degrades gracefully for high-packet loss rates
* Syncing regions of the video, ’best-effort’
* Stay completely connectionless
* Recover from lost connections, changed IPs gracefully

## Installation
Requires:
```
Python3 (Tested with >= 3.4)
OpenCV3
OpenCV3 for python (3.1.0)
A machine with a camera attached (camera id 0)
```

Beyond that, setup is as follows:
```
git clone git@github.com:netsecIITK/movi.git
mkvirtualenv movi
cd movi/
python setup.py develop
```

## Usage
To run, first start a broker on an IP accessible by both clients
```
cd movi/movi
python broker.py

# No distinction between SERVER and CLIENT for now
python movi.py SERVER <ip-of-broker>
python movi.py CLIENT <ip-of-broker>
```

This should open a window each for the client and the server. The client and server difference is nothing but
a way to decide who listens for the initial handshake (which involves secret sharing and port negotiation).
Beyond that, both the parties tear down their initial TCP connection, and proceed to use the UDP port for
subsequent video communication.

Note that the code can handle the client and the server both sending and receiving frames. But since this prevents
testing on a local machine (only one process can grab camera frames at one point), this is disabled for now.

Use **q** key to stop the video from any side. At the moment there is no `EOF` packet, but will be added soon.

## Credits
This package was created with [Cookiecutter_](https://github.com/audreyr/cookiecutter)
