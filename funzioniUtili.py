import numpy as np

#--------------------------------------------------------------------------------------------------------

def stampaDataset(inputDataset: list):
    for i, traiettoria in enumerate(inputDataset):
        print("\n" f"Traiettoria {i + 1}: \n")
        
        stato_vero = traiettoria[0]
        misure = traiettoria[1]
        print(f"Stato vero della traiettoria: {stato_vero}")
        print(f"Misure della traiettoria: {misure}")
        print()


            
    # Quando vedi "..." nella lista degli stati veri, significa che ci sono altri stati intermedi tra
    # le posizioni mostrate. Questo è comune quando si tratta di dati di traiettorie, dove le posizioni
    # possono essere campionate a intervalli regolari nel tempo e i punti intermedi non vengono
    # esplicitamente registrati per ridurre la dimensione del dataset.

#--------------------------------------------------------------------------------------------------------

def creaScenario(numTraiettorie: int, inputDataset: list):
    #creo l'array di indici delle numTraiettorie traiettorie selezioante casualmente, da 0 a 49
    traiettorieSelezionate = np.random.choice(len(inputDataset), numTraiettorie, replace=False)
    print("Indici traiettorie selezionate:", traiettorieSelezionate)
    
    #np.random.choice(len(inputDataset), numTraiettorie, replace=False): Questa parte del codice utilizza
    #la funzione np.random.choice di NumPy per selezionare casualmente numTraiettorie indici compresi
    #tra 0 e len(inputDataset) - 1. Questi indici rappresentano le posizioni delle traiettorie
    #all'interno dell'inputDataset. L'argomento replace=False garantisce che gli indici selezionati
    #siano unici, ovvero che non ci siano traiettorie duplicate nel risultato.

    #stampo le traiettorie selezionate in ordine rispetto a come sono stati messi gli indici nell'array
    print("Traiettorie selezionate:")
    try:
        # Lista per memorizzare le traiettorie selezionate
        traiettorie_selezionate = []
        
        for i, iTraiettoria in enumerate(traiettorieSelezionate):
            print(f"Traiettoria {i + 1}: {iTraiettoria}-esima")
            traiettoria = inputDataset[iTraiettoria]
            
            # Aggiungi la traiettoria alla lista delle traiettorie selezionate
            traiettorie_selezionate.append(traiettoria)
    except Exception as e:
        print("Errore durante la creazione dello scenario:", e)

    #per verificare che ne stampo effettivamente il numero passato alla funzione
    print("Numero di traiettorie selezionate:", len(traiettorieSelezionate))
    
    # Restituisci la lista delle traiettorie selezionate
    return traiettorie_selezionate
