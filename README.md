# Analysis of Ring Galaxies Detected Using Deep Learning with Real and Simulated Data
A Convolutional Neural Network to identify Ring Galaxies, code to simulate ringed galaxies via GalFit, code to download galaxy images from catalogs, and a SED Fitting pipeline for galaxies given their photometry in 11 bands. 

## Data Download

Downloading images from the PANSTARRS survey which are not in the range covered by SDSS DR7, downloading images of ringed galaxies while sufficently iterating resolution, and downloading the photometric data for galaxies (VizieR photometric interface from: https://gist.github.com/mfouesneau/6caaae8651a926516a0ada4f85742c95). 

## SED Fitting

A pipeline which uses the BAGPIPES library to fit a SED to galaxies from photometric data in 11 bands, and estimate properties from this.

## Simulated Model

Three different models which were trained and compared on the simulated data (Inception ResNet V2 had the best metrics).

## Simulating Galaxies

Code to generate GalFit template files to generate ringed and non-ringed galaxies, run GalFit on these template files, convolve the images with a PSF, add noise, strech them, and export as a JPEG. Code modified from https://github.com/aritraghsh09/GalaxySim. 

## Transfer Learn

Inception ResNet V2 model trained on simulated data transfer learnt onto real data. Three models tested and compared, one with no transfer learning at all, one retraining only the output layers, and one retraining convolutional block C and the output layers (this was found to have the best metrics, and also has the code which was used to apply this model on unclassified data). 

## GAN

Three GAN architectures tested out for generating ring images and data augmentation.
