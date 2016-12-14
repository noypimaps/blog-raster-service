from flask import Flask
from osgeo import gdal, osr
from osgeo.gdalconst import GA_ReadOnly
import numpy
import json

app = Flask(__name__)

tiffLoc = "data/raster.tif"

@app.route("/")
def home():
    return "Hello World!"

@app.route("/raster/<float:lng>/<float:lat>/")
def rasterInfo(lng, lat):
    pixelValue = getPixelValue(lng, lat)
    return json.dumps(pixelValue)

def convertCoords(lng, lat):
    """
    Converts the clicked latitude and longitude coordinates
    into an image coordinates using affine transformation.

    Returns:
        pixel coordinates
    """
    pixelPair = []
    # Opens the tiff location
    ds = gdal.Open(tiffLoc)
    # Gets the transformation parameters w/ respect to the tiff
    gt = ds.GetGeoTransform()
    # Gets the coordinate system of the tiff.
    srs = osr.SpatialReference()
    srs.ImportFromWkt(ds.GetProjection())
    srsLatLng = srs.CloneGeogCS()
    ct = osr.CoordinateTransformation(srsLatLng, srs)
    # Transforms the clicked coordinates into the same coordinate
    # system with the tiff
    (x1, y1, holder) = ct.TransformPoint(float(lng), float(lat))
    # Implement affine transformation
    x = (x1 - gt[0]) / gt[1]
    y = (y1 - gt[3]) / gt[5]
    pixelPair.append([int(x), int(y)])
    return pixelPair

def getPixelValue(lng, lat):
    """
    Access the pixel value of a tiff matrix using the pixel coords.
    Returns:
        a python dictionary containing pixel values with bands as keys.
    """
    data = {}
    pixelCoords = convertCoords(lng, lat)[0]
    ds = gdal.Open(tiffLoc)
    x = pixelCoords[0]
    y = pixelCoords[1]
    # Access pixel values of the raster image using numpy.
    # Apply the extraction to all bands
    for b in range(ds.RasterCount):
       # For windowed reading
       data[str(b + 1)] = str(numpy.array(
                ds.GetRasterBand(int(b + 1)).ReadAsArray(x,y,1,1))[0][0])
    return data

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
