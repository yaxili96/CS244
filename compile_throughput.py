'''
Compile the throughput data
'''

from argparse import ArgumentParser

import glob
import string

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
    tp = string.split(summary, ',')
    return tp

def compileData(topo, routing):
    throughputs = []
    for f in glob.glob("%s_%s_%s_*/iperf_client*.txt"):
        throughputs.append(calculateThroughput(f))

    return throughputs

jf-ksp = compile_data('jf', 'ksp')
jf-ecmp = compile_data('jf', 'ecmp')
#ft-ksp = compile_data('ft', 'ksp')
ft-ecmp = compile_data('ft', 'ecmp')

if args.out:
    print "Saving output to %s" % args.out
    # save to output file
    f = open(args.out, 'w')
    f.write("Jellyfish K-Shortest Paths: %s" % jf-ksp)
    f.write("Jellyfish ECMP: %s" % jf-ecmp)
    f.write("FatTree ECMP: %s" % ft-ecmp)
    f.close()
else:
    print "Jellyfish K-Shortest Paths: %s" % jf-ksp
    print "Jellyfish ECMP: %s" % jf-ecmp
#    print "FatTree K-Shortest Paths: %s" % ft-ksp
    print "FatTree ECMP: %s" % ft-ecmp
    
