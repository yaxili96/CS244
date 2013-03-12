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
    return tp

def compileData(topo, routing):
    throughputs = []
    for f in glob.glob("%s_%s_%s_*/iperf_client*.txt"):
        throughputs.append(calculateThroughput(f))

    return numpy.mean(throughputs)

jf-ksp = compile_data('jf', 'ksp') * BITS_TO_MBITS
jf-ecmp = compile_data('jf', 'ecmp') * BITS_TO_MBITS
#ft-ksp = compile_data('ft', 'ksp') * BITS_TO_MBITS
ft-ecmp = compile_data('ft', 'ecmp') * BITS_TO_MBITS

if args.out:
    print "Saving output to %s" % args.out
    # save to output file
    f = open(args.out, 'w')
    f.write("Jellyfish K-Shortest Paths: %sMb/s" % jf-ksp)
    f.write("Jellyfish ECMP: %sMb/s" % jf-ecmp)
    f.write("FatTree ECMP: %sMb/s" % ft-ecmp)
    f.close()
else:
    print "Jellyfish K-Shortest Paths: %sMb/s" % jf-ksp
    print "Jellyfish ECMP: %sMb/s" % jf-ecmp
#    print "FatTree K-Shortest Paths: %sMb/s" % ft-ksp
    print "FatTree ECMP: %sMb/s" % ft-ecmp
    
