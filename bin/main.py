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

    if len(sys.argv) > 1:
        fastasFile= sys.argv[1]
        logger.info(f' fastaFile: {fastasFile}')
    else:
        logger.info(f' Usage: {sys.argv[0]} <fastaFile>\n')
        exit(1)

    return(fastasFile)
    

def main():
    fastaFile = parseArgv()
    mysim = simulation.simulation_params()
    mysim.setFastaFile(fastaFile)
    myres = simulation.simulation_main(mysim)
    print(myres)

main()







