# -*- coding: utf-8 -*-
import cli
from unittest import TestCase
from click.testing import CliRunner


class TestCli(TestCase):
    # Bootstrap
    def setUp(self):
        TestCase.setUp(self)

        self.runner = CliRunner()

    def test_cli(self):
        self.skipTest("skip")
        result = self.runner.invoke(cli, ['help'])

        assert result.exit_code == 0
