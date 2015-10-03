import argparse
import logging

import opentuner
from opentuner.search.manipulator import (ConfigurationManipulator,
                                          PermutationParameter)
from opentuner.search.objective import MinimizeTime
from opentuner.measurement import MeasurementInterface
from opentuner.measurement.inputmanager import FixedInputManager
from opentuner.tuningrunmain import TuningRunMain


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

if __name__ == '__main__':
    parser = argparse.ArgumentParser(parents=opentuner.argparsers())
    args = parser.parse_args()
    TSP.main(args)
