import logging
import unittest
from pathlib import Path

import numpy as np

import alf.io
from ibllib.io import raw_data_loaders as raw
import ibllib.io.extractors


class TestExtractTrialData(unittest.TestCase):

    def setUp(self):
        self.main_path = Path(__file__).parent
        self.training_lt5 = {'path': self.main_path / 'data' / 'session_training_lt5'}
        self.biased_lt5 = {'path': self.main_path / 'data' / 'session_biased_lt5'}
        self.training_ge5 = {'path': self.main_path / 'data' / 'session_training_ge5'}
        self.biased_ge5 = {'path': self.main_path / 'data' / 'session_biased_ge5'}
        self.training_lt5['ntrials'] = len(raw.load_data(self.training_lt5['path']))
        self.biased_lt5['ntrials'] = len(raw.load_data(self.biased_lt5['path']))
        self.training_ge5['ntrials'] = len(raw.load_data(self.training_ge5['path']))
        self.biased_ge5['ntrials'] = len(raw.load_data(self.biased_ge5['path']))
        # turn off logging for unit testing as we will purposedly go into warning/error cases
        self.wheel_ge5_path = self.main_path / 'data' / 'wheel_ge5'
        self.wheel_lt5_path = self.main_path / 'data' / 'wheel_lt5'
        self.logger = logging.getLogger('ibllib')

    def test_get_feedbackType(self):
        # TRAINING SESSIONS
        ft = ibllib.io.extractors.training_trials.get_feedbackType(
            self.training_lt5['path'], save=False, data=False)
        self.assertEqual(ft.size, self.training_lt5['ntrials'])
        # check if no 0's in feedbackTypes
        self.assertFalse(ft[ft == 0].size > 0)
        # -- version >= 5.0.0
        ft = ibllib.io.extractors.training_trials.get_feedbackType(
            self.training_ge5['path'], save=False, data=False)
        self.assertEqual(ft.size, self.training_ge5['ntrials'])
        # check if no 0's in feedbackTypes
        self.assertFalse(ft[ft == 0].size > 0)

        # BIASED SESSIONS
        ft = ibllib.io.extractors.biased_trials.get_feedbackType(
            self.biased_lt5['path'], save=False, data=False)
        self.assertEqual(ft.size, self.biased_lt5['ntrials'])
        # check if no 0's in feedbackTypes
        self.assertFalse(ft[ft == 0].size > 0)
        # -- version >= 5.0.0
        ft = ibllib.io.extractors.biased_trials.get_feedbackType(
            self.biased_ge5['path'], save=False, data=False)
        self.assertEqual(ft.size, self.biased_ge5['ntrials'])
        # check if no 0's in feedbackTypes
        self.assertFalse(ft[ft == 0].size > 0)

    def test_get_contrastLR(self):
        # TRAINING SESSIONS
        cl, cr = ibllib.io.extractors.training_trials.get_contrastLR(
            self.training_lt5['path'])
        self.assertTrue(all([np.sign(x) >= 0 for x in cl if ~np.isnan(x)]))
        self.assertTrue(all([np.sign(x) >= 0 for x in cr if ~np.isnan(x)]))
        self.assertTrue(sum(np.isnan(cl)) + sum(np.isnan(cr)) == len(cl))
        self.assertTrue(sum(~np.isnan(cl)) + sum(~np.isnan(cr)) == len(cl))
        # -- version >= 5.0.0
        cl, cr = ibllib.io.extractors.training_trials.get_contrastLR(
            self.training_ge5['path'])
        self.assertTrue(all([np.sign(x) >= 0 for x in cl if ~np.isnan(x)]))
        self.assertTrue(all([np.sign(x) >= 0 for x in cr if ~np.isnan(x)]))
        self.assertTrue(sum(np.isnan(cl)) + sum(np.isnan(cr)) == len(cl))
        self.assertTrue(sum(~np.isnan(cl)) + sum(~np.isnan(cr)) == len(cl))

        # BIASED SESSIONS
        cl, cr = ibllib.io.extractors.biased_trials.get_contrastLR(
            self.biased_lt5['path'])
        self.assertTrue(all([np.sign(x) >= 0 for x in cl if ~np.isnan(x)]))
        self.assertTrue(all([np.sign(x) >= 0 for x in cr if ~np.isnan(x)]))
        self.assertTrue(sum(np.isnan(cl)) + sum(np.isnan(cr)) == len(cl))
        self.assertTrue(sum(~np.isnan(cl)) + sum(~np.isnan(cr)) == len(cl))
        # -- version >= 5.0.0
        cl, cr = ibllib.io.extractors.biased_trials.get_contrastLR(
            self.biased_ge5['path'])
        self.assertTrue(all([np.sign(x) >= 0 for x in cl if ~np.isnan(x)]))
        self.assertTrue(all([np.sign(x) >= 0 for x in cr if ~np.isnan(x)]))
        self.assertTrue(sum(np.isnan(cl)) + sum(np.isnan(cr)) == len(cl))
        self.assertTrue(sum(~np.isnan(cl)) + sum(~np.isnan(cr)) == len(cl))

    def test_get_probabilityLeft(self):
        # TRAINING SESSIONS
        pl = ibllib.io.extractors.training_trials.get_probabilityLeft(
            self.training_lt5['path'])
        self.assertTrue(isinstance(pl, np.ndarray))
        # -- version >= 5.0.0
        pl = ibllib.io.extractors.training_trials.get_probabilityLeft(
            self.training_ge5['path'])
        self.assertTrue(isinstance(pl, np.ndarray))

        # BIASED SESSIONS
        pl = ibllib.io.extractors.biased_trials.get_probabilityLeft(
            self.biased_lt5['path'])
        self.assertTrue(isinstance(pl, np.ndarray))
        # Test if only probs that are in prob set
        md = raw.load_settings(self.biased_lt5['path'])
        if md:
            probs = md['BLOCK_PROBABILITY_SET']
            probs.append(0.5)
            self.assertTrue(sum([x in probs for x in pl]) == len(pl))
        # -- version >= 5.0.0
        pl = ibllib.io.extractors.biased_trials.get_probabilityLeft(
            self.biased_ge5['path'])
        self.assertTrue(isinstance(pl, np.ndarray))
        # Test if only probs that are in prob set
        md = raw.load_settings(self.biased_ge5['path'])
        probs = md['BLOCK_PROBABILITY_SET']
        probs.append(0.5)
        self.assertTrue(sum([x in probs for x in pl]) == len(pl))

    def test_get_choice(self):
        # TRAINING SESSIONS
        choice = ibllib.io.extractors.training_trials.get_choice(
            self.training_lt5['path'])
        self.assertTrue(isinstance(choice, np.ndarray))
        data = raw.load_data(self.training_lt5['path'])
        trial_nogo = np.array(
            [~np.isnan(t['behavior_data']['States timestamps']['no_go'][0][0])
             for t in data])
        if any(trial_nogo):
            self.assertTrue(all(choice[trial_nogo]) == 0)
        # -- version >= 5.0.0
        choice = ibllib.io.extractors.training_trials.get_choice(
            self.training_ge5['path'])
        self.assertTrue(isinstance(choice, np.ndarray))
        data = raw.load_data(self.training_ge5['path'])
        trial_nogo = np.array(
            [~np.isnan(t['behavior_data']['States timestamps']['no_go'][0][0])
             for t in data])
        if any(trial_nogo):
            self.assertTrue(all(choice[trial_nogo]) == 0)

        # BIASED SESSIONS
        choice = ibllib.io.extractors.biased_trials.get_choice(
            self.biased_lt5['path'])
        self.assertTrue(isinstance(choice, np.ndarray))
        data = raw.load_data(self.biased_lt5['path'])
        trial_nogo = np.array(
            [~np.isnan(t['behavior_data']['States timestamps']['no_go'][0][0])
             for t in data])
        if any(trial_nogo):
            self.assertTrue(all(choice[trial_nogo]) == 0)
        # -- version >= 5.0.0
        choice = ibllib.io.extractors.biased_trials.get_choice(
            self.biased_ge5['path'])
        self.assertTrue(isinstance(choice, np.ndarray))
        data = raw.load_data(self.biased_ge5['path'])
        trial_nogo = np.array(
            [~np.isnan(t['behavior_data']['States timestamps']['no_go'][0][0])
             for t in data])
        if any(trial_nogo):
            self.assertTrue(all(choice[trial_nogo]) == 0)

    def test_get_repNum(self):
        # TODO: Test its sawtooth
        # TRAINING SESSIONS
        rn = ibllib.io.extractors.training_trials.get_repNum(
            self.training_lt5['path'])
        self.assertTrue(isinstance(rn, np.ndarray))
        for i in range(3):
            self.assertTrue(i in rn)
        # -- version >= 5.0.0
        rn = ibllib.io.extractors.training_trials.get_repNum(
            self.training_ge5['path'])
        self.assertTrue(isinstance(rn, np.ndarray))
        for i in range(4):
            self.assertTrue(i in rn)

        # BIASED SESSIONS have no repeted trials

    def test_get_rewardVolume(self):
        # TRAINING SESSIONS
        rv = ibllib.io.extractors.training_trials.get_rewardVolume(
            self.training_lt5['path'])
        self.assertTrue(isinstance(rv, np.ndarray))
        # -- version >= 5.0.0
        rv = ibllib.io.extractors.training_trials.get_rewardVolume(
            self.training_ge5['path'])
        self.assertTrue(isinstance(rv, np.ndarray))

        # BIASED SESSIONS
        rv = ibllib.io.extractors.biased_trials.get_rewardVolume(
            self.biased_lt5['path'])
        self.assertTrue(isinstance(rv, np.ndarray))
        # Test if all non zero rewards are of the same value
        self.assertTrue(all([x == max(rv) for x in rv if x != 0]))
        # -- version >= 5.0.0
        rv = ibllib.io.extractors.biased_trials.get_rewardVolume(
            self.biased_ge5['path'])
        self.assertTrue(isinstance(rv, np.ndarray))
        # Test if all non zero rewards are of the same value
        self.assertTrue(all([x == max(rv) for x in rv if x != 0]))

    def test_get_feedback_times_ge5(self):
        # TRAINING SESSIONS
        ft = ibllib.io.extractors.training_trials.get_feedback_times_ge5(
            self.training_ge5['path'])
        self.assertTrue(isinstance(ft, np.ndarray))

        # BIASED SESSIONS
        ft = ibllib.io.extractors.biased_trials.get_feedback_times_ge5(
            self.biased_ge5['path'])
        self.assertTrue(isinstance(ft, np.ndarray))

    def test_get_feedback_times_lt5(self):
        # TRAINING SESSIONS
        ft = ibllib.io.extractors.training_trials.get_feedback_times_lt5(
            self.training_lt5['path'])
        self.assertTrue(isinstance(ft, np.ndarray))

        # BIASED SESSIONS
        ft = ibllib.io.extractors.biased_trials.get_feedback_times_lt5(
            self.biased_lt5['path'])
        self.assertTrue(isinstance(ft, np.ndarray))

    def test_get_feedback_times(self):
        # TRAINING SESSIONS
        ft = ibllib.io.extractors.training_trials.get_feedback_times(
            self.training_ge5['path'])
        self.assertTrue(isinstance(ft, np.ndarray))
        ft = ibllib.io.extractors.training_trials.get_feedback_times(
            self.training_lt5['path'], settings={'IBLRIG_VERSION_TAG': '4.9.9'})
        self.assertTrue(isinstance(ft, np.ndarray))

        # BIASED SESSIONS
        ft = ibllib.io.extractors.biased_trials.get_feedback_times(
            self.biased_ge5['path'])
        self.assertTrue(isinstance(ft, np.ndarray))
        ft = ibllib.io.extractors.biased_trials.get_feedback_times(
            self.biased_lt5['path'], settings={'IBLRIG_VERSION_TAG': '4.9.9'})
        self.assertTrue(isinstance(ft, np.ndarray))

    def test_get_stimOnTrigger_times(self):
        # TRAINING SESSIONS
        sott = ibllib.io.extractors.training_trials.get_stimOnTrigger_times(
            self.training_lt5['path'])
        self.assertTrue(isinstance(sott, np.ndarray))
        # -- version >= 5.0.0
        sott = ibllib.io.extractors.training_trials.get_stimOnTrigger_times(
            self.training_ge5['path'])
        self.assertTrue(isinstance(sott, np.ndarray))
        # BIASED SESSIONS
        sott = ibllib.io.extractors.biased_trials.get_stimOnTrigger_times(
            self.biased_lt5['path'])
        self.assertTrue(isinstance(sott, np.ndarray))
        # -- version >= 5.0.0
        sott = ibllib.io.extractors.biased_trials.get_stimOnTrigger_times(
            self.biased_ge5['path'])
        self.assertTrue(isinstance(sott, np.ndarray))

    def test_get_stimOn_times_lt5(self):
        # TRAINING SESSIONS
        st = ibllib.io.extractors.training_trials.get_stimOn_times_lt5(
            self.training_lt5['path'])
        self.assertTrue(isinstance(st, np.ndarray))

        # BIASED SESSIONS
        st = ibllib.io.extractors.biased_trials.get_stimOn_times_lt5(
            self.biased_lt5['path'])
        self.assertTrue(isinstance(st, np.ndarray))

    def test_get_stimOn_times_ge5(self):
        # TRAINING SESSIONS
        st = ibllib.io.extractors.training_trials.get_stimOn_times_ge5(
            self.training_ge5['path'])
        self.assertTrue(isinstance(st, np.ndarray))

        # BIASED SESSIONS
        st = ibllib.io.extractors.biased_trials.get_stimOn_times_ge5(
            self.biased_ge5['path'])
        self.assertTrue(isinstance(st, np.ndarray))

    def test_get_stimOn_times(self):
        # TRAINING SESSIONS
        st = ibllib.io.extractors.training_trials.get_stimOn_times(
            self.training_lt5['path'], settings={'IBLRIG_VERSION_TAG': '4.9.9'})
        self.assertTrue(isinstance(st, np.ndarray))
        st = ibllib.io.extractors.training_trials.get_stimOn_times(
            self.training_ge5['path'])
        self.assertTrue(isinstance(st, np.ndarray))

        # BIASED SESSIONS
        st = ibllib.io.extractors.biased_trials.get_stimOn_times(
            self.biased_lt5['path'], settings={'IBLRIG_VERSION_TAG': '4.9.9'})
        self.assertTrue(isinstance(st, np.ndarray))
        st = ibllib.io.extractors.biased_trials.get_stimOn_times(
            self.biased_ge5['path'])
        self.assertTrue(isinstance(st, np.ndarray))

    def test_get_intervals(self):
        # TRAINING SESSIONS
        di = ibllib.io.extractors.training_trials.get_intervals(
            self.training_lt5['path'])
        self.assertTrue(isinstance(di, np.ndarray))
        self.assertFalse(np.isnan(di).all())
        # -- version >= 5.0.0
        di = ibllib.io.extractors.training_trials.get_intervals(
            self.training_ge5['path'])
        self.assertTrue(isinstance(di, np.ndarray))
        self.assertFalse(np.isnan(di).all())

        # BIASED SESSIONS
        di = ibllib.io.extractors.biased_trials.get_intervals(
            self.training_lt5['path'])
        self.assertTrue(isinstance(di, np.ndarray))
        self.assertFalse(np.isnan(di).all())
        # -- version >= 5.0.0
        di = ibllib.io.extractors.biased_trials.get_intervals(
            self.training_ge5['path'])
        self.assertTrue(isinstance(di, np.ndarray))
        self.assertFalse(np.isnan(di).all())

    def test_get_iti_duration(self):
        # TRAINING SESSIONS
        iti = ibllib.io.extractors.training_trials.get_iti_duration(
            self.training_lt5['path'])
        self.assertTrue(isinstance(iti, np.ndarray))
        # -- version >= 5.0.0 iti always == 0.5 sec no extract

        # BIASED SESSIONS
        iti = ibllib.io.extractors.biased_trials.get_iti_duration(
            self.biased_lt5['path'])
        self.assertTrue(isinstance(iti, np.ndarray))
        # -- version >= 5.0.0 iti always == 0.5 sec no extract

    def test_get_response_times(self):
        # TRAINING SESSIONS
        rt = ibllib.io.extractors.training_trials.get_response_times(
            self.training_lt5['path'])
        self.assertTrue(isinstance(rt, np.ndarray))
        # -- version >= 5.0.0
        rt = ibllib.io.extractors.training_trials.get_response_times(
            self.training_ge5['path'])
        self.assertTrue(isinstance(rt, np.ndarray))

        # BIASED SESSIONS
        rt = ibllib.io.extractors.biased_trials.get_response_times(
            self.biased_lt5['path'])
        self.assertTrue(isinstance(rt, np.ndarray))
        # -- version >= 5.0.0
        rt = ibllib.io.extractors.biased_trials.get_response_times(
            self.biased_ge5['path'])
        self.assertTrue(isinstance(rt, np.ndarray))

    def test_get_goCueTrigger_times(self):
        # TRAINING SESSIONS
        data = raw.load_data(self.training_lt5['path'])
        gct = np.array([tr['behavior_data']['States timestamps']
                        ['closed_loop'][0][0] for tr in data])
        self.assertTrue(isinstance(gct, np.ndarray))
        # -- version >= 5.0.0
        gct = ibllib.io.extractors.training_trials.get_goCueTrigger_times(
            self.training_ge5['path'])
        self.assertTrue(isinstance(gct, np.ndarray))

        # BIASED SESSIONS
        data = raw.load_data(self.biased_lt5['path'])
        gct = np.array([tr['behavior_data']['States timestamps']
                        ['closed_loop'][0][0] for tr in data])
        self.assertTrue(isinstance(gct, np.ndarray))
        # -- version >= 5.0.0
        gct = ibllib.io.extractors.biased_trials.get_goCueTrigger_times(
            self.biased_ge5['path'])
        self.assertTrue(isinstance(gct, np.ndarray))

    def test_get_goCueOnset_times(self):
        # TRAINING SESSIONS
        gcot = ibllib.io.extractors.training_trials.get_goCueOnset_times(
            self.training_lt5['path'])
        self.assertTrue(isinstance(gcot, np.ndarray))
        self.assertTrue(np.all(np.isnan(gcot)))
        self.assertTrue(gcot.size != 0 or gcot.size == 4)
        # -- version >= 5.0.0
        gcot = ibllib.io.extractors.training_trials.get_goCueOnset_times(
            self.training_ge5['path'])
        self.assertTrue(isinstance(gcot, np.ndarray))
        self.assertFalse(np.any(np.isnan(gcot)))
        self.assertTrue(gcot.size != 0 or gcot.size == 12)

        # BIASED SESSIONS
        gcot = ibllib.io.extractors.biased_trials.get_goCueOnset_times(
            self.biased_lt5['path'])
        self.assertTrue(isinstance(gcot, np.ndarray))
        self.assertFalse(np.any(np.isnan(gcot)))
        self.assertTrue(gcot.size != 0 or gcot.size == 4)
        # -- version >= 5.0.0
        gcot = ibllib.io.extractors.biased_trials.get_goCueOnset_times(
            self.biased_ge5['path'])
        self.assertTrue(isinstance(gcot, np.ndarray))
        self.assertFalse(np.any(np.isnan(gcot)))
        self.assertTrue(gcot.size != 0 or gcot.size == 8)

    def test_get_included_trials_lt5(self):
        # TRAINING SESSIONS
        it = ibllib.io.extractors.training_trials.get_included_trials_lt5(
            self.training_lt5['path'])
        self.assertTrue(isinstance(it, np.ndarray))
        # BIASED SESSIONS
        it = ibllib.io.extractors.biased_trials.get_included_trials_lt5(
            self.biased_lt5['path'])
        self.assertTrue(isinstance(it, np.ndarray))

    def test_get_included_trials_ge5(self):
        # TRAINING SESSIONS
        it = ibllib.io.extractors.training_trials.get_included_trials_ge5(
            self.training_ge5['path'])
        self.assertTrue(isinstance(it, np.ndarray))
        # BIASED SESSIONS
        it = ibllib.io.extractors.biased_trials.get_included_trials_ge5(
            self.biased_ge5['path'])
        self.assertTrue(isinstance(it, np.ndarray))

    def test_get_included_trials(self):
        # TRAINING SESSIONS
        it = ibllib.io.extractors.training_trials.get_included_trials(
            self.training_lt5['path'], settings={'IBLRIG_VERSION_TAG': '4.9.9'})
        self.assertTrue(isinstance(it, np.ndarray))
        # -- version >= 5.0.0
        it = ibllib.io.extractors.training_trials.get_included_trials(
            self.training_ge5['path'])
        self.assertTrue(isinstance(it, np.ndarray))

        # BIASED SESSIONS
        it = ibllib.io.extractors.biased_trials.get_included_trials(
            self.biased_lt5['path'], settings={'IBLRIG_VERSION_TAG': '4.9.9'})
        self.assertTrue(isinstance(it, np.ndarray))
        # -- version >= 5.0.0
        it = ibllib.io.extractors.biased_trials.get_included_trials(
            self.biased_ge5['path'])
        self.assertTrue(isinstance(it, np.ndarray))

    def test_extract_all(self):
        # TRAINING SESSIONS
        ibllib.io.extractors.training_trials.extract_all(
            self.training_lt5['path'], settings={'IBLRIG_VERSION_TAG': '4.9.9'}, save=True)
        # -- version >= 5.0.0
        ibllib.io.extractors.training_trials.extract_all(
            self.training_ge5['path'], save=True)
        # BIASED SESSIONS
        ibllib.io.extractors.biased_trials.extract_all(
            self.biased_lt5['path'], settings={'IBLRIG_VERSION_TAG': '4.9.9'}, save=True)
        # -- version >= 5.0.0
        ibllib.io.extractors.biased_trials.extract_all(
            self.biased_ge5['path'], save=True)

    def test_encoder_positions_clock_reset(self):
        # TRAINING SESSIONS
        # only for training?
        path = self.training_lt5['path'] / "raw_behavior_data"
        path = next(path.glob("_iblrig_encoderPositions.raw*.ssv"), None)
        dy = raw._load_encoder_positions_file_lt5(path)
        dat = np.array([849736, 1532230, 1822449, 1833514, 1841566, 1848206, 1853979, 1859144])
        self.assertTrue(np.all(np.diff(dy['re_ts']) > 0))
        self.assertTrue(all(dy['re_ts'][6:] - 2 ** 32 - dat == 0))

    def test_encoder_positions_clock_errors(self):
        # here we test for 2 kinds of file corruption that happen
        # 1/2 the first sample time is corrupt and absurdly high and should be discarded
        # 2/2 2 samples are swapped and need to be swapped backk
        path = self.biased_lt5['path'] / "raw_behavior_data"
        path = next(path.glob("_iblrig_encoderPositions.raw*.ssv"), None)
        dy = raw._load_encoder_positions_file_lt5(path)
        self.assertTrue(np.all(np.diff(np.array(dy.re_ts)) > 0))
        # -- version >= 5.0.0
        path = self.biased_ge5['path'] / "raw_behavior_data"
        path = next(path.glob("_iblrig_encoderPositions.raw*.ssv"), None)
        dy = raw._load_encoder_positions_file_ge5(path)
        self.assertTrue(np.all(np.diff(np.array(dy.re_ts)) > 0))

    def test_wheel_folders(self):
        # the wheel folder contains other errors in bpod output that had to be addressed
        for wf in self.wheel_lt5_path.glob('_iblrig_encoderPositions*.raw*.ssv'):
            df = raw._load_encoder_positions_file_lt5(wf)
            self.assertTrue(np.all(np.diff(np.array(df.re_ts)) > 0))
        for wf in self.wheel_lt5_path.glob('_iblrig_encoderEvents*.raw*.ssv'):
            df = raw._load_encoder_events_file_lt5(wf)
            self.assertTrue(np.all(np.diff(np.array(df.re_ts)) > 0))
        for wf in self.wheel_ge5_path.glob('_iblrig_encoderPositions*.raw*.ssv'):
            df = raw._load_encoder_positions_file_ge5(wf)
            self.assertTrue(np.all(np.diff(np.array(df.re_ts)) > 0))
        for wf in self.wheel_ge5_path.glob('_iblrig_encoderEvents*.raw*.ssv'):
            df = raw._load_encoder_events_file_ge5(wf)
            self.assertTrue(np.all(np.diff(np.array(df.re_ts)) > 0))

    def test_load_encoder_positions(self):
        raw.load_encoder_positions(self.training_lt5['path'],
                                   settings={'IBLRIG_VERSION_TAG': '4.9.9'})
        raw.load_encoder_positions(self.training_ge5['path'])
        raw.load_encoder_positions(self.biased_lt5['path'],
                                   settings={'IBLRIG_VERSION_TAG': '4.9.9'})
        raw.load_encoder_positions(self.biased_ge5['path'])

    def test_load_encoder_events(self):
        raw.load_encoder_events(self.training_lt5['path'],
                                settings={'IBLRIG_VERSION_TAG': '4.9.9'})
        raw.load_encoder_events(self.training_ge5['path'])
        raw.load_encoder_events(self.biased_lt5['path'],
                                settings={'IBLRIG_VERSION_TAG': '4.9.9'})
        raw.load_encoder_events(self.biased_ge5['path'])

    def test_size_outputs(self):
        # check the output dimensions
        from ibllib.pipes import extract_session
        extract_session.from_path(self.training_ge5['path'])
        trials = alf.io.load_object(self.training_ge5['path'] / 'alf', object='_ibl_trials')
        self.assertTrue(alf.io.check_dimensions(trials) == 0)
        extract_session.from_path(self.training_lt5['path'], force=True)
        trials = alf.io.load_object(self.training_lt5['path'] / 'alf', object='_ibl_trials')
        self.assertTrue(alf.io.check_dimensions(trials) == 0)
        extract_session.from_path(self.biased_ge5['path'])
        trials = alf.io.load_object(self.biased_ge5['path'] / 'alf', object='_ibl_trials')
        self.assertTrue(alf.io.check_dimensions(trials) == 0)
        extract_session.from_path(self.biased_lt5['path'], force=True)
        trials = alf.io.load_object(self.biased_lt5['path'] / 'alf', object='_ibl_trials')
        self.assertTrue(alf.io.check_dimensions(trials) == 0)
        # Make sure we get the log files
        log_files = list(self.main_path.rglob('_ibl_log.info*.log'))
        self.assertTrue(len(log_files) == 4)

    def tearDown(self):
        for f in self.main_path.rglob('_ibl_log.*.log'):
            f.unlink()
        [x.unlink() for x in self.training_lt5['path'].rglob('alf/*') if x.is_file()]
        [x.unlink() for x in self.biased_lt5['path'].rglob('alf/*') if x.is_file()]
        [x.unlink() for x in self.training_ge5['path'].rglob('alf/*') if x.is_file()]
        [x.unlink() for x in self.biased_ge5['path'].rglob('alf/*') if x.is_file()]
        [x.rmdir() for x in self.training_lt5['path'].rglob('alf/') if x.is_dir()]
        [x.rmdir() for x in self.biased_lt5['path'].rglob('alf/') if x.is_dir()]
        [x.rmdir() for x in self.training_ge5['path'].rglob('alf/') if x.is_dir()]
        [x.rmdir() for x in self.biased_ge5['path'].rglob('alf/') if x.is_dir()]


