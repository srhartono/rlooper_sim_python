import os
import sys
import logging
import model
import gene
import math
from math import pi
import pandas as pd
import numpy as np
from numpy import random
from numpy.random import choice

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class energyTable:

	df = pd.DataFrame()

	def parseEnergyTable(self,energyFile):
		energyTable.df = pd.read_table(energyFile, delimiter=',')
				
	def getEnergy(self,n1, n2):
		t0 = energyTable.df
		t1 = t0[t0['n1'] == n1]
		t2 = t1[t1['n2'] == n2]
		energy = t2['energy']
		if len(energy) == 0:
			return(0)
		else:
			return(energy.values[0])
	
class simulation_params():
	fasta_file = "example.fasta"
	minlength = 2
	dynamic_window_size = 15
	reverse_flag = False
	complement_flag = False
	power_threshold = 1
	circular_flag = False
	auto_domain_size = False
	import_flag = False
	top = 0
	dump = False
	average_g = True  # or False
	seed = 0
	dynamic_flag = False
	naive_flag = False
	verbose_flag = False
	orig_flag = False
	def setFastaFile(self,filename):
		self.fasta_file = filename
	def getFastaFile(self):
		return(self.fasta_file)
		
def naive_forloop_rlooper(sequence, model, start, stop, structure, bp_energy, verbose):

	myres = pd.DataFrame()
	df = energyTable()
	df.parseEnergyTable('energy.csv')
	
	Gsigma = list()
	for m in range(0, len(sequence)):
		mact = m
		if (m != 0):
			mact = m + 1

		Gsigma.append((2 * (pi**2) * model.getC() * model.getK() * (model.getAlpha() + mact * model.getA())**2) / (4 * (pi**2) * model.getC() + model.getK() * mact))

	n1 = list()
	n2 = list()
	Gsigmas = list()
	Gbps = list()
	Gs = list()
	bfs = list()
	myindex = 0
	bftotal = 0.0
	Gs_m0 = (0 + 0 + Gsigma[0])
	bf_m0 = math.exp(-1 * Gs_m0 / (0.0019858775 * model.getT()))

	mya = model.geta()

	for n in range(start, 5):
		Gbp = 0.0
		if n % 10 == 0:
			logger.info(f"n: {n}, bftotal: {bftotal}")
	
		if n == 0:
			Gs.append(Gs_m0)
			bfs.append(bf_m0)
			bftotal = bftotal + bf_m0
			n1.append(n)
			n2.append(m)
			Gsigmas.append(Gsigma[m])
			Gbps.append(0.0)
			myindex = myindex + 1
		
		for m in range(0, len(sequence)-n-1):
			if m > model.getMaxLength():
				break
			curr_a = mya
			
			if n >= model.getnick() and n + m >= model.getnick() + model.getSelffoldlen():
				Gbp += df.getEnergy(sequence[n+m],sequence[m+1])
				
			if n >= model.getnick() and n < model.getnick() + model.getnicklen():
				curr_a = 0
						

			n1.append(sequence[n])
			n2.append(sequence[n+m+1])
			
			Gbps.append(Gbp)
			Gsigmas.append(Gsigma[m+1])
			G = curr_a + Gbp + Gsigma[m+1]
			Gs.append(G)
			currbf = math.exp(-1 * (G) / (0.0019858775 * model.getT()))
			bfs.append(currbf)
			bftotal += currbf


			myres2 = pd.DataFrame.from_dict({'index': [myindex],'n': [n], 'm': [m], 'Gsigma': [Gsigma[m+1]], 'Gbp': [Gbp], 'a': [curr_a], 'G': [G], 'bf': [currbf]})
			
			if n == 0 and m == 0:
				myres = myres2
			else:	
				myres = pd.concat([myres,myres2])
				
			myindex = myindex + 1
			
	myres['probability'] = myres['bf'] / bftotal

	
	return(myres)

def simulation_main(mysim):
	logger.info("Simulation main function")
	logger.info(mysim.fasta_file)
	mymodel = model.rloop_model()
	mygene = gene.Gene()
	mygene.loadFromFasta(mysim.getFastaFile())
	mygene.printGene()
	logger.info("Model parameters:")
	logger.info(f"N: {mymodel.N}, sigma: {mymodel.sigma}, A: {mymodel.A}, C: {mymodel.C}, T: {mymodel.T}")
	myres = naive_forloop_rlooper(mygene.getSequence(), mymodel, 0, mygene.getLength(), [], -1.0, True)
	myres.index = np.arange(0,len(myres))
	simpeak(myres,50,mygene.gene_name)
	printout(myres)

def simpeak(myres, npeak,gene_name):
	if len(myres) == 0:
		return(None)

	randomindex = choice(myres.index, size=npeak, p=myres['probability']/myres['probability'].sum(), replace=True)
	print(randomindex)
	peaks = myres.loc[randomindex, :]
	peaks['start'] = peaks['n']
	peaks['end'] = peaks['n'] + peaks['m'] + 1
	peaks['chr'] = gene_name
	peaks.sort_values(by=['chr','start','end'], ascending=True, inplace=True)
	peaks['strand'] = '+'
	open("rlooper_peaks.csv", "w").write(peaks[['chr','start','end','probability','m','strand']].to_csv(sep="\t",index=False))

def printout(myres):
	open("rlooper_output.csv", "w").write(myres.to_csv(sep="\t",index=False))
	return

