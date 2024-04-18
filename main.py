import pickle

from funzioniUtili import stampaDataset, creaScenario, plotTraiettorie

#---------------------------------------------------------------------------------------------------------

def main():
    try:
        with open("dataset.pkl", "rb") as f:
            inputDataset = pickle.load(f)
            print('Dataset caricato correttamente')
    except Exception as e:
        print("Errore durante il caricamento del dataset:", e)
        
    datasetCreato = creaScenario(10, inputDataset)
    stampaDataset(datasetCreato)
    plotTraiettorie(datasetCreato)
    
#---------------------------------------------------------------------------------------------------------

if __name__ == "__main__":
    main()