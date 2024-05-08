import pickle
import sys

from createTheSetOfTargets import printDataset, buildTheSet, plotTrajectories, plotStartingPointOfTrajectories
from createTheSetOfAgents import generateInitialAgentPositions, plotInitialAgentPositions
from initialCoverageIndices import calculateE_00_0, calculateInitialCoverageIndices, calculateInitialTotalCoverageIndex
from plotMergeFunctions import plotTrajectoriesWithAgentStartPoints, plotAll
from gradient import gradientOfInitialCoverageIndex
from coverageAlgorithm import coverageAlgorithm

#---------------------------------------------------------------------------------------------------------

def main():
    
    #------------------------------------------------------------------------------------------
    # 1, 2.1) CARICO IL DATASET E CREO UNO SCENARIO DI TRAIETTORIE DI TARGET SELZIONATE
    
    # Apri il file per scrivere l'output, nel file txt ci metto le traiettorie selezionate
    with open('outputSetTargets.txt', 'w') as f:
        # Salva l'output standard in una variabile per ripristinarlo successivamente
        original_stdout = sys.stdout
        
        # Redirigi l'output standard verso il file
        sys.stdout = f
        
        try:
            with open("dataset.pkl", "rb") as f:
                inputDataset = pickle.load(f)
                print('Dataset caricato correttamente')
        except Exception as e:
            print("Errore durante il caricamento del dataset:", e)
            
        numTargets = 10 # numero di traittorie selezionate
        duration = 100  # secondi di durata delle traiettorie
        createdDatasetOfTargets = buildTheSet(numTargets, inputDataset, duration)
        printDataset(createdDatasetOfTargets)
        plotTrajectories(createdDatasetOfTargets, plotDir="selectedTrajectories.png")
        
        # Ripristina l'output standard
        sys.stdout = original_stdout
    
    print(f"E' stato creato uno scenario con {numTargets} traiettorie selezionate della durata di "
      f"{duration} secondi. I dettagli dello scenario sono stati salvati "
      f"in 'outputSetTargets.txt'.\n\n")
    
    
    #------------------------------------------------------------------------------------------
    # 2.2) CREO UN GRAFICO DELLE TRAIETTORIE SELEZIONATE, CON SOLO IL LORO PUNTO DI PARTENZA
    
    plotStartingPointOfTrajectories(createdDatasetOfTargets, plotDir="startingPoints.png")
     
     
    #------------------------------------------------------------------------------------------
    # 3) CREO UNO SCENARIO INIZIALE DI AGENTI (DRONI) E CALCOLO GLI INDICI DI COPERTURA A t=0 
    # PER OGNI TARGET
    
    numAgents = 4
    initialAreaSize = 200
    
    # Genera le posizioni iniziali degli agenti
    initialAgentPositions = generateInitialAgentPositions(numAgents, initialAreaSize)
    
    # Stampa le posizioni iniziali degli agenti
    print("\n\nPosizioni iniziali degli agenti:")
    for i, (x, y) in enumerate(initialAgentPositions):
        print(f"Agente {i+1}: x = {x}, y = {y}")
        
    # Plot delle posizioni iniziali degli agenti
    plotInitialAgentPositions(initialAgentPositions, plotDir="initialAgentPositions.png")
    
    # raggio di visione degli agenti (droni)
    r = 300
    # peak sensing quality
    mp = 2
    
    # calcolo E_00_0 come prova, sarebbe E00(0)
    E_00_0 = calculateE_00_0(createdDatasetOfTargets, initialAgentPositions, r, mp)
    
    # adesso devo calcolare gli indici di copertura di ogni target j all'istante t=0
    initialCoverageIndices = calculateInitialCoverageIndices(createdDatasetOfTargets, initialAgentPositions, r, mp)
    print("\n\nINDICI DI COPERTURA INIZIALI E_j AL TEMPO t=0:")
    for i, coverage_index in enumerate(initialCoverageIndices):
        print(f"E_{i}_(0): {coverage_index}")
        
    # ora plotto il grafico delle traiettorie, insieme agli startin point degli agenti
    plotTrajectoriesWithAgentStartPoints(createdDatasetOfTargets, initialAgentPositions, plotDir="trajectoriesWithAgentStartPoints.png")
    
    
    #------------------------------------------------------------------------------------------
    # 4) CALCOLO L'EFFETTIVO INDICE DI COPERTURA COMPLESSIVO ALL'ISTANTE t=0
    
    print("\n")
    lowerboundIndex = 1 #=E*
    # QUESTA PARTE SI PUO' ANCHE COMMENTARE, DATO CHE PASSO TUTTO ALLA FUNZIONE GRADIENTE TANTO
    totalCoverageIndex_0 = calculateInitialTotalCoverageIndex(initialCoverageIndices, lowerboundIndex)
    print(f"\nINDICE DI COPERTURA COMPLESSIVO ALL'ISTANTE t=0: \nE(0): {totalCoverageIndex_0}")
    
    # 4.1) CALCOLO GRADIENTE INDICE DI COPERTURA COMPLESSIVO A t=0, PER OGNI AGENTE i
    initalGradients = gradientOfInitialCoverageIndex(createdDatasetOfTargets, initialAgentPositions, r, mp, lowerboundIndex)
    print("\nGRADIENTE INDICE DI COPERTURA COMPLESSIVO A t=0, PER OGNI AGENTE i:")
    for i, gradient in enumerate(initalGradients):
        print(f"Agente {i+1}: {gradient}")
        
        
    #------------------------------------------------------------------------------------------
    # 5) ALGORITMO
    
    # Passo di salita
    epsilon = 0.1
    agentTrajectories = coverageAlgorithm(createdDatasetOfTargets, initialAgentPositions, r, mp, lowerboundIndex, numAgents, duration, epsilon)
    
    # Stampa le traiettorie degli agenti
    print("\n\nTraiettorie degli agenti:")
    for i, agent_trajectory in enumerate(agentTrajectories):
        print(f"Agente al tempo {i+1}:\n{agent_trajectory}")
    
    plotAll(createdDatasetOfTargets, agentTrajectories, plotDir="finalTrajectories.png")
    
#---------------------------------------------------------------------------------------------------------

if __name__ == "__main__":
    main()