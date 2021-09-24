"""
File: 	concentration_plot.py
Author:	Jack Fawdon & Kevin Hurlbutt
Date:	2020-03-31
----------------------
This program converts a series of Raman spectra into a concentration vs. time spectrum.
"""
import os
import numpy as np
import matplotlib.pyplot as plt
from tkinter import Tcl
from scipy import integrate

class Peak():
	"""	class: Peak
		-----------------
		This is the heart of the function. It takes in the path to a text file
		containing the spectroscopic data and writes a file containing a normalized 
		700 cm-1 peak and converted that peak's area into a resulting concentration
	"""
	def __init__(self, path_to_input, dst_dir):
		self.filename = path_to_input
		self.dst_dir = dst_dir
		self.wavenumber = []
		self.intensity = []
		self.normalized = []
		self.truncated = []
		self.wavenumber2 = []
		self.concentration_m = []
		return

	def run(self):
		self.parse()
		self.normalize()
		self.truncate()
		self.write_results()
		#self.plotting()
		self.area()
		return

	def parse(self):
		with open(self.filename, encoding="utf8", errors="ignore") as f:
			for line in f:
				if line.startswith('#'):
					continue
				parts = line.split()
				w = float(parts[0])
				i = float(parts[1])
				self.wavenumber.append(w)
				self.intensity.append(i)
		return


	def normalize(self):
		index = 0
		for ind, val in enumerate(self.wavenumber):
			if val > 1400:
				index = ind
		m = max(self.intensity[:index])
		for i in self.intensity:
			self.normalized.append(i/m)
		return

	def truncate(self):
		index1 = 0
		index2 = 0
		for ind1, val1 in enumerate(self.wavenumber):
			if val1 < 762 and val1 > 758:
				index1 = ind1
			if val1 < 682 and val1 > 678:
				index2 = ind1
			self.truncated = self.normalized[index1:index2]
			self.wavenumber2 = self.wavenumber[index1:index2]
		return

	def area(self):
		
			area_peak = integrate.simps(self.truncated, self.wavenumber2)

			a = -20.46985
			b = -0.6228

			self.concentration_m = (area_peak-b)/a


			#with open(self.dst_dir+'/'+self.filename[self.filename.rfind('/'):-4]+"_concentration.txt", 'w', encoding="utf8", errors="ignore") as f:
				#f.write(str(self.concentration_m))

			return


	def plotting(self):
		plt.plot(self.wavenumber2, self.truncated)
		plt.fill_between(self.wavenumber2, self.truncated, color = "grey",alpha = 0.3, hatch = '|')
		plt.show()
		return


	def write_results(self):
		with open(self.dst_dir+'/'+self.filename[self.filename.rfind('/'):-4]+"_700PEAK.txt", 'w', encoding="utf8", errors="ignore") as f:
			for i in range(len(self.truncated)):
				f.write(str(self.wavenumber2[i]))
				f.write('\t')
				f.write(str(self.truncated[i]))
				f.write('\n')
		return


def main():

	src_dir = input("Please type the full path to the input directory or input file : ").strip()
	dst_dir = input("Please type the full path to the output directory: ").strip() + '/'
	#src_dir = "/Users/jackfawdon 1/Desktop/20190226_0_5m_LiFSI_G4_5x_785nm_static_Copy.txt"
	#dst_dir = "/Users/jackfawdon 1/Desktop/"
	distance = input("How many steps?").strip()
	step_size = input("What was the step size?").strip()


	conctotal=[]
	distance_list = []

	x = 0
	y = 0
	while x < int(distance):
		s = int(step_size)*y
		distance_list.append(s)
		x = x+1
		y = y+1


	if os.path.isdir(src_dir):
		for filename in Tcl().call('lsort', '-dict', os.listdir(src_dir)):
			if filename.endswith(".txt") and "700PEAK" not in filename and "NORMALIZED" not in filename:
				print(filename)
				n = Peak(src_dir+'/'+filename, dst_dir)
				n.run()
				conctotal.append(n.concentration_m)
		with open(src_dir+'/'+"_NORMALIZED_conctotal.txt", 'w', encoding="utf8", errors="ignore") as f:
			for i in range(len(conctotal)):
				f.write(str(distance_list[i]))
				f.write('\t')
				f.write(str(conctotal[i]))
				f.write('\n')

	else:
		n = Peak(path_to_input=src_dir, dst_dir=dst_dir)
		n.run()

	print(conctotal)
	print(distance_list)

	plt.plot(distance_list, conctotal, 'o')
	plt.xlabel('Distance / um')
	plt.ylabel('Concentration / M')
	plt.show()
			
if __name__ == '__main__':
	main()