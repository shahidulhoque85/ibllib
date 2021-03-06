# Mock dataset
import unittest

import numpy as np

from ibllib.ephys import ephysqc


class TestFpgaTask(unittest.TestCase):

    def test_impeccable_dataset(self):

        fpga2bpod = np.array([11 * 1e-6, -20])  # bpod starts 20 secs before with 10 ppm drift
        fpga_trials = {
            'intervals': np.array([[0, 9.5], [10, 19.5]]),
            'stimOn_times': np.array([2, 12]),
            'goCue_times': np.array([2.0001, 12.0001]),
            'ready_tone_in': np.array([2.0001, 12.0001]),
            'stim_freeze': np.array([4., 14.]),
            'feedback_times': np.array([4.0001, 14.0001]),
            'error_tone_in': np.array([4.0001, np.nan]),
            'valve_open': np.array([np.nan, 14.0001]),
            'stimOff_times': np.array([6.0001, 15.0001]),
            'iti_in': np.array([6.0011, 15.000]),
        }

        alf_trials = {
            'goCueTrigger_times_bpod': np.polyval(fpga2bpod, fpga_trials['goCue_times'] - 0.00067),
            'response_times_bpod': np.polyval(fpga2bpod, np.array([4., 14.])),
            'intervals_bpod': np.polyval(fpga2bpod, fpga_trials['intervals']),
            # Times from session start
            'goCueTrigger_times': fpga_trials['goCue_times'] - 0.00067,
            'response_times': np.array([4., 14.]),
            'intervals': fpga_trials['intervals'],
            'stimOn_times': fpga_trials['stimOn_times'],
            'goCue_times': fpga_trials['goCue_times'],
            'feedback_times': fpga_trials['feedback_times'],
        }
        qcs, qct = ephysqc.qc_fpga_task(fpga_trials, alf_trials)
        self.assertTrue(np.all([qcs[k] for k in qcs]))
        self.assertTrue(np.all([np.all(qct[k]) for k in qct]))


if __name__ == "__main__":
    unittest.main(exit=False)
