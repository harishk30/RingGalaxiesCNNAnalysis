#############################################
#   extra_proc.py
#
#   Aritra Ghosh
#
#   This script is meant to do extra processing to all the simulated images -- Convolve with the suitable PSF--add the noise.
############################################

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
IMG_WIDTH = IMG_HEIGHT = 256 #No of pixels length/width -wise in each cutout

def psf_and_noise(i):
	try:
		img_data = fits.getdata(dataReadPath+"output_img_"+ str(i)+".fits",memmap=False)
		psf_data = fits.getdata(psfFilePath, memmap=False)
		convolved_data = convolve(img_data,psf_data,boundary='extend')
		final_data = convolved_data + np.random.normal(scale = 0.00005 ,size=(IMG_WIDTH,IMG_HEIGHT))
		strech = SqrtStretch() + PercentileInterval(99.95)
		stretched_image = strech(final_data)
		stretched_image = (255 * stretched_image).astype(np.uint8)
		stretched_image = stretched_image[::-1, :]
		image = Image.fromarray(stretched_image, 'L')
		img_name = dataWritePath + "output " + str(i) + ".jpg"
		image.save(img_name)
	except:
		print("failed")




pl = Pool(NUM_THREADS)
pl.map(psf_and_noise,range(0,NUM_FILES_TOTAL))

#if you don't want this just replace this with the previous line
#this next line does the same thing as the pool call above, but now with a progress bar
#for _ in tqdm.tqdm(pl.imap_unordered(psf_and_noise,range(0,NUM_FILES_TOTAL)), total=NUM_FILES_TOTAL):
#	pass


