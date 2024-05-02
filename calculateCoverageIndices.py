import math

#--------------------------------------------------------------------------------------------------------

# funz di prova, calcolo di E00
def calculateE00(targets: list, initialAgents: list, r, mp):
    
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
    l00 = (initialAgents[0][0] - qx0)**2 + (initialAgents[0][1] - qy0)**2
    print(f"\nDistanza l00 tra il target 0 e l'agente 0: {l00}")
    
    # calcolo l'indice di copertura al E00 all'istante iniziale t=0
    
    if(l00 <= (r**2)):
        E00 = (mp / (r**4))*(l00-(r**2))**2
    else:
        E00 = 0
        
    # Stampa l'indice di copertura l00 del target 0 rispetto all'agente 0
    print(f"\nIndice di copertura E00 del target 0 rispetto all'agente 0: {E00}")
    
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
        E_j = 0
        
        # Calcola l'indice di copertura per il target corrente rispetto a tutti gli agenti
        for agent_x, agent_y in initialAgents:
            # Calcola la distanza tra l'agente corrente e il target corrente
            l_ij = (agent_x - qx0)**2 + (agent_y - qy0)**2
            
            # Calcola l'indice di copertura per l'agente corrente e il target corrente
            if l_ij <= (r**2):
                E_ij = (mp / (r**4)) * (l_ij - (r**2))**2
            else:
                E_ij = 0
            
            # Aggiungi l'indice di copertura parziale all'indice di copertura totale per il target
            E_j += E_ij
        
        # Aggiungi l'indice di copertura totale per il target corrente alla lista degli indici di copertura
        initialCoverageIndices.append(E_j)
    
    return initialCoverageIndices
