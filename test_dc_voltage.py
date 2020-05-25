import time

__author__ = "Synapticon GmbH"
__copyright__ = "Copyright 2019, Synapticon GmbH"
__license__ = "Closed"
__email__ = "support@synapticon.com"

import logging
import pytest

import numpy as np
import ea_psu_controller
import random

# import somanet_toolbox as stb
logger = logging.getLogger(__name__)

# creat a connection with the power supply and turn it on waiting that it turns on also the device
psu = ea_psu_controller.PsuEA(comport='ea-ps-12v')
psu.output_on()
time.sleep(9)

class TestVoltage:
    def test_voltage(self, mmw, device_list):
        # set the parameters of maximum and minimun voltage and how many different random test you want to execute and the maximum error admitted
        psu = ea_psu_controller.PsuEA(comport='ea-ps-12v')
        number_tests = 3
        maximum_error = 2.3
        maximum_error = 2.3
        high_limit = 15
        low_limit = 10
        error_value = []
        error = []
        failures = []
        sum_errors = 0

        for device in device_list:
            od = device['object_dictionary']
            device_address = device['info'].device_address

            # Generates a random value between the range already stablished and sets it on the power supply
            for i in range(0, number_tests):
                voltage_set = (random.randrange(low_limit * 100, high_limit * 100, 1)) / 100
                psu.set_voltage(voltage_set)
                time.sleep(2)

                # The device voltage is measured and collected
                voltage_read = od.dc_link_circuit_voltage() / 1000

                # To compare the difference between both values we take the percentage of this error
                e_v = abs(round(10000 * (voltage_set - voltage_read) / voltage_read) / 100)
                error_value.append(e_v)

                #Assign a value according compering to your maximum value to perform a sum of errors
                if error_value[i] < maximum_error:
                    error.append(1)
                else:
                    error.append(0)
                    failures.append(str(error_value[i])+'%')
                sum_errors += error[i]

                # Show the voltage writen, readed and the calculated error
                logger.info('The voltage was set at ' + str(voltage_set) + 'V')
                logger.info(" The readed voltage is of " + str(voltage_read) + 'V')
                logger.info(" The error is of " + str(error_value[i]) + '%\n')

            # Keep voltage stablished after the test ended
            psu.close(True, False)

            # Criteria to pass the test
            assert sum_errors == number_tests, "The difference of voltages is of {} and increases the maximum error of {}%".format(failures, maximum_error)


