import numpy as np

#--------------------------------------------------------------------------------------------------------

# NOTE: è uguale al file initialCoverageIndices, ma non più solo per l'istante t=0
# ma per un generico istante t che passo alle funzioni

# LEGENDA:
# l_00_t, i primi due indici sono i e j, i indica gli agenti e j i target, il terzo indice indica
# l'istante di tempo, in questo caso mi interessa solo l'istante iniziale e dunque ho 0 
# 
# quando invece ho solo E_j_t si tratta dell'indice di copertura complessivo del target j, non è
# presente dunque il primo indice i, in quanto gli ho sommati tutti
#
# inoltre, se non è presente il terzo indice finale, quello del tempo, vuol dire che sto calcolando
# il vettore / lista complessiva per tutti e 100 i secondi

#--------------------------------------------------------------------------------------------------------
# calcolo degli indici di copertura al tempo t generico per ogni target j
def calculateCoverageIndices(targets: list, agentsPosition: list, t, r, mp):
    # Inizializza una lista per memorizzare gli indici di copertura iniziali per ogni target
    coverageIndices = []
    
    #measurement = targets[1]
    
    
    # Itera su tutti i target con un indice j esplicito
    for j, trajectory in enumerate(targets):
        # [1] perchè prendo solo le misure, non lo stato vero
        measurement = trajectory[1]
        
        # # Aggiungi un controllo per assicurarti che t sia un indice valido
        # if t >= len(measurement):
        #     print(f"Errore: indice t={t} fuori dai limiti per la traiettoria {j}. Lunghezza traiettoria: {len(measurement)}.")
        #     continue  # Salta questa traiettoria se t è fuori dai limiti
        
        # t indica l'istante di tempo, il secondo numero indica la x (0) o la y (1)
        qx = measurement[t, 0]  # Coordinate x del target al tempo t
        qy = measurement[t, 1]  # Coordinate y del target al tempo t
        
        # Inizializza l'indice di copertura per il target corrente
        E_j_t = 0
        
        # Calcola l'indice di copertura per il target corrente rispetto a tutti gli agenti
        # Utilizza un indice i esplicito per gli agenti
        for i, (agent_x, agent_y) in enumerate(agentsPosition):
            # Calcola la distanza tra l'agente corrente e il target corrente
            l_ij_t = (agent_x - qx)**2 + (agent_y - qy)**2
            
            # Calcola l'indice di copertura per l'agente corrente e il target corrente
            if l_ij_t <= (r**2):
                E_ij_t = (mp / (r**4)) * (l_ij_t - (r**2))**2
            else:
                E_ij_t = 0
            
            # Aggiungi l'indice di copertura parziale all'indice di copertura totale per il target
            E_j_t += E_ij_t
        
        # Aggiungi l'indice di copertura totale per il target corrente alla lista degli indici di copertura
        coverageIndices.append(E_j_t)
    
    # avrà dunque un vettore composto da 10 elementi (= nr targets)
    return coverageIndices

#--------------------------------------------------------------------------------------------------------

# funzione sigmoidale
def sigmoid(x, lb):
    #TODO controllare come passo parametro lb
    return (np.tanh((x - lb)) + 1) / 2


# calcolo dell'indice di copertura totale E(t), al tempo t generico
def calculateTotalCoverageIndex(coverageIndices: list, t, lowerboundIndex):
    totalCoverageIndex_t = 0
    for i, index in enumerate(coverageIndices):
        indexWithSigmoid = sigmoid(index, lowerboundIndex)
        totalCoverageIndex_t += indexWithSigmoid
        #print(f"Indice di copertura parziale sigmoidale per l'elemento {i}: {indexWithSigmoid}")
        
    return totalCoverageIndex_t
