#!/usr/bin/env python

"""Tests for `nldi_xstool` package."""

import pytest

from click.testing import CliRunner

# from nldi_xstool import nldi_xstool
from nldi_xstool import cli
from tempfile import NamedTemporaryFile
import json


# @pytest.fixture
# def response():
#     """Sample pytest fixture.

#     See more at: http://doc.pytest.org/en/latest/fixture.html
#     """
#     # import requests
#     # return requests.get('https://github.com/audreyr/cookiecutter-pypackage')


# def test_content(response):
#     """Sample pytest test function with the pytest fixture as an argument."""
#     # from bs4 import BeautifulSoup
#     # assert 'GitHub' in BeautifulSoup(response.content).title.string


def test_command_line_interface():
    """Test the CLI."""
    runner = CliRunner()
    result = runner.invoke(cli.main)
    print(result)
    assert result.exit_code == 0
    assert 'xsatpoint' in result.output
    help_result = runner.invoke(cli.main, ['--help'])
    assert help_result.exit_code == 0
    assert '\n\nCommands:\n  xsatendpts\n' in help_result.output


def test_xsatpoint():
    runner = CliRunner()

    with NamedTemporaryFile(mode='w+') as tf:
        result = runner.invoke(
                                cli.main,
                                [
                                    'xsatpoint', '-f', tf.name,
                                    '--lonlat', '-103.80119', '40.2684',
                                    '--width', '100', '--numpoints', '11',
                                    '-r', '10m'
                                ]
                              )
        assert(result.exit_code == 0)
        ogdata = json.load(tf)
        feat = ogdata.get('features')
        assert(len(feat) == 11)


def test_xsatendpts():
    runner = CliRunner()

    with NamedTemporaryFile(mode='w+') as tf:
        result = runner.invoke(
                                cli.main,
                                [
                                    'xsatendpts', '-f', tf.name,
                                    '-s', '-103.801134', '40.26733',
                                    '-e', '-103.800787', ' 40.272798',
                                    '-c', 'epsg:4326',
                                    '-n', '11',
                                    '-r', '10m'
                                ]
                              )
        assert(result.exit_code == 0)
        ogdata = json.load(tf)
        feat = ogdata.get('features')
        assert(len(feat) == 11)


def test_xsatendpts_wres():
    runner = CliRunner()
    res = ['1m', '3m', '5m', '10m', '30m']
    for tr in res:
        print(f'resoluition: {tr}')
        with NamedTemporaryFile(mode='w+') as tf:
            result = runner.invoke(
                                    cli.main,
                                    [
                                        'xsatendpts', '-f', tf.name,
                                        '-s', '-103.801134', '40.26733',
                                        '-e', '-103.800787', ' 40.272798',
                                        '-c', 'epsg:4326',
                                        '-n', '11',
                                        '-r', tr
                                    ]
                                )
            assert(result.exit_code == 0)
            ogdata = json.load(tf)
            feat = ogdata.get('features')
            assert(len(feat) == 11)
