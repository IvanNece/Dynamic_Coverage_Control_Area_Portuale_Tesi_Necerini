import numpy as np

from coverageIndices import calculateCoverageIndices, calculateTotalCoverageIndex
from gradient import gradientOfCoverageIndex
    
#-------------------------------------------------------------------------------------------------------

def coverageAlgorithmV1(targetsTrajectories: list, agentsInitialPosition: list, r, mp, lb, h, NUMAGENTS, NUMSECONDS, EPSILON):
    # Assicurati che agentsPosition sia un array NumPy bidimensionale
    #TODO CHIAMALO DIVERSAMENTE, TIPO CON s FINALE
    agentsInitialPositions = np.array(agentsInitialPosition)
    
    # NUMSECONDS x NUMAGENTS x 2 (x, y coordinates)
    #TODO CONTROLLA SE NON DEVI INVERTIRE STRUTTURA
    agentsTrajectories = np.zeros((NUMSECONDS, NUMAGENTS, 2))  
    
    agentsTrajectories[0] = agentsInitialPositions
    # print(agentsTrajectories[0][1][0])
    # print(agentsTrajectories[0][1][1])
    # print(agentsTrajectories[0])
    
    #FISSO L'ISTANTE DI TEMPO
    for t in range(NUMSECONDS-1):  
        
        # print(f"Posizioni degli agenti al tempo {t}:")
        # print(agentsTrajectories[t])
                  
        # Prima di iniziare il ciclo, creiamo un array di zeri con la stessa forma delle posizioni
        # degli agenti (NUM_AGENTS righe e 2 colonne per le coordinate x e y). Questo assicura che
        # l'array possa contenere i gradienti per ogni agente.
        # Calcola il gradiente dell'indice di copertura per ogni agente per determinare la direzione di movimento ottimale
        # Preallocazione dell'array per i gradienti con la stessa dimensione delle posizioni degli agenti
        #gradients_t = np.zeros((NUMAGENTS, 2))  # 2 per x e y
        
        # Calcola il gradiente dell'indice di copertura per ogni agente
        # Lo faccio fuori dal ciclo perchè la funzione è già fatta per calcolare il gradiente
        # di ogni agente i al tempo t
        #TODO CONTROLLA QUA, MAGARI PASSO IL NUOVO AGENTSPOSITIONS[T]
        gradients_t = gradientOfCoverageIndex(targetsTrajectories, agentsTrajectories[t], t, r, mp, lb, h)
        # print(gradients_t.shape)  

        
        # Stampa i gradienti per monitorare i cambiamenti
        #print(f"Iterazione {t+1}, Gradienti:\n {gradients_t}\n")
        
        # Verifica se i gradienti sono vicini a zero e termina se vero
        # if np.all(np.abs(gradients_t) < 1e-6):  # Soglia da regolare a seconda delle esigenze
        #     print("I gradienti sono vicini a zero, terminazione anticipata dell'algoritmo.")
        #     break
        
        # Uso del ciclo for classico per iterare sugli agenti
        for i in range(NUMAGENTS):
            # Aggiornamento della posizione dell'agente i-esimo
            # Lo fa in automatico sia di x che di y l'aggiornamento essendo entrambi due array
            # numpy bidimensionali
            #TODO QUA DA RIVERE TUTTO, IO DEVO FARE P[i][t+1] = P[i][t] + ....
            agentsTrajectories[t+1][i][0] = (agentsTrajectories[t][i][0]) + (EPSILON*gradients_t[i][0])
            agentsTrajectories[t+1][i][1] = (agentsTrajectories[t][i][1]) + (EPSILON*gradients_t[i][1])
            #agentsPosition[i] += EPSILON * gradients_t[i]
            
        # print(f"Posizioni degli agenti al tempo {t+1}:")
        # print(agentsTrajectories[t+1])
        
        # Salva la posizione aggiornata di tutti gli agenti al tempo t
        #agentsTrajectories[t] = agentsPosition.copy()
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
    
    
    
    

    
