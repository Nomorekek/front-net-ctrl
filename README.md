# Network Control Tool for MPTCP

Developed for Front Research Group - NCSR Demokritos

Author: Christos Sakkas (chsakkas@hotmail.com)


A command-line tool for MPTCP initialization and network interface bandwidth control in Linux environments.

This tool provides functionality for:

- Configuring MPTCP client and server endpoints
- Managing network interface bandwidth using traffic control (tc)
  

## Usage

    python3 front-net-ctrl.py -m bandwidth --iface1 eth0 --bw1 100 --iface2 eth1 --bw2 50
    python3 front-net-ctrl.py -m mptcp-client
    python3 front-net-ctrl.py -m mptcp-server --subflow-ip 192.168.2.100 --subflow-iface eth0

## Testing

**Server:** mptcpize run iperf3 -s

**Client:** mptcpize run iperf3 -c 192.168.1.100 -t60



## MIT License

Copyright (c) 2025 Front Research Group, NCSR Demokritos

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
