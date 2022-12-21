# -*- coding: utf-8 -*-

import unittest
from voiceassistant import main
from voiceassistant.audio.recorder import record
from voiceassistant.core.iaudio import IAudio


class AllTestSuite(unittest.TestCase):
    """All test cases."""

    def test_absolute_truth(self):
        assert True

    def test_imported_module(self):
        self.assertIsNone(main.main())

    def test_recorder(self):
        res = record(dur=0.01)
        self.assertIsInstance(res, IAudio)