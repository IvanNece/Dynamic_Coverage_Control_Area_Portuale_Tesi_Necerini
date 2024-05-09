import numpy as np

from coverageIndices import calculateCoverageIndices, calculateTotalCoverageIndex
from gradient import gradientOfCoverageIndex
    
#-------------------------------------------------------------------------------------------------------

def coverageAlgorithm(targetsTrajectories: list, agentsPosition: list, r, mp, lb, h, NUMAGENTS, NUMSECONDS, EPSILON):
    # Assicurati che agentsPosition sia un array NumPy bidimensionale
    agentsPosition = np.array(agentsPosition)
    
    # NUMSECONDS x NUMAGENTS x 2 (x, y coordinates)
    agentsTrajectories = np.zeros((NUMSECONDS, NUMAGENTS, 2))  
    
    for t in range(NUMSECONDS):
        # calcola gli indici di copertura per ogni target data la posizione corrente degli agenti
        # calcolo Ej(t) per ogni target j
        coverageIndices_t = calculateCoverageIndices(targetsTrajectories, agentsPosition, t, r, mp )
        
        # calcola l'indice di copertura totale combinando gli indici di tutti i target
        # calcolo E(t)
        # totalCoverageIndex_t = calculateTotalCoverageIndex(coverageIndices_t, t, lb)
        # tanto viene calcolato dentro gradientOfCoverageIndex
        
            
        # Prima di iniziare il ciclo, creiamo un array di zeri con la stessa forma delle posizioni
        # degli agenti (NUM_AGENTS righe e 2 colonne per le coordinate x e y). Questo assicura che
        # l'array possa contenere i gradienti per ogni agente.
        # Calcola il gradiente dell'indice di copertura per ogni agente per determinare la direzione di movimento ottimale
        # Preallocazione dell'array per i gradienti con la stessa dimensione delle posizioni degli agenti
        gradients_t = np.zeros((NUMAGENTS, 2))  # 2 per x e y
        
        # Calcola il gradiente dell'indice di copertura per ogni agente
        # Lo faccio fuori dal ciclo perchè la funzione è già fatta per calcolare il gradiente
        # di ogni agente i al tempo t
        gradients_t = gradientOfCoverageIndex(targetsTrajectories, agentsPosition, t, r, mp, lb, h)
        
        # Stampa i gradienti per monitorare i cambiamenti
        print(f"Iterazione {t+1}, Gradienti:\n {gradients_t}\n")
        
        # Verifica se i gradienti sono vicini a zero e termina se vero
        # if np.all(np.abs(gradients_t) < 1e-6):  # Soglia da regolare a seconda delle esigenze
        #     print("I gradienti sono vicini a zero, terminazione anticipata dell'algoritmo.")
        #     break
        
        # Uso del ciclo for classico per iterare sugli agenti
        for i in range(NUMAGENTS):
            # Aggiornamento della posizione dell'agente i-esimo
            # Lo fa in automatico sia di x che di y l'aggiornamento essendo entrmabi due array
            # numpy bidimensionali
            agentsPosition[i] += EPSILON * gradients_t[i]
            
        # Salva la posizione aggiornata di tutti gli agenti al tempo t
        agentsTrajectories[t] = agentsPosition.copy()
        # L'uso del metodo .copy() è cruciale qui. Senza .copy(), l'assegnazione avrebbe solo creato 
        # un riferimento all'array agentsPosition e non una copia fisica dei dati. Ciò significa che 
        # modifiche future ad agentsPosition avrebbero influenzato anche i dati già memorizzati in
        # agentsTrajectories. Con .copy(), si garantisce che ogni "fetta" di tempo in agentsTrajectories
        # mantenga una copia indipendente e immutabile delle posizioni degli agenti come erano alla fine
        # di quel secondo specifico.

    return agentsTrajectories

    # ESEMPIO:
    # Con 4 agenti e una simulazione di 100 secondi, alla fine della simulazione, agentsTrajectories
    # sarà una matrice di dimensione 100 x 4 x 2. Ogni elemento agentsTrajectories[t][i] sarà un array
    # di due elementi [x, y], rappresentando la posizione dell'agente i al secondo t.

    
