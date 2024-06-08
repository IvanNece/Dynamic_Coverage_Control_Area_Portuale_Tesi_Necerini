import numpy as np
import matplotlib.pyplot as plt
import os

#---------------------------------------------------------------------------------------------------------

def plotTotalCoverageIndex(totalCoverageIndex_values: list, plotDir=None):
    plt.figure(figsize=(10, 8))
    
    # Converti i tensor in array NumPy staccandoli dal grafo computazionale
    totalCoverageIndex_values_np = [val.detach().numpy() for val in totalCoverageIndex_values]

    plt.plot(range(len(totalCoverageIndex_values_np)), totalCoverageIndex_values_np, marker='o')
    
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
        
#---------------------------------------------------------------------------------------------------------

def plotTotalCoverageIndexStopped(totalCoverageIndex_values: list, plotDir=None):
    plt.figure(figsize=(10, 8))
    
    # Converti i tensor in array NumPy staccandoli dal grafo computazionale
    totalCoverageIndex_values_np = [val.detach().numpy() for val in totalCoverageIndex_values]

    plt.plot(range(len(totalCoverageIndex_values_np)), totalCoverageIndex_values_np, marker='o')
    
    plt.xlabel('Time')
    plt.ylabel('Total Coverage Index')
    plt.title('Total Coverage Index over Time With stopped targets')
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
        
#---------------------------------------------------------------------------------------------------------

# calcolo degli indici di copertura al tempo t generico per ogni target j
def calculateCoverageIndicesStopped(targets: list, agentsPosition: list, t, r, mp):
    # Inizializza una lista per memorizzare gli indici di copertura iniziali per ogni target
    coverageIndices = []
    
    #measurement = targets[1]
    
    
    # Itera su tutti i target con un indice j esplicito
    # for j, trajectory in enumerate(targets):
    for trajectory in targets:
        
        # # Aggiungi un controllo per assicurarti che t sia un indice valido
        # if t >= len(measurement):
        #     print(f"Errore: indice t={t} fuori dai limiti per la traiettoria {j}. Lunghezza traiettoria: {len(measurement)}.")
        #     continue  # Salta questa traiettoria se t è fuori dai limiti
        
        # t indica l'istante di tempo, il secondo numero indica la x (0) o la y (1)
        qx = trajectory[t, 0]  # Coordinate x del target al tempo t
        qy = trajectory[t, 1]  # Coordinate y del target al tempo t
        
        # Inizializza l'indice di copertura per il target corrente
        E_j_t = 0
        
        # Calcola l'indice di copertura per il target corrente rispetto a tutti gli agenti
        # Utilizza un indice i esplicito per gli agenti
        # for i, (agent_x, agent_y) in enumerate(agentsPosition):
        for agent_x, agent_y in agentsPosition:
            # Calcola la distanza tra l'agente corrente e il target corrente
            l_ij_t = (agent_x - qx)**2 + (agent_y - qy)**2
            
            # Calcola l'indice di copertura per l'agente corrente e il target corrente
            if l_ij_t <= (r**2):
                E_ij_t = (mp / (r**4)) * ((l_ij_t - (r**2))**2)
            else:
                E_ij_t = 0
            
            # Aggiungi l'indice di copertura parziale all'indice di copertura totale per il target
            E_j_t += E_ij_t
        
        # Aggiungi l'indice di copertura totale per il target corrente alla lista degli indici di copertura
        coverageIndices.append(E_j_t)
    
    # avrà dunque un vettore composto da 10 elementi (= nr targets)
    return coverageIndices