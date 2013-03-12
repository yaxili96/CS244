'''
Compile the throughput data
'''

from argparse import ArgumentParser

import glob
import string

import numpy

BITS_TO_MBITS = 1.0/1000000

parser = ArgumentParser(description="Jellyfish Plots")
parser.add_argument('-dir',
                    help="Directory containing inputs for the throughput.",
                    dest="dir",
                    default=None)

parser.add_argument('-o',
                    help="Output txt file for the plot.",
                    dest="out",
                    default=None)

args = parser.parse_args()

def calculateThroughput(filename):
    f = open(filename)
    lines = f.readlines()

    # get last line summary
    summary = lines[-1]
    tp = string.split(summary, ',')[-1]
    print tp
    return tp

def compileData(topo, routing):
    throughputs = []
    for f in glob.glob("%s_%s_%s_*/iperf_client*.txt"):
        throughputs.append(calculateThroughput(f))

    print throughputs
    return numpy.array(throughputs).mean()

jf_ksp = compileData('jf', 'ksp') * BITS_TO_MBITS
jf_ecmp = compileData('jf', 'ecmp') * BITS_TO_MBITS
#ft_ksp = compileData('ft', 'ksp') * BITS_TO_MBITS
#ft_ecmp = compileData('ft', 'ecmp') * BITS_TO_MBITS

if args.out:
    print "Saving output to %s" % args.out
    # save to output file
    f = open(args.out, 'w')
    f.write("Jellyfish K-Shortest Paths: %sMb/s" % jf_ksp)
    f.write("Jellyfish ECMP: %sMb/s" % jf_ecmp)
    #f.write("FatTree ECMP: %sMb/s" % ft_ecmp)
    f.close()
else:
    print "Jellyfish K-Shortest Paths: %sMb/s" % jf_ksp
    print "Jellyfish ECMP: %sMb/s" % jf_ecmp
#    print "FatTree K_Shortest Paths: %sMb/s" % ft_ksp
    #print "FatTree ECMP: %sMb/s" % ft_ecmp
    
