# %%
%matplotlib inline
from nldi_xstool.XSGen import XSGen
from nldi_xstool.COGridGen import COGridGen
import py3dep
from pynhd import NLDI, NHDPlusHR, WaterData
import geopandas as gpd
import xarray as xr
import numpy as np
import rasterio
from nldi_xstool.mapper import mapper
import matplotlib.pyplot as plt

# stationid = "09152500"

# flw_up = NLDI().navigate_byid(
#     fsource="nwissite",
#     fid=f"USGS-{stationid}",
#     navigation="upstreamMain",
#     source="flowlines",
#     distance=2)

# flw_dwn = NLDI().navigate_byid(
#     fsource="nwissite",
#     fid=f"USGS-{stationid}",
#     navigation="downstreamMain",
#     source="flowlines",
#     distance=2)

# # reorder so upstream to downstream
# flw_tot =flw_up[::-1].reset_index(drop=True).append(flw_dwn[1:])
# comids = flw_tot['nhdplus_comid'].values.tolist()
# wd_cat = WaterData("catchmentsp")
# catchments = wd_cat.byid("featureid", comids)

# %%
from pathlib import Path
cf = Path('../Data/s2simp.shp')
print(cf.exists())
flw = gpd.read_file('../Data/s2simp.shp')

# %%

flwmain = flw[flw['FID'] == 1]
flwmain
# %%
grd = COGridGen(flwmain, 100, 100, 1000)

# %%
topo = xr.open_rasterio('../Data/test2_sm_df.tif')
xgrd, ygrd = grd.getXYGrid()

# %%
x = xr.DataArray(xgrd, dims="z")
y = xr.DataArray(ygrd, dims="z")
nx, ny = grd.getGridDims()
tx = np.reshape(xgrd, (nx, ny))
ty = np.reshape(ygrd, (nx, ny))
nwg = topo.interp(x=x, y=y)
tz = np.reshape(nwg.values, (nx, ny))
plt.scatter(x,y)
plt.show()
# %%
plt.contourf(tx, ty, tz)

# %%
flw_tot.to_crs("epsg:5071", inplace=True)
flw_tot.plot()
catchments.to_crs("epsg:5071", inplace=True)
catchments.plot()

flw_tot_b = flw_tot.buffer(1000)
minx = min(flw_tot_b.geometry.bounds.minx)
miny = min(flw_tot_b.geometry.bounds.miny)
maxx = max(flw_tot_b.geometry.bounds.maxx)
maxy = max(flw_tot_b.geometry.bounds.maxy)
print(minx, miny, maxx, maxy)

dem = py3dep.get_map( 
    "DEM",
    tuple((minx, miny, maxx, maxy)), 
    resolution=10, 
    geo_crs="epsg:5071", 
    crs="epsg:5071")

grid = COGridGen(
    cl_geom=flw_tot,
    nx=20,
    ny=30,
    width=1000
)

tmp=0
# %%
