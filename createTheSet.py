import os
import numpy as np
import matplotlib.pyplot as plt

#--------------------------------------------------------------------------------------------------------

def printDataset(inputDatasetToPrint: list):
    for i, trajectory in enumerate(inputDatasetToPrint):
        print("\n" f"Traiettoria {i + 1}: \n")
        
        realState = trajectory[0]
        measurement = trajectory[1]
        print(f"Stato vero della traiettoria: {realState}")
        print(f"Misure della traiettoria: {measurement}")
        print()


            
    # Quando vedi "..." nella lista degli stati veri, significa che ci sono altri stati intermedi tra
    # le posizioni mostrate. Questo è comune quando si tratta di dati di traiettorie, dove le posizioni
    # possono essere campionate a intervalli regolari nel tempo e i punti intermedi non vengono
    # esplicitamente registrati per ridurre la dimensione del dataset.

#--------------------------------------------------------------------------------------------------------

def buildTheSet(numTrajectories: int, inputDataset: list):
    #creo l'array di indici delle numTraiettorie traiettorie selezioante casualmente, da 0 a 49
    selectedTrajectoriesIndex = np.random.choice(len(inputDataset), numTrajectories, replace=False)
    print("Indici traiettorie selezionate:", selectedTrajectoriesIndex)
    
    #np.random.choice(len(inputDataset), numTraiettorie, replace=False): Questa parte del codice utilizza
    #la funzione np.random.choice di NumPy per selezionare casualmente numTraiettorie indici compresi
    #tra 0 e len(inputDataset) - 1. Questi indici rappresentano le posizioni delle traiettorie
    #all'interno dell'inputDataset. L'argomento replace=False garantisce che gli indici selezionati
    #siano unici, ovvero che non ci siano traiettorie duplicate nel risultato.

    #stampo le traiettorie selezionate in ordine rispetto a come sono stati messi gli indici nell'array
    print("Traiettorie selezionate:")
    try:
        # Lista per memorizzare le traiettorie selezionate
        selectedTrajectories = []
        
        for i, iTraiettoria in enumerate(selectedTrajectoriesIndex):
            print(f"Traiettoria {i + 1}: {iTraiettoria}-esima")
            traiettoria = inputDataset[iTraiettoria]
            
            # Aggiungi la traiettoria alla lista delle traiettorie selezionate
            selectedTrajectories.append(traiettoria)
    except Exception as e:
        print("Errore durante la creazione dello scenario:", e)

    #per verificare che ne stampo effettivamente il numero passato alla funzione
    print("Numero di traiettorie selezionate:", len(selectedTrajectories))
    
    # Restituisci la lista delle traiettorie selezionate
    return selectedTrajectories

#--------------------------------------------------------------------------------------------------------

def plotTrajectories(dataset, plotDir = None):
    plt.figure(figsize=(10, 8))
    for i, (_, measurement) in enumerate(dataset):
        #for i, (_, misure) in enumerate(dataset):: Questo ciclo for itera su ogni traiettoria nel dataset.
        # enumerate(dataset) restituisce una tupla di valori (indice, traiettoria) in cui indice è l'indice
        # corrente della traiettoria e traiettoria è la traiettoria stessa. Poiché non usiamo lo stato
        # vero, poniamo _ come il primo elemento della tupla che non ci serve. misure è la seconda parte
        # della tupla, che contiene i dati di misura della traiettoria.
        x = measurement[:, 0]  # Coordinate x delle misure
        #x = misure[:, 0]: Estrae le coordinate x delle misure della traiettoria corrente. misure[:, 0]
        # significa "prendi tutte le righe della matrice misure e seleziona solo la colonna 0",
        # che rappresenta le coordinate x.
        y = measurement[:, 1]  # Coordinate y delle misure
        
        # Colore della traiettoria
        color = plt.get_cmap('tab10')(i)  # Selezione del colore in base all'indice
        
        # Plot della traiettoria 
        plt.plot(x, y, color=color, label=f'Traiettoria {i+1}', zorder=1)
        
        # Punto all'inizio e alla fine della traiettoria
        plt.plot(x[0], y[0], marker='o', markersize=8, color=color, zorder=3)
        plt.plot(x[-1], y[-1], marker='o', markersize=8, color=color, zorder=3)
    
    
    plt.xlabel('Coordinate x')
    plt.ylabel('Coordinate y')
    plt.title('Traiettorie delle barche')
    plt.legend()
    plt.grid(True)
    
    if plotDir:
        # Ottieni il percorso completo della cartella "Images"
        imageDir = os.path.join(os.getcwd(), "Images")
        # Crea la cartella se non esiste
        os.makedirs(imageDir, exist_ok=True)
        # Salva il grafico nella cartella "Images" con il nome specificato
        plt.savefig(os.path.join(imageDir, plotDir))
    else:
        plt.show()
    
