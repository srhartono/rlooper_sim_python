import argparse
import os
import sys
import logging
import pandas as pd
import simulation

currentDir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(currentDir)

def parseArgv():
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    parser = argparse.ArgumentParser(description='R-loop Peak Simulator')
    parser.add_argument('-i','--fasta', type=str, help='Path to the FASTA file')
    parser.add_argument('-s','--sigma', type=float, help='sigma value [0.07]')
    parser.add_argument('-a','--a', type=float, help='a value [10]')
    args = parser.parse_args()

    if args.fasta:
        fastaFile = args.fasta
        logger.info(f' fastaFile: {fastaFile}')
    if args.sigma:
        sigma = args.sigma
        logger.info(f' sigma: {sigma}')
    if args.a:
        a = args.a
        logger.info(f' a: {a}')
    mysim = simulation.simulation_params()
    mysim.setFastaFile(args.fasta)
    mysim.setSigma(args.sigma)
    mysim.seta(args.a)

    return(mysim)


def main():
    mysim = parseArgv()
    myres = simulation.simulation_main(mysim)
    print(myres)

main()







