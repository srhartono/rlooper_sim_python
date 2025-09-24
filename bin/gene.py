import os
import sys
import logging
import pandas as pd
import structure


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Gene():

    gene_name = "init"
    header = ""
    pos = structure.Loci()
    sequence = list()
    mystruct = structure.Structure()
    ground_state_energy = 0.0

    def parseHeader(self):
        pass
    def getName(self):
        return(Gene.gene_name)
    def setName(self,name):
        Gene.gene_name = name
    def getHeader(self):
        return(Gene.header)
    def setHeader(self,h):
        Gene.header = h
    def getSequence(self):
        return(Gene.sequence)
    def setSequence(self,seq):
        Gene.sequence = seq
    def getPos(self):
        return(Gene.pos)
    def setPos(self,p):
        Gene.pos = p

    def printGene(self):
        logger.info("Gene Name: " + Gene.gene_name)
        logger.info("Header: " + Gene.header)
        logger.info("Position: " + Gene.pos.chromsome + ":" + str(Gene.pos.start_pos) + "-" + str(Gene.pos.end_pos) + " (" + Gene.pos.strand + ")")
        logger.info("Sequence Length: " + str(len(Gene.sequence)))
        logger.info("Sequence: " + ''.join(Gene.sequence[0:10]) + ("..." if len(Gene.sequence) > 10 else ""))
        logger.info("Ground State Energy: " + str(Gene.ground_state_energy))

    def getGroundStateEnergy(self):
        return(Gene.ground_state_energy)
    def setGroundStateEnergy(e):
        Gene.ground_state_energy = e
    
    def computeGCSkew(self):
        return( (Gene.sequence.count('G') - Gene.sequence.count('C')) / (Gene.sequence.count('G') + Gene.sequence.count('C')) 
               if (Gene.sequence.count('G') + Gene.sequence.count('C')) > 0 else 0 
               )
    def computeATSkew(self):
        return( (Gene.sequence.count('A') - Gene.sequence.count('T')) / (Gene.sequence.count('A') + Gene.sequence.count('T')) 
               if (Gene.sequence.count('A') + Gene.sequence.count('T')) > 0 else 0 
               )
    def computeGCContent(self):
        return( (Gene.sequence.count('G') + Gene.sequence.count('C')) / len(Gene.sequence) 
               if len(Gene.sequence) > 0 else 0 
               )
    def computeATContent(self):
        return( (Gene.sequence.count('A') + Gene.sequence.count('T')) / len(Gene.sequence) 
               if len(Gene.sequence) > 0 else 0 
               )
    def reverseComplement(self):
        complement = {'A': 'T', 'T': 'A', 'C': 'G', 'G': 'C', 'N': 'N'}
        return(''.join(complement.get(base, base) for base in reversed(Gene.sequence)))
    def getLength(self):
        return(len(Gene.sequence))
    def extractSubsequence(start, end):
        return(''.join(Gene.sequence[start:end]))
    def loadFromFasta(self,fasta_file):
        with open(fasta_file, 'r') as f:
            lines = f.readlines()
            header = lines[0].strip()
            sequence = ''.join(line.strip() for line in lines[1:])
        gene = Gene()
        gene.setHeader(header)
        gene.setSequence(list(sequence))
        gene.setName(header.split()[0][1:])  # Assuming the first word after '>' is the gene name
        return(gene)

