"""
File: 	ILarea.py
Author:	Jack Fawdon 
Date:	2021-06-01
----------------------
This program truncates and subtracts the baseline Raman spectra.
"""

from BaselineRemoval import BaselineRemoval
import matplotlib.pyplot as plt
import numpy as np
import os
from scipy import integrate

src_dir = input("Please type the full path to the input directory or input file : ").strip()
dst_dir = input("Please type the full path to the output directory: ").strip() + '/'

total_area = []
total_area1 = []
total_area2 = []

j=0
all_txt_files = sorted(os.listdir(src_dir)) #opens source directory
for txt in all_txt_files: 
	if txt.endswith(".txt"):
		data = np.loadtxt(src_dir+'/'+txt)
		x=data[:,0]
		ydata=data[:,1]


		index=[] 
		for ind, val in enumerate(x):
			if 680 <= val <= 800:
				index.append(ind)

			ydata_trunc = ydata[index]
			xdata_trunc = x[index]


		area_peak = integrate.simps(ydata_trunc, xdata_trunc)


		index1=[] 
		for ind1, val1 in enumerate(x):
			if 873 <= val1 <= 932:
				index1.append(ind1)

			ydata_trunc1 = ydata[index1]
			xdata_trunc1 = x[index1]

		area_peak1 = integrate.simps(ydata_trunc1, xdata_trunc1)


		index2=[] 
		for ind2, val2 in enumerate(x):
			if 546 <= val2 <= 615:
				index2.append(ind2)

			ydata_trunc2 = ydata[index2]
			xdata_trunc2 = x[index2]


		area_peak2 = integrate.simps(ydata_trunc2, xdata_trunc2)

		total_area.append(area_peak)
		total_area1.append(area_peak1)
		total_area2.append(area_peak2)
		j+1

print(total_area, total_area1, total_area2)


newfilename = 'area_'+str(txt)
with open(dst_dir+'/'+newfilename,'w') as p:
		p.write(str(total_area))


newfilename = 'area1_'+str(txt)
with open(dst_dir+'/'+newfilename,'w') as p:
		p.write(str(total_area1))

newfilename = 'area2_'+str(txt)
with open(dst_dir+'/'+newfilename,'w') as p:
		p.write(str(total_area2))


