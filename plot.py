'''
Plot
'''
from helper import *
import plot_defaults

parser = argparse.ArgumentParser()
parser.add_argument('-i',
                    help="Input file for the plot.",
                    default=None)

parser.add_argument('-o',
                    help="Output png file for the plot.",
                    default=None) # Will show the plot

args = parser.parse_args()

# get keys
# get values
# get label

plt.plot(keys, values, lw=2, label="8 shortest paths", color="blue", drawstyle="steps-pre")
plt.plot(keys, values, lw=1, label="64 way ecmp", color="green", drawstyle="steps-pre")
plt.plot(keys, values, lw=1, label="8 way ecmp", color="red", drawstyle="steps-pre")

#plt.xlim((start,end))
#plt.ylim((start,end))
plt.xlabel("Rank of Link")
plt.ylabel("# Paths Link is on")
plt.legend()

if args.out:
    print "Saving output to %s" % args.out
    plt.savefig(args.out)
else:
    plt.show()
