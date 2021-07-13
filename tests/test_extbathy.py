import pytest

from nldi_xstool.ancillary import getExtBathyXS
import numpy.testing as npt


@pytest.mark.parametrize(
    'file, ext, lonstr, latstr, elstr, acrs',
    [
        ('./data/09152500_2019-10-25_bathymetry.csv',
         50,
         'Lon_NAD83',
         'Lat_NAD83',
         'Bed_Elevation_meters_NAVD88',
         'epsg:4326')
    ]
)
def testxsbathy(file, ext, lonstr, latstr, elstr, acrs):
    xscomp = getExtBathyXS(file, ext, lonstr, latstr, elstr, acrs)
    npt.assert_allclose(min(xscomp.elevation), 1410.657, rtol=1e-3, atol=0)
    npt.assert_allclose(max(xscomp.elevation), 1417.439, rtol=1e-3, atol=0)
