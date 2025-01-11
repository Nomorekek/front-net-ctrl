#!/usr/bin/env python3
"""
Network Control Tool for MPTCP
Developed for Front Research Group - NCSR Demokritos
Author: Christos Sakkas (chsakkas@hotmail.com - https://github.com/Nomorekek)

A command-line tool for MPTCP initialization and network interface bandwidth control in Linux environments.
This tool provides functionality for:
- Configuring MPTCP client and server endpoints
- Managing network interface bandwidth using traffic control (tc)

Usage:
    ./front-net-ctrl -m bandwidth --iface1 eth0 --bw1 100 --iface2 eth1 --bw2 50
    ./front-net-ctrl -m mptcp-client
    ./front-net-ctrl -m mptcp-server --subflow-ip 192.168.1.100 --subflow-iface eth0

MIT License

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
"""

import argparse
import subprocess
import sys

def configure_interface(iface, bandwidth):
    # Try to change existing qdisc first
    change_cmd = ['tc', 'qdisc', 'change', 'dev', iface, 'root', 'tbf',
                  'rate', f'{bandwidth}mbit', 'burst', '256mbit', 'latency', '600ms']
    
    try:
        result = subprocess.run(change_cmd, capture_output=True, text=True)
        if not result.stderr:
            print(f"Successfully modified bandwidth for {iface}")
            return True
    except subprocess.SubprocessError:
        pass

    # If change failed, try to add new qdisc
    add_cmd = ['tc', 'qdisc', 'add', 'dev', iface, 'root', 'tbf',
               'rate', f'{bandwidth}mbit', 'burst', '256mbit', 'latency', '600ms']
    
    try:
        result = subprocess.run(add_cmd, capture_output=True, text=True)
        if not result.stderr:
            print(f"Successfully added bandwidth limit for {iface}")
            return True
        print(f"Error configuring {iface}: {result.stderr}", file=sys.stderr)
        return False
    except subprocess.SubprocessError as e:
        print(f"Error executing command for {iface}: {e}", file=sys.stderr)
        return False

def handle_bandwidth_mode(args):
    success = True
    if not configure_interface(args.iface1, args.bw1):
        success = False
    if not configure_interface(args.iface2, args.bw2):
        success = False
    return success

def handle_mptcp_client_mode(args):
    print("Configuring MPTCP client mode...")
    commands = [
        ['ip', 'mptcp', 'limits', 'set', 'subflow', '2'],
        ['ip', 'mptcp', 'limits', 'set', 'add_addr_accepted', '2']
    ]
    
    success = True
    for cmd in commands:
        try:
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.stderr:
                print(f"Error executing {' '.join(cmd)}: {result.stderr}", file=sys.stderr)
                success = False
            else:
                print(f"Successfully executed: {' '.join(cmd)}")
        except subprocess.SubprocessError as e:
            print(f"Command failed {' '.join(cmd)}: {e}", file=sys.stderr)
            success = False
    
    return success

def handle_mptcp_server_mode(args):
    print("Configuring MPTCP server mode...")
    
    # First command: set subflow limit
    subflow_cmd = ['ip', 'mptcp', 'limits', 'set', 'subflow', '2']
    
    # Second command: add endpoint
    endpoint_cmd = ['ip', 'mptcp', 'endpoint', 'add', args.subflow_ip, 
                   'dev', args.subflow_iface, 'signal']
    
    success = True
    for cmd in [subflow_cmd, endpoint_cmd]:
        try:
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.stderr:
                print(f"Error executing {' '.join(cmd)}: {result.stderr}", file=sys.stderr)
                success = False
            else:
                print(f"Successfully executed: {' '.join(cmd)}")
        except subprocess.SubprocessError as e:
            print(f"Command failed {' '.join(cmd)}: {e}", file=sys.stderr)
            success = False
    
    return success

def main():
    parser = argparse.ArgumentParser(
        description="""
        Network Control Tool for MPTCP - Front Research Group, NCSR Demokritos
        Developer: Christos Sakkas (chsakkas@hotmail.com)
        
        A tool for initializing MPTCP in Linux environments and controlling
        network interface bandwidth. Supports MPTCP client/server configuration for one 
        subflow (e.g. Terrestrial+Satellite) and bandwidth management using traffic control (tc).
        
        Mode-specific parameters:
          bandwidth:     Requires --iface1, --bw1, --iface2, --bw2
          mptcp-client: No additional parameters required
          mptcp-server: Requires --subflow-ip, --subflow-iface
        
        Examples:
          ./front-net-ctrl -m bandwidth --iface1 eth0 --bw1 100 --iface2 eth1 --bw2 50
          ./front-net-ctrl -m mptcp-client
          ./front-net-ctrl -m mptcp-server --subflow-ip 192.168.1.100 --subflow-iface eth0
        """,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    # Mode argument
    parser.add_argument('-m', '--mode', required=True,
                       choices=['bandwidth', 'mptcp-client', 'mptcp-server'],
                       help='Operation mode (required)')
    
    # Bandwidth mode arguments
    bandwidth_group = parser.add_argument_group('Bandwidth mode parameters')
    bandwidth_group.add_argument('--iface1', help='First network interface')
    bandwidth_group.add_argument('--bw1', help='Bandwidth for first interface in Mbits')
    bandwidth_group.add_argument('--iface2', help='Second network interface')
    bandwidth_group.add_argument('--bw2', help='Bandwidth for second interface in Mbits')
    
    # MPTCP server mode arguments
    server_group = parser.add_argument_group('MPTCP server mode parameters')
    server_group.add_argument('--subflow-ip', help='Subflow IP address')
    server_group.add_argument('--subflow-iface', help='Subflow interface')
    
    args = parser.parse_args()
    
    # Validate mode-specific arguments
    if args.mode == 'bandwidth':
        if not all([args.iface1, args.bw1, args.iface2, args.bw2]):
            parser.error("bandwidth mode requires --iface1, --bw1, --iface2, and --bw2 arguments")
    elif args.mode == 'mptcp-server':
        if not args.subflow_ip or not args.subflow_iface:
            parser.error("mptcp-server mode requires --subflow-ip and --subflow-iface arguments")
    
    # Handle different modes
    success = False
    if args.mode == 'bandwidth':
        success = handle_bandwidth_mode(args)
    elif args.mode == 'mptcp-client':
        success = handle_mptcp_client_mode(args)
    elif args.mode == 'mptcp-server':
        success = handle_mptcp_server_mode(args)
    
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
