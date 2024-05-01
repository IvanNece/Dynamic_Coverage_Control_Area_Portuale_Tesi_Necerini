import pickle
import sys

from createTheSet import printDataset, buildTheSet, plotTrajectories

#---------------------------------------------------------------------------------------------------------

def main():
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
            
        numTargets = 10
        createdDatasetOfTargets = buildTheSet(numTargets, inputDataset)
        printDataset(createdDatasetOfTargets)
        plotTrajectories(createdDatasetOfTargets, plotDir="selectedTrajectories.png")
        
        # Ripristina l'output standard
        sys.stdout = original_stdout
        
    
#---------------------------------------------------------------------------------------------------------

if __name__ == "__main__":
    main()