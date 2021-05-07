'''Console script for nldi_xstool.'''
import sys
import click
# import numpy as np
from nldi_xstool.nldi_xstool import getXSAtPoint, getXSAtEndPts
# import geopandas as gpd
# import pandas as pd
# import json

resdict = {'1m': 1, '3m': 3, '5m': 5, '10m': 10, '30m': 30, '60m': 60}


class NLDI_XSTool:
    def __init__(self):
        self.out_crs = 'epsg:4326'

    def setoutCRS(self, out_crs='epsg:4326'):
        self.out_crs = out_crs

    def outCRS(self):
        return self.out_crs

    def __repr__(self):
        return f'NLDI_XSTool {self.out_crs}'


pass_nldi_xstool = click.make_pass_decorator(NLDI_XSTool)


@click.group()
@click.option('--outcrs',
              default='epsg:4326',
              help='Projection CRS to return cross-section geometry: default is epsg:4326')
@click.version_option('0.1')
@click.pass_context
def main(ctx, outcrs):
    '''NLDI_XSTool is a command line tool to for elevation-based services to the NLDI'''

    ctx.obj = NLDI_XSTool()
    ctx.obj.setoutCRS(outcrs)
    return 0

# XS command at point with NHD


@main.command()
@click.option(
                '-f', '--file',
                default=None,
                type=click.File('w'),
                help='enter path and filenmae for json ouput'
             )
@click.option(
                '-ll', '--lonlat',
                required=True,
                type=tuple((float, float)),
                help='format lon,lat (x,y) as floats for example: -103.8011 40.2684'
             )
@click.option(
                '-n', '--numpoints',
                default=101,
                type=int,
                help='number of points in cross-section'
             )
@click.option(
                '-w', '--width',
                default=1000.0,
                type=float,
                help='width of cross-section')
@click.option(
                '-r', '--resolution',
                type=click.Choice(['1m', '3m', '5m', '10m', '30m', '60m'], case_sensitive=False),
                default='10m',
                help='Resolution of DEM used.  Note: 3DEP provides server side interpolatin given best available data'
             )
@click.option(
                '-v', '--verbose',
                default=False,
                type=bool,
                help='verbose ouput'
             )
@pass_nldi_xstool
def XSAtPoint(nldi_xstool, lonlat, numpoints, width, resolution, file, verbose):
    x = lonlat[0]
    y = lonlat[1]
    nl = '\n'
    if verbose:
        print(
                f'input={lonlat}, lat={x}, lon={y}, {nl} \
                npts={numpoints}, width={width}, resolution={resolution}, {nl} \
                crs={nldi_xstool.outCRS()}, {nl} \
                file={file}, {nl} \
                out_epsg={nldi_xstool.outCRS()}'
            )
    # print(tuple(latlon))
    xs = getXSAtPoint(
                        point=tuple((x, y)),
                        numpoints=numpoints,
                        width=width,
                        file=file,
                        res=resdict.get(resolution)
                    )
    if file is None:
        print(xs.to_json())
    return 0

# XS command at user defined endpoints


@main.command()
@click.option('-f', '--file',
              default=None,
              type=click.File('w'),
              help='Output json file')
@click.option('-s', '--startpt',
              required=True,
              type=tuple((float, float)),
              help='format x y pair as floats for example: -103.801134 40.267335')
@click.option('-e', '--endpt',
              required=True,
              type=tuple((float, float)),
              help='format x y pair as floats for example: -103.800787 40.272798 ')
@click.option('-c', '--crs',
              required=True,
              type=str,
              help='spatial reference of input data',
              default='epsg:4326')
@click.option('-n', '--numpoints',
              default=100,
              type=int,
              help='number of points in cross-section')
@click.option(
                '-r', '--resolution',
                type=click.Choice(['1m', '3m', '5m', '10m', '30m', '60m'], case_sensitive=False),
                default='10m',
                help='Resolution of DEM used.  Note: 3DEP provides server side interpolatin given best available data'
             )
@click.option('-v', '--verbose',
              default=False,
              type=bool,
              help='verbose ouput')
@pass_nldi_xstool
def XSAtEndPts(nldi_xstool, startpt, endpt, crs, numpoints, resolution, file, verbose):
    x1 = startpt[0]
    y1 = startpt[1]
    x2 = endpt[0]
    y2 = endpt[1]
    nl = '\n'
    if verbose:
        print(
            f'input:  {nl}, \
            start: {startpt}, {nl}, \
            end: {endpt}, {nl}, \
            x1:{x1}, y1:{y1}, {nl}, \
            x2:{x2}, y2:{y2}, {nl}, \
            npts={numpoints}, {nl}, \
            resolution={resolution}, \
            input_crs={crs}, {nl}, \
            output_crs={nldi_xstool.outCRS()}  {nl}, \
            file={file}, {nl}, \
            verbose: {verbose} '
            )
    path = []
    path.append(startpt)
    path.append(endpt)
    # print(type(path))
    xs = getXSAtEndPts(
                        path=path,
                        numpts=numpoints,
                        res=resdict.get(resolution),
                        crs=crs,
                        file=file
                      )
    if file is None:
        print(xs.to_json())
    return 0


if __name__ == '__main__':
    sys.exit(main())  # pragma: no cover
