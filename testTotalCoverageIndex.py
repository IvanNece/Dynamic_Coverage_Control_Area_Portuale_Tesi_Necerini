import numpy as np
import matplotlib.pyplot as plt
import os

#---------------------------------------------------------------------------------------------------------

def plotTotalCoverageIndex(totalCoverageIndex_values: list, plotDir=None):
    plt.figure(figsize=(10, 8))
    
    plt.plot(range(len(totalCoverageIndex_values)), totalCoverageIndex_values, marker='o')
    plt.xlabel('Time')
    plt.ylabel('Total Coverage Index')
    plt.title('Total Coverage Index over Time')
    plt.grid(True)
    
    if plotDir:
        # Ottieni il percorso completo della cartella "Images"
        imageDir = os.path.join(os.getcwd(), "Images")
        # Crea la cartella se non esiste
        os.makedirs(imageDir, exist_ok=True)
        # Salva il grafico nella cartella "Images" con il nome specificato
        plt.savefig(os.path.join(imageDir, plotDir), bbox_inches='tight')
    else:
        plt.show()