class TestSyncWheelBpod(unittest.TestCase):

    def test_sync_bpod_bonsai_poor_quality_timestamps(self):
        sync_trials_robust = raw.sync_trials_robust
        drift_pol = np.array([11 * 1e-6, -20])  # bpod starts 20 secs before with 10 ppm drift
        np.random.seed(seed=784)
        t0_full = np.cumsum(np.random.rand(50)) + .001
        t1_full = np.polyval(drift_pol, t0_full) + t0_full
        t0 = t0_full.copy()
        t1 = t1_full.copy()

        t0_, t1_ = sync_trials_robust(t0, t1)
        assert np.allclose(t1_, np.polyval(drift_pol, t0_) + t0_)

        t0_, t1_ = sync_trials_robust(t0, t1[:-1])
        assert np.allclose(t1_, np.polyval(drift_pol, t0_) + t0_)

        t0_, t1_ = sync_trials_robust(t0, t1[1:])
        assert np.allclose(t1_, np.polyval(drift_pol, t0_) + t0_)

        t0_, t1_ = sync_trials_robust(t0[1:], t1)
        assert np.allclose(t1_, np.polyval(drift_pol, t0_) + t0_)

        t0_, t1_ = sync_trials_robust(t0[:-1], t1)
        assert np.allclose(t1_, np.polyval(drift_pol, t0_) + t0_)

        t0_, t1_ = sync_trials_robust(t0, np.delete(t1, 24))
        assert np.allclose(t1_, np.polyval(drift_pol, t0_) + t0_)

        t0_, t1_ = sync_trials_robust(np.delete(t0, 12), np.delete(t1, 24))
        assert np.allclose(t1_, np.polyval(drift_pol, t0_) + t0_)


