"""
File: 	ILarea.py
Author:	Jack Fawdon 
Date:	2021-06-01
----------------------
This program truncates and subtracts the baseline Raman spectra.
"""

import matplotlib.pyplot as plt
import numpy as np
from numpy import linspace
import os
from scipy import integrate, special
from lmfit import Model, Parameters, minimize, fit_report
import matplotlib.cm as cm
from cycler import cycler
import operator
from natsort import natsorted
import itertools

#exponentially modified gaussian function

def gaussmod(x, y0, A, t0, w, xc):
    return y0 + A/t0 * np.exp(0.5*(w/t0)**2-(x-xc)/t0)*(special.erf(((x-xc)/w - w/t0)/np.sqrt(2))+1)/2

src_dir = input("Please type the full path to the input directory or input file : ").strip()
distance = input("How many steps?").strip()
step_size = input("What was the step size?").strip()


#lists of the concentration values and distance after fitting

conc_values = []
distance_list = []


x = 0
y = 0
while x < int(distance):
	s = int(step_size)*y
	distance_list.append(s)
	x = x+1
	y = y+1


#importing data

i = 0
all_txt_files = natsorted(os.listdir(src_dir))
for txt in all_txt_files: 
	if txt.endswith(".txt") and "conc_gradient" not in txt:
		data = np.loadtxt(src_dir+'/'+txt)
		xdata=data[:,0]
		ydata=data[:,1]

		#truncate spectra

		index=[] 
		for ind, val in enumerate(xdata):
			if 680 <= val <= 800:
				index.append(ind)

			ydata_trunc = ydata[index]
			xdata_trunc = xdata[index]

		#fitting of truncated data

		gmodel = Model(gaussmod)

		params = Parameters()
		params.add('y0', value=10000, vary=True) #min=100000, max=300000)
		params.add('A', value=36e5, vary=True) 
		params.add('t0', value=11.2, vary=True)
		params.add('w', value=11.5, vary=True) 
		params.add('xc', value=732, vary=True) 
		result = gmodel.fit(ydata_trunc, params, x=xdata_trunc, weights=np.sqrt(1.0/ydata_trunc))
		color = cm.winter(np.linspace(0,1,5))
		plt.rc('axes', prop_cycle=(cycler('color', color)))

		
		#plt.plot(xdata_trunc, ydata_trunc, 'o')
		##plt.plot(xdata_trunc, result.best_fit, 'o', label = "Fitted Curve")
		plt.xlabel('Distance / um')
		plt.ylabel('Concentration / $moldm^-3$')

		
		#specifying the fitted function

		x_eval = linspace(680, 800, 5000)
		y_eval = gmodel.eval(result.params, x=x_eval)
		"""plt.plot(x_eval, y_eval)
		plt.show()"""

		#find the x at max height of the fitted function

		max_value = np.max(y_eval)
		max_index = np.where(y_eval == max_value)
		max_wavenumber = x_eval[max_index]

		#convert to concentration using calibration curve values

		a = -0.6078
		b = 9.17847
		c = 724.034

		concentration = (-b+(np.sqrt(b**2-(4*a*(c-max_wavenumber)))))/(a*2)
		concentration1 = concentration.tolist()
		conc_values.append(concentration1)
		i+1


#convert list of lists into a list

conc_values1 = list(itertools.chain(*conc_values))

plt.plot(distance_list, conc_values1)

print(conc_values1)

plt.show()

#write file into a .txt file of concentrations and distance

newfilename = 'conc_gradient.txt'
with open(src_dir+'/'+newfilename,'w') as p:
	for j in range(len(distance_list)):
		p.write(str(distance_list[j]))
		p.write('\t')
		p.write(str(conc_values1[j]))
		p.write('\n')

#print(result.fit_report())