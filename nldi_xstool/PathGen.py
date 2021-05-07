import numpy as np
from shapely.geometry import LineString, Point
import geopandas as gpd
import pandas as pd


class PathGen:

    def __init__(self, path_geom, ny) -> None:
        # print(path_geom, ny)
        self.path_geom = path_geom
        self.width = self.path_geom.geometry[0].length
        if ny % 2 == 0:
            ny += 1
        self.ny = ny
        self.x = np.zeros(self.ny, dtype=np.double)
        self.y = np.zeros(self.ny, dtype=np.double)
        self.int_path = None
        self._buildpath()

    def _buildpath(self):
        line = self.path_geom.geometry[0]
        spacing = line.length/self.ny
        # print(line, spacing)
        d = 0.0
        index = 0
        while d < self.width and index < self.ny:
            point = line.interpolate(d)
            self.x[index] = point.x
            self.y[index] = point.y
            d += spacing
            index += 1

    def get_xs(self):
        points = gpd.GeoSeries(map(Point, zip(self.x, self.y)))
        ls = LineString((points.to_list()))
        # print(ls)
        d = {0: {'name': 'section-path', 'geometry': ls}}
        df = pd.DataFrame.from_dict(d, orient='index')
        gdf = gpd.GeoDataFrame(df, geometry=df.geometry, crs=self.path_geom.crs)
        return gdf

    def get_xs_points(self):
        return self.x, self.y
