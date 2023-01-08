# -*- coding: utf-8 -*-

import unittest
import numpy as np
import os
from voiceassistant import main
from voiceassistant.core.iaudio import IAudio
from voiceassistant.audio import recorder, loader, speech_detector, player
from voiceassistant.text2speech import text2speech
from voiceassistant.core.constants import AUDIO_OUT


TESTS_RES = os.path.dirname(os.path.realpath(__file__)) + '/res'

class AllTestSuite(unittest.TestCase):
    """All test cases."""

    def test_absolute_truth(self):
        assert True

    def test_imported_module(self):
        self.assertIsNone(main.main())

    def test_recorder(self):
        res = recorder.record(dur=0.01)
        self.assertIsInstance(res, IAudio)

    def test_recorder(self):
        res = recorder.record(dur=0.01)
        self.assertIsInstance(res, IAudio)

    def test_loader(self):
        self.assertIsNone(loader.load_wave('random-path-xyz'))

        with open(f'{TESTS_RES}/smile-for-camera/test-values.npy', 'rb') as f:
            expected_values = np.load(f, encoding='bytes')
        with open(f'{TESTS_RES}/smile-for-camera/test-sample-width.npy', 'rb') as f:
            expected_sample_width = np.load(f, encoding='bytes')
        with open(f'{TESTS_RES}/smile-for-camera/test-framerate.npy', 'rb') as f:
            expected_framerate = np.load(f, encoding='bytes')

        aud = loader.load_wave(f'{TESTS_RES}/smile-for-camera/test.wav')
        self.assertIsInstance(aud, IAudio)
        self.assertTrue(np.array_equal(expected_values, aud.get_values()))
        self.assertTrue(np.array_equal(expected_sample_width, aud.get_sample_width()))
        self.assertTrue(np.array_equal(expected_framerate, aud.get_framerate()))

    def test_endpointing(self):
        with open(f'{TESTS_RES}/smile-for-camera/test-noise-mask.npy', 'rb') as f:
            expected_noise_mask = np.load(f, encoding='bytes')
        with open(f'{TESTS_RES}/smile-for-camera/test-noise-borders.npy', 'rb') as f:
            expected_noise_borders = np.load(f, encoding='bytes')
        
        aud = loader.load_wave(f'{TESTS_RES}/smile-for-camera/test.wav')
        noise_mask, noise_border = speech_detector.endpointing(aud)
        self.assertTrue(np.array_equal(expected_noise_mask, noise_mask))
        self.assertTrue(np.array_equal(expected_noise_borders, noise_border))

    def test_extraction(self):
        word_vals = []
        for i in range(4):
            with open(f'{TESTS_RES}/smile-for-camera/test-word-{i}.npy', 'rb') as f:
                word_vals.append(np.load(f, encoding='bytes'))

        aud = loader.load_wave(f'{TESTS_RES}/smile-for-camera/test.wav')
        speech = speech_detector.extract_speech(aud)
        self.assertEqual(len(speech), 4)

        for i in range(4):
            self.assertTrue(np.array_equal(word_vals[i], speech[i].get_values()))

    def test_text2speech(self):
        text = "Test speech here"
        file_path = AUDIO_OUT
        aud = text2speech.generate(text, file_path)

        # sound test
        player.play(aud)

        self.assertTrue(os.path.exists(file_path))
        self.assertTrue(os.path.getsize(file_path) > 0)

        # cleanup
        os.unlink(file_path)