from click.testing import CliRunner

# from nldi_xstool import nldi_xstool
from nldi_xstool import cli
from tempfile import NamedTemporaryFile
import json

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
    print(result)
    assert(result.exit_code == 0)
    ogdata = json.load(tf)
    feat = ogdata.get('features')
    assert(len(feat) == 11)
