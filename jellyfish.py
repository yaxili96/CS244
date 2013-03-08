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

parser.add_argument('-t',
                    dest="topo",
                    action="store",
                    help="Topology",
                    default="jf")

parser.add_argument('-r',
                    dest="routing",
                    action="store",
                    help="Routing algorithm",
                    default="ksp")

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

def experiment(tp="jf", routing="ksp"):
    if tp == "jf":
        topo = JellyfishTopo(nServers=args.nServers,nSwitches=args.nSwitches,nPorts=args.nPorts)
    elif tp == "ft":
        topo = FatTreeTopo(k=args.nPorts)
    
    print "Starting Mininet"
    net = Mininet(topo=topo, host=CPULimitedHost, link=TCLink, controller=RemoteController,autoSetMacs=True)
    net.start()
    
    print "Dumping node connections"
    dumpNodeConnections(net.hosts)
    
    if tp == "jf":
        pox_args = shlex.split("pox/pox.py riplpox.riplpox --topo=%s,%s,%s,%s --routing=%s --mode=reactive" % (tp, args.nServers, args.nSwitches, args.nPorts, routing))
    elif tp == "ft":
        pox_args = shlex.split("pox/pox.py riplpox.riplpox --topo=%s,%s --routing=%s --mode=reactive" % (tp, args.nPorts, routing))
                
    print "Starting RiplPox"
    p = Popen(pox_args)
    sleep(25)

    print "Starting experiments"
    net.pingAll()

    

    print "Stopping Mininet"
    net.stop()
    print "Stopping RiplPox"
    p.terminate()
    sleep(10)
    
    # Ensure that all processes you create within Mininet are killed.       
    # Sometimes they require manual killing.                                
    Popen("pgrep -f webserver.py | xargs kill -9", shell=True).wait()

if __name__ == "__main__":
    experiment(tp=args.topo, routing=args.routing)