class TestWheelLoaders(unittest.TestCase):

    def setUp(self) -> None:
        self.main_path = Path(__file__).parent

    def test_encoder_events_corrupt(self):
        path = self.main_path.joinpath('data', 'wheel', 'lt5')
        for file_events in path.rglob('_iblrig_encoderEvents.raw.*'):
            dy = raw._load_encoder_events_file_lt5(file_events)
            self.assertTrue(dy.size > 6)
        path = self.main_path.joinpath('data', 'wheel', 'ge5')
        for file_events in path.rglob('_iblrig_encoderEvents.raw.*'):
            dy = raw._load_encoder_events_file_ge5(file_events)
            self.assertTrue(dy.size > 6)

    def test_encoder_positions_corrupts(self):
        path = self.main_path.joinpath('data', 'wheel', 'ge5')
        for file_position in path.rglob('_iblrig_encoderPositions.raw.*'):
            dy = raw._load_encoder_positions_file_ge5(file_position)
            self.assertTrue(dy.size > 18)
        path = self.main_path.joinpath('data', 'wheel', 'lt5')
        for file_position in path.rglob('_iblrig_encoderPositions.raw.*'):
            dy = raw._load_encoder_positions_file_lt5(file_position)
            self.assertTrue(dy.size > 18)


if __name__ == "__main__":
    unittest.main(exit=False)
    print('.')
