
""" test_script.py: run all the examples in the openmc workshop and check each example produces the expected results.
    The example scripts open up various plots, some of which pause / block the running of this test suite.
    The running of the tests can be manually resumed by closing matplotlib and eog windows when they pop up
    run with
    pytest test_scripts.py
"""

# at the moment, we are only testing to see whether the outputs are created
# we are NOT testing to see whether the outputs are also saved locally
# this will have to be implemented

from pathlib import Path 
import os
import pytest
import unittest

cwd = os.getcwd()


class test_task_6(unittest.TestCase):

    def test_task_6_part_1(self):

        os.chdir(Path(cwd))
        os.chdir(Path('tasks/task_6'))
        output_filename = 'simulation_results.json'
        os.system('rm '+output_filename)
        os.system('python 1_example_tritium_production.py')
        assert Path(output_filename).exists() is True
        os.system('rm '+output_filename)

    def test_task_6_part_2(self):

        os.chdir(Path(cwd))
        os.chdir(Path('tasks/task_6'))
        output_filename = 'tbr_study.html'
        os.system('rm '+output_filename)
        os.system('python 2_example_tritium_production_study.py')
        assert Path(output_filename).exists() is True
        os.system('rm '+output_filename)
