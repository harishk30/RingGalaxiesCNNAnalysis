# Python script to simulate templates to generate ringed galaxies, modified from https://github.com/aritraghsh09/GalaxySim to simulate ringed galaxies.

from multiprocessing import Pool
import numpy as np
import time
import tqdm

NUM_ITER = 100000  # number of galaxies.
NUM_THREADS = 15  # number of threads available
FILE_PATH = "/home/harish/Desktop/images/"
IMG_PATH = "/home/harish/Desktop/images/"

def file_write(i):
    template_file = open(FILE_PATH + 'galfit_temp_' + str(i), 'w')

    template_file.write("===============================================================================\n")

    # File parameters
    template_file.write("A) gal.fits\n")  
    template_file.write("B) " + "output_img_" + str(i) + ".fits" + "\n")  
    template_file.write("C) none\n") 
    template_file.write("D) none\n") 
    template_file.write("E) 1\n")  
    template_file.write("F) none\n")
    template_file.write("G) none\n")
    template_file.write("H) 1 256 1 256\n")  
    template_file.write("I) 256 256\n") 
    template_file.write("J) 21.2\n")  
    template_file.write("K) 0.06 0.06\n") 
    template_file.write("O) regular\n")  
    template_file.write("P) 1\n\n") 

    # Outer ring component, without truncation
  
    template_file.write(" 0) sersic\n")  # object type
    template_file.write(" 1) " + str(int(x_pos[i])) + " " + str(int(y_pos[i])) + " 0 0\n")  # position x y
    template_file.write(" 3) " + str(inte_mag[i]) + " 0\n")  # Integrated Magnitude
    template_file.write(" 4) " + str(half_light_radius[i]) + " 0\n")  # R_e (half-light radius)  
    template_file.write(" 5) " + str(sersic_idx[i]) + " 0\n")
    template_file.write(" 6) 0.0000 0\n")
    template_file.write(" 7) 0.0000 0\n")
    template_file.write(" 8) 0.0000 0\n")
    template_file.write(" 9) " + str(axis_ratio[i]) + " 0\n")  # axis ratio
    template_file.write("10) " + str(position_angle[i]) + " 0\n")  # position angle (PA) 
    template_file.write("Ti) 2\n")
    template_file.write(" Z) 0\n\n")  

    # Truncation Component
  
    template_file.write("T0) radial\n")  # object type
    template_file.write("T4) " + str(break_rad[i]) + " 0\n")
    template_file.write("T5) " + str(trunc_radius[i]) + " 0\n")
    template_file.write("T9) " + str(trunc_ab[i]) + " 0\n")
    template_file.write("T10) " + str(position_angle[i]) + " 0\n\n") 

    # Inner component of ring.
  
    template_file.write(" 0) sersic\n")  # object type
    template_file.write(" 1) " + str(int(x_pos_2[i])) + " " + str(int(y_pos_2[i])) + " 0 0\n")  # position x y
    template_file.write(" 3) " + str(inte_mag_2[i]) + " 0\n")  # Integrated Magnitude
    template_file.write(" 4) " + str(half_light_radius_2[i]) + " 0\n")  # R_e (half-light radius)   [pix]
    template_file.write(" 5) " + str(sersic_idx_2[i]) + " 0\n")  # Sersic index n (de Vaucouleurs n=4)
    template_file.write(" 6) 0.0000 0\n")
    template_file.write(" 7) 0.0000 0\n")
    template_file.write(" 8) 0.0000 0\n")
    template_file.write(" 9) " + str(axis_ratio_2[i]) + " 0\n")  # axis ratio (b/a)
    template_file.write("10) " + str(position_angle_2[i]) + " 0\n")  # position angle (PA) [deg: Up=0, Left=90]
    template_file.write(" Z) 0\n\n")  # output option (0 = resid., 1 = Don't subtract)

    # Object number 4
    template_file.write(" 0) sky\n")
    template_file.write(" 1) " + str(sky_back[i]) + " 0\n")  # sky background at center of fitting region [ADUs]
    # template_file.write(" 1) 1.3920 0\n") # sky background at center of fitting region [ADUs]
    template_file.write(" 2) 0.0000 0\n")  # dsky/dx (sky gradient in x)
    template_file.write(" 3) 0.0000 0\n")  # dsky/dy (sky gradient in y)
    template_file.write(" Z) 0\n\n")  # output option (0 = resid., 1 = Don't subtract)

    template_file.write("===============================================================================")
    template_file.close()


if __name__ == '__main__':

    start_timestamp = time.time()

    # Randomize parameters of galaxies
  
    # Outer ring
    sersic_idx = np.array([1.7] * NUM_ITER)
    half_light_radius = np.random.uniform(2.0, 6.0, NUM_ITER)
    axis_ratio = np.random.uniform(0.70, 1.0, NUM_ITER)
    position_angle = np.random.uniform(-90.0, 90.0, NUM_ITER)
    inte_mag = np.random.uniform(15.0, 25.0, NUM_ITER)
    x_pos = np.random.uniform(121.61, 134.38, NUM_ITER)
    y_pos = np.random.uniform(121.61, 134.38, NUM_ITER)

    # Truncation of ring
    break_rad = np.random.uniform(40, 60, NUM_ITER)
    trunc_radius = np.random.uniform(24, 34, NUM_ITER)
    trunc_ab = np.random.uniform(0.7, 0.9, NUM_ITER)

    # Inner section
    sersic_idx_2 = np.array([3.0] * NUM_ITER)
    half_light_radius_2 = np.random.uniform(8.0, 12.0, NUM_ITER)
    axis_ratio_2 = np.random.uniform(0.5, 0.75, NUM_ITER)
    position_angle_2 = -1 * position_angle
    inte_mag_2 = inte_mag + np.random.uniform(-3.2, -6.2, NUM_ITER)
    x_pos_2 = x_pos
    y_pos_2 = y_pos

    sky_back = np.random.uniform(0.001, 0.005, NUM_ITER)

    #Store parameters in a file
    para_file = open(FILE_PATH + "sim_para.txt", "w") 
    stacked_para = np.column_stack((sersic_idx, half_light_radius, axis_ratio, position_angle, inte_mag, x_pos, y_pos,
                                    sersic_idx_2, half_light_radius_2, axis_ratio_2, position_angle_2, inte_mag_2,
                                    x_pos_2, y_pos_2, sky_back))
    np.savetxt(para_file, stacked_para, delimiter=" ",
               header="sersic_idx R_e axis_ratio PA Inte_Mag x_pos y_pos sersic_idx_2 R_e_2 axis_ratio_2 PA_2 Inte_Mag_2 x_pos_2 y_pos_2 sky_back",
               fmt="%.4f")
    para_file.close()

    print("Parameters generated. Real time taken:- %s seconds\nCreating Files....." % (time.time() - start_timestamp))

    pl = Pool(NUM_THREADS)

    for _ in tqdm.tqdm(pl.imap_unordered(file_write, range(0, NUM_ITER)), total=NUM_ITER):
        pass
