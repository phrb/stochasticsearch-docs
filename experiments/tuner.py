import argparse
import logging

import opentuner
from opentuner.search.manipulator import (ConfigurationManipulator,
                                          PermutationParameter)
from opentuner.search.objective import MinimizeTime
from opentuner.measurement import MeasurementInterface
from opentuner.measurement.inputmanager import FixedInputManager
from opentuner.tuningrunmain import TuningRunMain

argparser = argparse.ArgumentParser(parents=opentuner.argparsers())
argparser.add_argument( "-last", "--log-last",
                        dest     = "loglast",
                        type     = str,
                        required = True,
                        help     = "File to save best configuration to.")


class TSP(MeasurementInterface):
    def run(self, desired_result, input, limit):
        cfg  = desired_result.configuration.data
        tour = cfg[0]
        cmd  = "./tour_cost "
        for city in tour:
            cmd += str(city + 1) + " "

        result = self.call_program(cmd)
        cost   = float(result['stdout'])
        return opentuner.resultsdb.models.Result(time = cost)

    def manipulator(self):
        manipulator = ConfigurationManipulator()
        manipulator.add_parameter(PermutationParameter(0, range(48)))
        return manipulator

    def save_final_config(self, configuration):
        print "[Saving Best Configuration]"

        cfg = configuration.data
        tour = cfg[0]
        cmd  = ""

        for city in tour:
            cmd += str(city + 1) + "\n"

        with open(LOG_FILE, "a+") as file:
            file.write(cmd)

        print "[Done]"

if __name__ == '__main__':
    args = argparser.parse_args()
    LOG_FILE = args.loglast
    TSP.main(args)
