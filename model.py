import os
import sys
import logging 

class rloop_model():

    nick = 0
    nicklen = 1
    selffoldlen=0
    maxLength=2000
    N = 1500 #1500bp is the experimentally determined length of the (-) sc domain after the transcription machinery
    A = 1/10.4 # turns/bp
    C = 1.8 #tortional stiffness of ssDNA winding. (Could be 3.6 for ds or 1.8 for ss winding)
    T = 310
    k = (2200 * 0.0019858775 * T) / N #Hooke's law coefficient: (2200*ideal_gas_constant in kcal/mol*absolute_temp_in_kelvin)/N
    a = 10 #Nucleation Free Energy in Kcals (~3-10.2kCals) 5000
    currSim = 0
    iter = 0
    sigma = -0.07 # measurement of energy upstream of replication domain
    alpha = N*sigma*A # linking difference: topological parameter
    ambient_sigma = sigma
    ambient_alpha = N * A * ambient_sigma
    tx_ambient_sigma = -0.07 #  transcriptional sigma
    tx_ambient_alpha = 0
    tx_alpha = 0
    tx_sigma = 0
    sigma_total = ambient_sigma
    alpha_total = ambient_alpha
    selffoldlen = 0

    def setSelffoldlen(self,length):
        rloop_model.selffoldlen = length
    def getSelffoldlen(self):
        return(rloop_model.selffoldlen)
    
    def setMaxLength(self,length):
        rloop_model.maxLength = length
    def getMaxLength(self):
        return(rloop_model.maxLength)
    
    def seta(self,a):
        rloop_model.a = a
    def geta(self):
        return(rloop_model.a)
    
    def setnick(self,n):
        rloop_model.nick = n
        rloop_model.nicklen = 1
    def getnick(self):
        return(rloop_model.nick)  

    def setnicklen(self,nicklen):
        rloop_model.nicklen = nicklen
    def getnicklen(self):
        return(rloop_model.nicklen)

    def setN(self,N):
        rloop_model.N = N
        rloop_model.setAlpha(rloop_model.N*rloop_model.sigma*rloop_model.A)
        rloop_model.k = (2200 * 0.0019858775 * rloop_model.T) / rloop_model.N
    def getN(self):
        return(rloop_model.N)

    def setSigma(self,s):
        rloop_model.sigma = s
        rloop_model.setAlpha(rloop_model.N*rloop_model.sigma*rloop_model.A)
    def getSigma(self):
        return(rloop_model.sigma)

    def setAlpha(self,a):
        rloop_model.alpha = a
    def getAlpha(self):
        return(rloop_model.alpha)

    def setK(self,k):
        rloop_model.k = k
    def getK(self):
        return(rloop_model.k)

    def setA(self,A):
        rloop_model.A = A
        rloop_model.setAlpha(rloop_model.N*rloop_model.sigma*rloop_model.A)
    def getA(self):
        return(rloop_model.A)

    def setC(self,C):
        rloop_model.C = C
    def getC(self):

        return(rloop_model.C)
    def setT(self,T):
        rloop_model.T = T
        rloop_model.k = (2200 * 0.0019858775 * rloop_model.T) / rloop_model.N
    def getT(self):
        return(rloop_model.T)

    def setSuperhelicty(self,sigma):
        rloop_model.sigma = sigma
        rloop_model.setAlpha(rloop_model.N*rloop_model.sigma*rloop_model.A)
    def getSuperhelicity(self):
        return(rloop_model.sigma)
    
    def join(self,mylist,delim):
        if (delim == None):
            delim = ""
        out = ""
        for i in range(len(mylist)):
            if i == 0:
                out = str(mylist[i])
            else:
                out = out + delim + str(mylist[i])
        return(out)

    def stepForward(self,sequence, b0, b1):
        if (b0 == sequence.end_pos and b1 == sequence.end_pos):
            b0 = sequence.begin_pos
            b1 = b0 + 1
        elif (b0 == sequence.end_pos - 1):
            b1 = sequence.begin_pos
        else:
            b1 = b0 + 1
        return(b0, b1)
    
    def findDistance(self,sequence, b0, b1, structure):
        dist = 0
        if (b1 < b0):
            dist += sequence.__sizeof__() - (b1-b0)
        else:
            dist += (b1-b0)
        return(dist)
        
    


