# Python script to convolve images with a PSF, add noise, and strech and export the images as JPEGS to train the model on. Modified from: https://github.com/aritraghsh09/GalaxySim.


import numpy as np
import tqdm
from astropy.io import fits
from multiprocessing import Pool
from astropy.convolution import convolve
from astropy.visualization import SqrtStretch
from astropy.visualization import PercentileInterval
from PIL import Image

dataReadPath = './SDSSNormal/'
dataWritePath = './SDSSNormalFinal/'
psfFilePath = './psf.fits'
noiseFilePath = ''

NUM_FILES_TOTAL = 55000
NUM_THREADS = 15
IMG_WIDTH = IMG_HEIGHT = 256 

def psf_and_noise(i):
	try:
    #Get image data as an array
		img_data = fits.getdata(dataReadPath+"output_img_"+ str(i)+".fits",memmap=False)
    #Get data from PSF
		psf_data = fits.getdata(psfFilePath, memmap=False)
    #Convolve image with PSF
		convolved_data = convolve(img_data,psf_data,boundary='extend')
    #Add randomized noise
		final_data = convolved_data + np.random.normal(scale = 0.00005 ,size=(IMG_WIDTH,IMG_HEIGHT))
    #Stretch the image, keeping 99.95% of initial pizels.
		strech = SqrtStretch() + PercentileInterval(99.95)
		stretched_image = strech(final_data)
		stretched_image = (255 * stretched_image).astype(np.uint8)
		stretched_image = stretched_image[::-1, :]
		image = Image.fromarray(stretched_image, 'L')
    #Write image
		img_name = dataWritePath + "output " + str(i) + ".jpg"
		image.save(img_name)
	except:
		print("failed")




pl = Pool(NUM_THREADS)
pl.map(psf_and_noise,range(0,NUM_FILES_TOTAL))



