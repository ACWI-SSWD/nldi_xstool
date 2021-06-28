import pytest

from nldi_xstool.XSGen import XSGen
from nldi_xstool.ancillary import queryDEMsShape
import py3dep
from pynhd import NLDI
# import xarray as xr
# from matplotlib import pyplot as plt
import json


@pytest.mark.parametrize(
                            'gage, gage_name, res, ny, width',
                            [
                                ("USGS-06888500", 'MILL C NR PAXICO, KS', 3, 100, 200),
                                ("USGS-06721000", 'SOUTH PLATTE RIVER AT FORT LUPTON, CO.', 10, 100, 200),
                                ("USGS-06759500", 'SOUTH PLATTE RIVER AT FORT MORGAN, CO.', 1, 100, 200)
                            ]
                        )
def test_get_gagexs(gage, gage_name, res, ny, width):
    gageloc = NLDI().getfeature_byid("nwissite", gage).to_crs('epsg:3857')
    cid = gageloc.comid.values.astype(str)
    # print(cid, gageloc.comid.values.astype(int)[0])
    strmseg_loc = NLDI().getfeature_byid("comid", cid[0]).to_crs('epsg:3857')
    xs = XSGen(point=gageloc, cl_geom=strmseg_loc, ny=ny, width=width)
    xs_line = xs.get_xs()
    spline = xs.get_strm_seg_spline()
    print(spline)
    t1 = (xs_line.total_bounds) + ((-100., -100., 100., 100.))
    xs_line_geom = xs_line.to_crs('epsg:4326')
    bbox = xs_line_geom.geometry[0].envelope.bounds
    query = queryDEMsShape(bbox)
    # print(query)
    query_text = json.dumps(query)
    print(query_text)

    x, y = xs.get_xs_points()
    dem = py3dep.get_map("DEM", tuple(t1), resolution=res, geo_crs="EPSG:3857", crs="epsg:3857")
    dsi = dem.interp(x=('z', x), y=('z', y))
    vals = dsi.values
    if ny % 2 == 0:
        ny += 1

    assert(len(vals) == ny)
    assert(vals.dtype == float)
