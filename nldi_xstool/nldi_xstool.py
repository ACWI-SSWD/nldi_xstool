"""Main module."""
# from nldi_xstool.cli import XSAtEndPts
from nldi_xstool.PathGen import PathGen
from nldi_xstool.XSGen import XSGen
import requests
# import json
import py3dep
from pynhd import NLDI
# import xarray as xr
# from matplotlib import pyplot as plt
from shapely.geometry import Point, LineString
import geopandas as gpd
import pandas as pd
import numpy as np
# import os.path as path


class HPoint(Point):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __hash__(self):
        return hash(tuple(self.coords))


def dataframe_to_geodataframe(df, crs):
    geometry = [HPoint(xy) for xy in zip(df.x, df.y)]
    df = df.drop(['x', 'y'], axis=1)
    gdf = gpd.GeoDataFrame(df, geometry=geometry, crs=crs)
    return gdf


def getXSAtEndPts(path, numpts, crs, file=None, res=10):
    """[summary]

    Args:
        path ([type]): [description]
        numpts ([type]): [description]
        crs ([type]): [description]
        file ([type], optional): [description]. Defaults to None.

    Returns:
        [type]: [description]
    """
    lnst = []
    for pt in path:
        # print(pt[0], pt[1])
        # x.append(pt[0])
        # y.append(pt[1])
        lnst.append(Point(pt[0], pt[1]))
    # ls1 = LineString(lnst)
    # print(ls1)
    d = {'name': ['xspath'], 'geometry': [LineString(lnst)]}
    gpd_pth = gpd.GeoDataFrame(d, crs=crs)
    # print(gpd_pth)
    # gpd_pth.set_crs(epsg=4326, inplace=True)
    gpd_pth.to_crs(epsg=3857, inplace=True)
    # print(gpd_pth)
    xs = PathGen(path_geom=gpd_pth, ny=numpts)
    xs_line = xs.get_xs()
    # print(xs_line.head())
    # print(xs_line.total_bounds, xs_line.bounds)
    bb = xs_line.total_bounds - ((100., 100., -100., -100.))
    # print('before dem', bb)
    dem = py3dep.get_map("DEM", tuple(bb), resolution=res,
                         geo_crs="EPSG:3857", crs="epsg:3857")

    # print('after dem')
    x, y = xs.get_xs_points()
    dsi = dem.interp(x=('z', x), y=('z', y))
    x1 = dsi.coords['x'].values - dsi.coords['x'].values[0]
    y1 = dsi.coords['y'].values - dsi.coords['y'].values[0]
    dist = np.hypot(x1, y1)
    pdsi = dsi.to_dataframe()
    pdsi['distance'] = dist

    # gpdsi = gpd.GeoDataFrame(pdsi, gpd.points_from_xy(pdsi.x.values, pdsi.y.values))
    gpdsi = dataframe_to_geodataframe(pdsi, crs='epsg:3857')
    # gpdsi.set_crs(epsg=3857, inplace=True)
    gpdsi.to_crs(epsg=4326, inplace=True)
    if(file):
        if not isinstance(file, str):
            # with open(file, "w") as f:
            file.write(gpdsi.to_json())
            file.close()
            return 0
        else:
            with open(file, "w") as f:
                f.write(gpdsi.to_json())
                f.close()
        # gpdsi.to_file(file, driver="GeoJSON")
            return 0
    else:
        return gpdsi


def getXSAtPoint(point, numpoints, width, file=None, res=10):
    """[summary]

    Args:
        point ([type]): [description]
        numpoints ([type]): [description]
        width ([type]): [description]
        file ([type], optional): [description]. Defaults to None.

    Returns:
        [type]: [description]
    """

    # tpoint = f'POINT({point[1]} {point[0]})'
    df = pd.DataFrame({'pointofinterest': ['this'],
                       'Lat': [point[1]],
                       'Lon': [point[0]]})
    gpd_pt = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df.Lon, df.Lat))
    gpd_pt.set_crs(epsg=4326, inplace=True)
    gpd_pt.to_crs(epsg=3857, inplace=True)
    comid = getCIDFromLatLon(point)
    # print(f'comid = {comid}')
    strm_seg = NLDI().getfeature_byid("comid", comid).to_crs('epsg:3857')
    xs = XSGen(point=gpd_pt, cl_geom=strm_seg, ny=numpoints, width=width)
    xs_line = xs.get_xs()
    # print(comid, xs_line)
    # get topo polygon with buffer to ensure there is enough topography to interpolate xs line
    # With coarsest DEM (30m) 100. m should
    bb = xs_line.total_bounds - ((100., 100., -100., -100.))
    dem = py3dep.get_map("DEM", tuple(bb), resolution=res,
                         geo_crs="EPSG:3857", crs="epsg:3857")
    x, y = xs.get_xs_points()
    dsi = dem.interp(x=('z', x), y=('z', y))
    x1 = dsi.coords['x'].values - dsi.coords['x'].values[0]
    y1 = dsi.coords['y'].values - dsi.coords['y'].values[0]
    dist = np.hypot(x1, y1)
    pdsi = dsi.to_dataframe()
    pdsi['distance'] = dist

    # gpdsi = gpd.GeoDataFrame(pdsi, gpd.points_from_xy(pdsi.x.values, pdsi.y.values))
    gpdsi = dataframe_to_geodataframe(pdsi, crs='epsg:3857')
    # gpdsi.set_crs(epsg=3857, inplace=True)
    gpdsi.to_crs(epsg=4326, inplace=True)
    if(file):
        if not isinstance(file, str):
            # with open(file, "w") as f:
            file.write(gpdsi.to_json())
            file.close()
            return 0
        else:
            with open(file, "w") as f:
                f.write(gpdsi.to_json())
                f.close()
        # gpdsi.to_file(file, driver="GeoJSON")
            return 0
    else:
        return gpdsi


def lonlatToPoint(lon, lat):
    return Point(lon, lat)


def getCIDFromLatLon(point):
    # print(point)
    pt = lonlatToPoint(point[0], point[1])
    location = pt.wkt
    location = f'POINT({point[0]} {point[1]})'
    baseURL = 'https://labs.waterdata.usgs.gov/api/nldi/linked-data/comid/position?f=json&coords='
    url = baseURL+location
    # print(url)
    response = requests.get(url)
    jres = response.json()
    comid = jres['features'][0]['properties']['comid']
    return comid
