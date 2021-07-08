from nldi_xstool.XSGen import XSGen
from nldi_xstool.ancillary import queryDEMsShape
import py3dep
from pynhd import NLDI


gagebasin = NLDI().get_basins("06721000").to_crs('epsg:3857')
gageloc = NLDI().getfeature_byid("nwissite", "USGS-06721000").to_crs('epsg:3857')
cid = gageloc.comid.values.astype(str)
print(cid, gageloc.comid.values.astype(int)[0])
# strmseg_basin = NLDI().getfeature_byid("comid", cid[0], basin=True).to_crs('epsg:3857')
strmseg_loc = NLDI().getfeature_byid("comid", cid[0]).to_crs('epsg:3857')

xs = XSGen(point=gageloc, cl_geom=strmseg_loc, ny=101, width=1000)
xs_line = xs.get_xs()

xs_line_geom = xs_line.to_crs('epsg:4326')
print(xs_line_geom)
bbox = xs_line_geom.geometry[0].envelope.bounds
print(bbox)
query = queryDEMsShape(bbox)
print(query)

t1 = (xs_line.total_bounds) + ((-100., -100., 100., 100.))
dem = py3dep.get_map("DEM", tuple(t1), resolution=10, geo_crs="EPSG:3857", crs="epsg:3857")

tmp = 0
