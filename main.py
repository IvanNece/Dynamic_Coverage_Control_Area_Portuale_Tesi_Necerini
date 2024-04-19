import pickle

from funzioniUtili import stampaDataset, creaScenario, plotTraiettorie

#---------------------------------------------------------------------------------------------------------

def main():
    #apro il file pickle per ottenere le 50 traiettorie
    try:
        with open("dataset.pkl", "rb") as f:
            inputDataset = pickle.load(f)
            print('Dataset caricato correttamente')
    except Exception as e:
        print("Errore durante il caricamento del dataset:", e)
        
    #creo uno scenario con 10 traiettorie casuali
    datasetCreato = creaScenario(10, inputDataset)
    stampaDataset(datasetCreato)
    plotTraiettorie(datasetCreato, destStampa = "traiettorieSelezionate.png")
    
#---------------------------------------------------------------------------------------------------------

if __name__ == "__main__":
    main()