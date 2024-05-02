import math

#--------------------------------------------------------------------------------------------------------

# LEGENDA:
# l_00_0, i primi due indici sono i e j, i indica gli agenti e j i target, il terzo indice indica
# l'istante di tempo, in questo caso mi interessa solo l'istante iniziale e dunque ho 0 
# 
# quando invece ho solo E_j_0 si tratta dell'indice di copertura complessivo del target j, non è
# presente dunque il primo indice i, in quanto gli ho sommati tutti
#
# inoltre, se non è presente il terzo indice finale, quello del tempo, vuol dire che sto calcolando
# il vettore / lista complessiva per tutti e 100 i secondi

#--------------------------------------------------------------------------------------------------------

# funz di prova, calcolo di E_00_0
def calculateE_00_0(targets: list, initialAgents: list, r, mp):
    
    trajectory0 = targets[0]
    measurement0 = trajectory0[1]
    # se metto :,0 ottengo tutte le coordinate x di tutte le traiettorie
    qx0 = measurement0[0, 0]
    qy0 = measurement0[0, 1]
    
    # stampo le coordinate (x,y) (qx0(0) e qy0(0)) del target scelto per primo in modo casuale a t=0
    print("\n\nCoordinate del target 0 al tempo t=0:\n")
    print(f"Qx0(0) = {qx0}")
    print(f"Qy0(0) = {qy0}")
    
    # Stampa la coordinata x del primo agente
    print(f"Coordinata x del primo agente: {initialAgents[0][0]}")

    # Stampa la coordinata y del primo agente
    print(f"Coordinata y del primo agente: {initialAgents[0][1]}")
    
    # calcolo la distanza l00, tra il primo agente e il primo target
    l_00_0 = (initialAgents[0][0] - qx0)**2 + (initialAgents[0][1] - qy0)**2
    print(f"\nDistanza l00 tra il target 0 e l'agente 0: {l_00_0}")
    
    # calcolo l'indice di copertura al E00 all'istante iniziale t=0
    
    if(l_00_0 <= (r**2)):
        E_00_0 = (mp / (r**4))*(l_00_0-(r**2))**2
    else:
        E_00_0 = 0
        
    # Stampa l'indice di copertura l00 del target 0 rispetto all'agente 0
    print(f"\nIndice di copertura E00 del target 0 rispetto all'agente 0: {E_00_0}")
    
#--------------------------------------------------------------------------------------------------------

# calcolo degli indici di copertura al tempo t=0 per ogni target j
def calculateInitialCoverageIndices(targets: list, initialAgents: list, r, mp):
    # Inizializza una lista per memorizzare gli indici di copertura iniziali per ogni target
    initialCoverageIndices = []
    
    # Itera su tutti i target
    for trajectory, _ in targets:
        measurement0 = trajectory[1]
        qx0 = measurement0[0]  # Coordinate x del target al tempo t=0
        qy0 = measurement0[1]  # Coordinate y del target al tempo t=0
        
        # Inizializza l'indice di copertura per il target corrente
        E_j_0 = 0
        
        # Calcola l'indice di copertura per il target corrente rispetto a tutti gli agenti
        for agent_x, agent_y in initialAgents:
            # Calcola la distanza tra l'agente corrente e il target corrente
            l_ij_0 = (agent_x - qx0)**2 + (agent_y - qy0)**2
            
            # Calcola l'indice di copertura per l'agente corrente e il target corrente
            if l_ij_0 <= (r**2):
                E_ij_0 = (mp / (r**4)) * (l_ij_0 - (r**2))**2
            else:
                E_ij_0 = 0
            
            # Aggiungi l'indice di copertura parziale all'indice di copertura totale per il target
            E_j_0 += E_ij_0
        
        # Aggiungi l'indice di copertura totale per il target corrente alla lista degli indici di copertura
        initialCoverageIndices.append(E_j_0)
    
    # avrà dunque un vettore composto da 10 elementi (= nr targets)
    return initialCoverageIndices
