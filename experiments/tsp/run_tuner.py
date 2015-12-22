#! /usr/bin/python2
import argparse
import time
import os

argparser = argparse.ArgumentParser()
argparser.add_argument( "-time", "--run-time",
                        dest     = "time",
                        type     = str,
                        required = True,
                        help     = "Time to tune the program.")
argparser.add_argument( "-r", "--tuning-runs",
                        dest     = "runs",
                        type     = int,
                        required = True,
                        help     = "Number of tuning runs to perform.")
argparser.add_argument( "-size", "--instance-size",
                        dest     = "size",
                        type     = int,
                        required = True,
                        help     = "Instance size.")

if __name__ == '__main__':
    print "[Initializing Tuning Experiment]"
    args =  argparser.parse_args()
    cmd  = "python2 tuner.py --no-dups"

    for i in range(args.runs):
        print "[Initializing Tuning Run " + str(i + 1) + "]"

        LOG_DIR = "results/pla85900_VM"

        run_id  = "/run_"  + str(i + 1)
        os.system("mkdir " + LOG_DIR)
        os.system("mkdir " + LOG_DIR + run_id)
        os.system("mkdir .tmp")

        cmd += " --stop-after="    + args.time
        cmd += " --log-last="      + LOG_DIR + run_id + "/last.txt"
        cmd += " --results-log="   + LOG_DIR + run_id + "/best.txt"
        cmd += " --instance-size=" + str(args.size)

        print "[Starting Run " + str(i + 1) + "]"
        os.system(cmd)
        print "[Tuning Run " + str(i + 1) + " is done]"

        os.system("rm -r opentuner.log opentuner.db .tmp")
