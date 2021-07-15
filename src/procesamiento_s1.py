# Funciones
    # Descriptores
def descr(prod):'''
##########################
## SCRIPT PRUEBA
## subset_region 
#######################
'''

# obr, therm, cal, spk refined lee, multilooking, terrein

import os
os.chdir('./')
import snappy
from snappy import Product
from snappy import ProductIO
from snappy import ProductUtils
from snappy import WKTReader
from snappy import HashMap
from snappy import GPF
import shapefile
import pygeoif
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as colors

# Funciones
    # Descriptores
def descr(prod):
    print("Width: {} px".format(prod.getSceneRasterWidth()))
    print("Height: {} px".format(prod.getSceneRasterHeight()))
    print("Band names: {}".format(", ".join(prod.getBandNames())))

    # Visualizador
def plotBand(prod, band, vmin=0, vmax=100000):
    band = prod.getBand(band)
    w = band.getRasterWidth()
    h = band.getRasterHeight()
    print(w, h)
    band_data = np.zeros(w * h, np.float32)
    band.readPixels(0, 0, w, h, band_data)    
    band_data.shape = h, w    
    width = 12    
    height = 12    
    plt.figure(figsize=(width, height))    
    imgplot = plt.imshow(band_data, cmap=plt.cm.binary.reversed(), vmin=vmin, vmax=vmax)
    return imgplot

    # Apply Orbit 
def orbit(prod, orb_state='Sentinel Precise (Auto Download)', pol_degree=3, not_fail=True):
    parameters = HashMap()
    GPF.getDefaultInstance().getOperatorSpiRegistry().loadOperatorSpis()
    parameters.put('orbitType', orb_state)
    parameters.put('polyDegree', str(pol_degree))
    parameters.put('continueOnFail', str(not_fail))
    output = GPF.createProduct('Apply-Orbit-File', parameters, prod)
    return output
    print('Orbit')

def thermal(prod):
    parameters = HashMap()
    parameters.put('removeThermalNoise', True)
    output = GPF.createProduct('ThermalNoiseRemoval', parameters, prod)
    return output
    print('Thermal Noise Removal')
    
def calibration(prod, out_band='outputSigmaBand',pols='VV,VH', db=False):
    parameters = HashMap()
    parameters.put(out_band, True)
    if pols == 'HH,HV' or pols == 'HV,HH':
        parameters.put('sourceBands', 'Intensity_HH,Intensity_HV')
    elif pols == 'VH,VV' or pols == 'VV,VH':
        parameters.put('sourceBands', 'Intensity_VH,Intensity_VV')
    elif pols == 'HH':
        parameters.put('sourceBands', 'Intensity_HH')
    elif pols == 'VV':
        parameters.put('sourceBands', 'Intensity_VV')
    elif pols == 'HV':
        parameters.put('sourceBands', 'Intensity_HV')
    elif pols == 'VH':
        parameters.put('sourceBands', 'Intensity_VH')
    else:
        print("POLARIZACIÓN EQUIVOCADA")
    parameters.put('selectedPolarisations', pols)
    parameters.put('outputImageScaleInDb', db)
    output = GPF.createProduct("Calibration", parameters, prod)
    return output
    print('Calibration')

def speckle(prod, source_band='Sigma0_VH,Sigma0_VV'):
    parameters = HashMap() 
    parameters.put('sourceBandNames', source_band)
    parameters.put('filter', 'Refined Lee')
    output = GPF.createProduct('Speckle-Filter', parameters, prod)
    return output
    print('Speckle Filtering')

def multilook(prod, source_band='Sigma0_VH,Sigma0_VV', rgLooks=1, azLooks=1, out_intensity=True):
    parameters = snappy.HashMap()
    parameters.put('nRgLooks', rgLooks)
    parameters.put('nAzLooks', azLooks)
    parameters.put('outputIntensity', str(out_intensity))
    parameters.put('sourceBands', source_band)
    output = snappy.GPF.createProduct('Multilook', parameters, prod)
    return output
    print('Multilooking')


def terrain(prod, dem='SRTM 3Sec', re_method='BILINEAR_INTERPOLATION',px_spacing=10, 
             proj='WGS84', source_band='Sigma0_VH,Sigma0_VV'):
    parameters = HashMap()
    parameters.put('demName', dem)
    parameters.put('imgResamplingMethod', 'BILINEAR_INTERPOLATION')
    parameters.put('pixelSpacingInMeter', float(px_spacing))
#    parameters.put('mapProjection', proj)
    parameters.put('sourceBands', source_band)
    output = GPF.createProduct('Terrain-Correction', parameters, prod)
    return output
    print('Terrain Correction')



# Secuencia completa
product = ProductIO.readProduct('data/presas_ags.dim')

product_final = terrain(multilook(speckle(calibration(thermal(orbit(product))))))

ProductIO.writeProduct(product_final, 'data/presas_ags_proc.tiff',  'GeoTIFF')

# Secuencia por pasos
product = ProductIO.readProduct('data/presas_ags.dim')
descr(product)
plotBand(product, "Intensity_VV")
plt.show()

product_Orb = orbit(product)
descr(product_Orb)
plotBand(product_Orb, "Intensity_VV")
plt.show()

product_Orb_Therm = thermal(product_Orb)
descr(product_Orb_Therm)
plotBand(product_Orb_Therm, "Intensity_VV")
plt.show()

product_Orb_Therm_Cal = calibration(product_Orb_Therm)
descr(product_Orb_Therm_Cal)
plotBand(product_Orb_Therm_Cal, "Sigma0_VV", 0, 1)
plt.show()

product_Orb_Therm_Cal_Spkl = speckle(product_Orb_Therm_Cal)
descr(product_Orb_Therm_Cal_Spkl)
plotBand(product_Orb_Therm_Cal_Spkl, 'Sigma0_VV', 0, 1)
plt.show()

product_Orb_Therm_Cal_Spkl_Mlt = multilook(product_Orb_Therm_Cal_Spkl)
descr(product_Orb_Therm_Cal_Spkl_Mlt)
plotBand(product_Orb_Therm_Cal_Spkl, 'Sigma0_VV', 0, 1)
plt.show()

product_Orb_Therm_Cal_Spkl_Mlt_Tc = terrain(product_Orb_Therm_Cal_Spkl_Mlt)
#plotBand(product_Orb_Therm_Cal_Spkl_Mlt_Tc, 'Sigma0_VV', 0, 0.1)
plt.show()
