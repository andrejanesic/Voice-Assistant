# -*- coding: utf-8 -*-

import unittest
from voiceassistant import main


class AllTestSuite(unittest.TestCase):
    """All test cases."""

    def test_absolute_truth(self):
        assert True

    def test_imported_module(self):
        self.assertIsNone(main.main())
