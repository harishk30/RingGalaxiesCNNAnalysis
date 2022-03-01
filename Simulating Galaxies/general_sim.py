# Python script to simulate templates to generate non-ringed galaxies, modified from https://github.com/aritraghsh09/GalaxySim.

from multiprocessing import Pool
import numpy as np
import time

NUM_ITER = 65000    #number of galaxies.
NUM_THREADS = 15    #number of threads available	
FILE_PATH = "/home/harish/Desktop/SDSSNormal/"
IMG_PATH = "/home/harish/Desktop/SDSSNormal/"
#FILE_PATH = IMG_PATH = "./"
	
def file_write(i):

	template_file = open(FILE_PATH + 'galfit_temp_'+str(i),'w')

	template_file.write("===============================================================================\n")

	#File parameters	
	template_file.write("A) gal.fits\n")  # Input data image (FITS file)
	template_file.write("B) "+IMG_PATH+"output_img_"+str(i)+".fits"+"\n") 
	template_file.write("C) none\n") 
	template_file.write("D) none\n") 
	template_file.write("E) 1\n") 
	template_file.write("F) none\n")
	template_file.write("G) none\n")
	template_file.write("H) 1 256 1 256\n") 
	template_file.write("I) 256 256\n") 
	template_file.write("J) 25.95\n") 
	template_file.write("K) 0.06 0.06\n")
	template_file.write("O) regular\n") 
	template_file.write("P) 1\n\n") 
	
	#Main galaxy

	template_file.write(" 0) sersic\n") #object type
	template_file.write(" 1) "+str(int(x_pos[i]))+" "+str(int(y_pos[i]))+" 0 0\n") #position 
	template_file.write(" 3) "+str(inte_mag[i])+" 0\n") #Integrated Magnitude
	template_file.write(" 4) "+str(half_light_radius[i])+" 0\n")
	template_file.write(" 5) "+str(sersic_idx[i])+" 0\n")#Sersic index n 
	template_file.write(" 6) 0.0000 0\n") 
	template_file.write(" 7) 0.0000 0\n")
	template_file.write(" 8) 0.0000 0\n")
	template_file.write(" 9) "+str(axis_ratio[i])+" 0\n")#axis ratio 
	template_file.write("10) "+str(position_angle[i])+" 0\n")#position angle (PA) 
	template_file.write(" Z) 0\n\n")

	# Sky background
	template_file.write(" 0) sky\n")
	template_file.write(" 1) "+ str(sky_back[i]) +" 0\n") 
	template_file.write(" 2) 0.0000 0\n") 
	template_file.write(" 3) 0.0000 0\n")  
	template_file.write(" Z) 0\n\n") 

	template_file.write("===============================================================================")
	template_file.close()

if __name__ == '__main__':
	
	start_timestamp = time.time()
	
	#Randomize parameter selection
	sersic_idx = np.random.uniform(0.0, 8.0, NUM_ITER)
	half_light_radius = np.random.uniform(50.0,88.0,NUM_ITER)
	axis_ratio = np.random.uniform(0.1,1.0,NUM_ITER)
	position_angle = np.random.uniform(-90.0,90.0,NUM_ITER)
	inte_mag = np.random.uniform(17.0,27.8,NUM_ITER)	
	x_pos = np.random.uniform(121.61, 134.38, NUM_ITER)
	y_pos = np.random.uniform(121.61, 134.38, NUM_ITER)
	sky_back = np.random.uniform(0.001,0.005,NUM_ITER)

	#Store parameters in a file
	para_file = open(FILE_PATH+"sim_para.txt","w") 
	stacked_para = np.column_stack((sersic_idx,half_light_radius,axis_ratio,position_angle,inte_mag,x_pos,y_pos,sky_back))
	np.savetxt(para_file,stacked_para,delimiter=" ",header="sersic_idx R_e axis_ratio PA Inte_Mag x_pos y_pos sky_back",fmt="%.4f")
	para_file.close()

	print( "Parameters generated. Real time taken:- %s seconds\nCreating Files....." %(time.time() - start_timestamp) )

	pl = Pool(NUM_THREADS)
	pl.map(file_write,range(0,NUM_ITER)) 
	
	print("Finished.Real Time of Execution:- %s seconds" % (time.time() - start_timestamp) )
