import pickle
import sys

from createTheSetOfTargets import printDataset, buildTheSet, plotTrajectories, plotStartingPointOfTrajectories
from createTheSetOfAgents import generateInitialAgentPositions, plotInitialAgentPositions
from calculateCoverageIndices import calculateInitialCoverageIndices

#---------------------------------------------------------------------------------------------------------

def main():
    
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
      f"in 'outputSetTargets.txt'.\n")
    
    print("Il grafico che mostra le traiettorie selezionate è presente in 'selectedTrajectories.png'.\n\n")
    
    
    # 2.2) CREO UN GRAFICO DELLE TRAIETTORIE SELEZIONATE, CON SOLO IL LORO PUNTO DI PARTENZA
    
    plotStartingPointOfTrajectories(createdDatasetOfTargets, plotDir="startingPoints.png")
     
    # 3) CREO UNO SCENARIO INIZIALE DI AGENTI (DRONI)
    
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
    
    # adesso devo calcolare gli indici di copertura di ogni target j all'istante t=0
    initialCoverageIndeces = calculateInitialCoverageIndices(createdDatasetOfTargets, initialAgentPositions)
    
#---------------------------------------------------------------------------------------------------------

if __name__ == "__main__":
    main()