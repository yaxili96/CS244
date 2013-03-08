#!/usr/bin/python 

"CS244 Spring 2013 Assignment 3: Jellyfish"

from mininet.topo import Topo
from mininet.node import CPULimitedHost
from mininet.link import TCLink
from mininet.node import RemoteController
from mininet.net import Mininet
from mininet.log import lg, info
from mininet.util import dumpNodeConnections
from mininet.cli import CLI

from ripl.ripl.dctopo import FatTreeTopo, JellyfishTopo

from ripl.ripl.routing import KSPRouting, ECMPRouting

import shlex

from subprocess import Popen, PIPE
from time import sleep, time
from multiprocessing import Process
from argparse import ArgumentParser
from random import randrange

#from monitor import monitor_qlen
import termcolor as T

import sys
import os
import math

parser = ArgumentParser(description="Jellyfish Tests")

parser.add_argument('-nse',
                    dest="nServers",
                    type=int,
                    action="store",
                    help="Number of servers",
                    default=16)

parser.add_argument('-nsw',
                    dest="nSwitches",
                    type=int,
                    action="store",
                    help="Number of switches",
                    default=20)

parser.add_argument('-np',
                     dest="nPorts",
                    type=int,
                    action="store",
                    help="Number of ports per switch",
                    default=4)

args = parser.parse_args()

def increment_link_count(link, link_counts):
    if link in link_counts:
        link_counts[link] += 1
    else:
        link_counts[link] = 1

# route is a list of nodes
# link_counts is a dictionary of links to their path counts
def parse_route(route, link_counts):
    if len(route) == 0:
        return
    curr_start = route[0]
    for i in range(1, len(route)):
        node = route[i]
        link = (curr_start, node)
        increment_link_count(link, link_counts)
        curr_start = node

# routes is a list of lists of nodes
# link_counts is a dictionary of links to their path counts
def parse_routes(routes, link_counts):
    for route in routes:
        parse_route(route, link_counts)

ROUTING = { 
    'ksp' : KSPRouting,
    'ecmp' : ECMPRouting
}

def experiment(exp="jf", routing="ksp"):
    if exp == "jf":
        topo = JellyfishTopo(nServers=args.nServers,nSwitches=args.nSwitches,nPorts=args.nPorts)
    elif exp == "ft":
        topo = FatTreeTopo(k=args.nPorts)
    
    print "Starting Mininet"
    net = Mininet(topo=topo, host=CPULimitedHost, link=TCLink, controller=RemoteController,autoSetMacs=True)
    net.start()
    
    #print "Dumping node connections"
    #dumpNodeConnections(net.hosts)
    
    if exp == "jf":
        pox_args = shlex.split("pox/pox.py riplpox.riplpox --topo=%s,%s,%s,%s --routing=%s --mode=reactive" % (exp, args.nServers, args.nSwitches, args.nPorts, routing))
    elif exp == "ft":
        pox_args = shlex.split("pox/pox.py riplpox.riplpox --topo=%s,%s --routing=%s --mode=reactive" % (exp, args.nPorts, routing))
                
    print "Starting RiplPox"
    with open(os.devnull, "w") as fnull:
        p = Popen(pox_args, stdout=fnull, stderr=fnull)
    sleep(25)

    print "Starting experiments for topo %s and routing %s" % (exp, routing)
    #net.pingAll()

    link_counts = {}
    routing_obj = ROUTING[routing](topo)
    for i in range(1, args.nServers + 1):
        src = 'h%d' % i
        for j in range(1, args.nServers + 1):
            if i == j:
                # skip if same node
                continue
            dst = 'h%d' % j
            #routes = routing_obj.get_routes(src, dst)
            # routes don't include the src and dst hosts, so pass those to parse
            #parse_routes(routes, link_counts)
            route = routing_obj.get_route(src, dst, 0)
            parse_route(route, link_counts)

    print link_counts

    print "Stopping Mininet"
    net.stop()
    print "Stopping RiplPox"
    p.terminate()
    sleep(10)
    
    # Ensure that all processes you create within Mininet are killed.       
    # Sometimes they require manual killing.                                
    Popen("pgrep -f webserver.py | xargs kill -9", shell=True).wait()

if __name__ == "__main__":
    experiment('jf', 'ksp')
    experiment('jf', 'ecmp')
