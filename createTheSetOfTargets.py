import os
import numpy as np
import matplotlib.pyplot as plt

#--------------------------------------------------------------------------------------------------------

# def buildTheSet(numTrajectories: int, inputDataset: list, duration: int = 100):
#     #creo l'array di indici delle numTraiettorie traiettorie selezioante casualmente, da 0 a 49
#     selectedTrajectoriesIndex = np.random.choice(len(inputDataset), numTrajectories, replace=False)
#     print("Indici traiettorie selezionate:", selectedTrajectoriesIndex)
    
#     #np.random.choice(len(inputDataset), numTraiettorie, replace=False): Questa parte del codice utilizza
#     #la funzione np.random.choice di NumPy per selezionare casualmente numTraiettorie indici compresi
#     #tra 0 e len(inputDataset) - 1. Questi indici rappresentano le posizioni delle traiettorie
#     #all'interno dell'inputDataset. L'argomento replace=False garantisce che gli indici selezionati
#     #siano unici, ovvero che non ci siano traiettorie duplicate nel risultato.

#     #stampo le traiettorie selezionate in ordine rispetto a come sono stati messi gli indici nell'array
#     print("Traiettorie selezionate:")
#     try:
#         # Lista per memorizzare le traiettorie selezionate
#         selectedTrajectories = []
        
#         for i, iTraiettoria in enumerate(selectedTrajectoriesIndex):
#             print(f"Traiettoria {i + 1}: {iTraiettoria}-esima")
#             traiettoria = inputDataset[iTraiettoria]
            
#             # Aggiungi la traiettoria alla lista delle traiettorie selezionate
#             selectedTrajectories.append(traiettoria)
#     except Exception as e:
#         print("Errore durante la creazione dello scenario:", e)

#     #per verificare che ne stampo effettivamente il numero passato alla funzione
#     print("Numero di traiettorie selezionate:", len(selectedTrajectories))
    
#     # Restituisci la lista delle traiettorie selezionate
#     return selectedTrajectories

def buildTheSet(numTrajectories: int, inputDataset: list, duration: int):
    selectedTrajectories = []
    
    try:
        print(f"Traiettorie selezionate, troncate ai primi {duration} secondi: \n")
        for _ in range(numTrajectories):
            # Seleziona casualmente un indice di traiettoria dall'inputDataset
            random_trajectory_index = np.random.choice(len(inputDataset))
            # Ottieni la traiettoria corrispondente all'indice casuale
            random_trajectory = inputDataset[random_trajectory_index]
            
            # Tronca la traiettoria ai primi "duration" secondi
            truncated_real_state = random_trajectory[0][:duration]
            truncated_measurement = random_trajectory[1][:duration]
            
            # Aggiungi la traiettoria troncata alla lista delle traiettorie selezionate
            selectedTrajectories.append((truncated_real_state, truncated_measurement))
            
            # Stampa l'indice della traiettoria selezionata
            print(f"Traiettoria {len(selectedTrajectories)}: {random_trajectory_index}-esima")
        
         # Stampa il numero totale di traiettorie selezionate
        print("Numero di traiettorie selezionate:", len(selectedTrajectories))
        
    except Exception as e:
        print("Errore durante la creazione dello scenario:", e)
    
    #truncated_measurements_list = [truncated_measurement for _, truncated_measurement in selectedTrajectories]
    #print(np.array(truncated_measurements_list).shape)
    
    return selectedTrajectories


#--------------------------------------------------------------------------------------------------------

def extractInitialTargetPositions(selectedTrajectories: list, numTargets):
    # Creare un array NumPy dalle traiettorie selezionate
    selectedTrajectoriesArray = np.array(selectedTrajectories)

    # Inizializzare l'array per le posizioni iniziali
    initialTargetPositions = np.zeros((numTargets, 1, 2))

    # Estrarre le posizioni al tempo 0 per tutti i target
    initialTargetPositions[:, 0, :] = selectedTrajectoriesArray[:, 0, :]

    return initialTargetPositions
    
    
    # for measurement in selectedTrajectories:
    #     initialTargetPositions.append(measurement[0])  # Solo la misura al tempo t=0
    # return np.array(initialTargetPositions)

#--------------------------------------------------------------------------------------------------------

def printDataset(inputDatasetToPrint: list):
    for i, trajectory in enumerate(inputDatasetToPrint):
        print("\n" f"Traiettoria {i + 1}: \n")
        
        realState = trajectory[0]
        measurement = trajectory[1]
        #print(f"Stato vero della traiettoria:\n {realState}")
        print(f"\nMisure della traiettoria:\n {measurement}")
        print()


            
    # Quando vedi "..." nella lista degli stati veri, significa che ci sono altri stati intermedi tra
    # le posizioni mostrate. Questo è comune quando si tratta di dati di traiettorie, dove le posizioni
    # possono essere campionate a intervalli regolari nel tempo e i punti intermedi non vengono
    # esplicitamente registrati per ridurre la dimensione del dataset.

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
        
        # Punto all'inizio e alla fine della traiettoria con simboli diversi
        if(i==0):
            plt.plot(x[0], y[0], marker='o', markersize=8, color=color, zorder=3, label='Inizio')
        else:
            plt.plot(x[0], y[0], marker='o', markersize=8, color=color, zorder=3)
        
        if(i==0):
            plt.plot(x[-1], y[-1], marker='s', markersize=8, color=color, zorder=3, label='Fine')
        else:
            plt.plot(x[-1], y[-1], marker='s', markersize=8, color=color, zorder=3)
    
    
    
    plt.xlabel('Coordinate x')
    plt.ylabel('Coordinate y')
    plt.title('Traiettorie delle barche (Targets)')
    plt.legend(loc='upper left', bbox_to_anchor=(1, 1))
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
    
#--------------------------------------------------------------------------------------------------------

def plotStartingPointOfTrajectories(dataset, plotDir = None):
    plt.figure(figsize=(10, 8))
    
    # Lista per memorizzare i colori delle traiettorie
    colors = plt.get_cmap('tab10').colors
    
    for i, (_, measurement) in enumerate(dataset):
        # Estrai le coordinate x e y del punto di partenza
        start_x = measurement[0, 0]
        start_y = measurement[0, 1]
        
        # Seleziona il colore della traiettoria
        color = colors[i % len(colors)]  # Utilizza i colori ciclicamente
        
        # Plot del punto di partenza
        plt.scatter(start_x, start_y, color=color, label=f'Traiettoria {i+1}', zorder=3)
    
    
    plt.xlabel('Coordinate x')
    plt.ylabel('Coordinate y')
    plt.title('Coordinate iniziali delle barche (Targets)')
    plt.legend(loc='upper left', bbox_to_anchor=(1, 1))
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
        
    # print("""Come vedo, le coordinate di partenza x e y di tutte le traiettorie, sono comprese
    #       tra 0 e 200, dentro il file startingPoints.png lo si vede. Tutto ciò è stato fatto
    #       come riprova""")
    

