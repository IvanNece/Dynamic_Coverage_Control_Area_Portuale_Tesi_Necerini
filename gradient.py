import numpy as np

from initialCoverageIndices import calculateInitialCoverageIndices, calculateInitialTotalCoverageIndex
from coverageIndices import calculateCoverageIndices, calculateTotalCoverageIndex

#--------------------------------------------------------------------------------------------------------

# AL TEMPO 0
# Utilizzo formula classica differenze finite, wikipedia
# Funzione per calcolare il gradiente dell'indice di copertura totale E(0) rispetto alle posizioni degli agenti
def gradientOfInitialCoverageIndex(targets, initialAgents, r, mp, lb=1, h=1e-5):
    initialGradients = []
    initialCoverageIndices = calculateInitialCoverageIndices(targets, initialAgents, r, mp)
    # Utilizza un lowerbound arbitrario di 1
    totalCoverageIndex_0 = calculateInitialTotalCoverageIndex(initialCoverageIndices, 1)  
    
    # Iterazione su ciascun agente per calcolare il gradiente
    for i in range(len(initialAgents)):
        # Copia profonda delle posizioni iniziali degli agenti
        newPositions = [list(pos) for pos in initialAgents]
        
        # Calcolo del gradiente rispetto a x
        newPositions[i][0] += h
        newIndicesX = calculateInitialCoverageIndices(targets, newPositions, r, mp)
        newTotalIndexX = calculateInitialTotalCoverageIndex(newIndicesX, 1)
        gradientX = (newTotalIndexX - totalCoverageIndex_0) / h
        
        # Reset della posizione x
        newPositions[i][0] -= h
        
        # Calcolo del gradiente rispetto a y
        newPositions[i][1] += h
        newIndicesY = calculateInitialCoverageIndices(targets, newPositions, r, mp)
        newTotalIndexY = calculateInitialTotalCoverageIndex(newIndicesY, 1)
        gradientY = (newTotalIndexY - totalCoverageIndex_0) / h
        
        # Reset della posizione y, anche se non necessario perchè non uso più il dato, ma messo per chiarezza codice
        newPositions[i][1] -= h
        
        # Aggiungi il gradiente dell'agente corrente alla lista dei gradienti
        initialGradients.append((gradientX, gradientY))
    
    return initialGradients

    # Questa funzione restituisce una lista di tuple, dove ogni tupla contiene il gradiente dell'indice di 
    # copertura totale rispetto alle coordinate x e y di ciascun agente.
    #
    # Puoi poi utilizzare questa funzione per ottimizzare le posizioni degli agenti in modo da massimizzare
    # l'indice di copertura totale. Ad esempio, puoi utilizzare l'algoritmo di ascesa del gradiente per
    # aggiornare le posizioni degli agenti iterativamente fino a quando l'indice di copertura totale non
    # raggiunge un valore desiderato


#--------------------------------------------------------------------------------------------------------

# AL TEMPO t GENERICO
# Utilizzo formula classica differenze finite, wikipedia
# Funzione per calcolare il gradiente dell'indice di copertura totale E(t) rispetto alle posizioni degli agenti i
def gradientOfCoverageIndex(targets, agentsPosition, t, r, mp, lb=1, h=1e-5):
    # Inizializza un array di zeri per i gradienti
    gradients_t = np.zeros((len(agentsPosition), 2)) 
    
    coverageIndices = calculateCoverageIndices(targets, agentsPosition, t, r, mp)

    totalCoverageIndex_t = calculateTotalCoverageIndex(coverageIndices, t, lb)  
    
    # Iterazione su ciascun agente per calcolare il gradiente
    for i in range(len(agentsPosition)):
        # Copia profonda delle posizioni iniziali degli agenti
        # newPositions = [list(pos) for pos in agentsPosition]
        newPositions = np.copy(agentsPosition)  # Usa np.copy per una copia profonda
        
        # Calcolo del gradiente rispetto a x
        newPositions[i][0] += h
        newIndicesX = calculateInitialCoverageIndices(targets, newPositions, r, mp)
        newTotalIndexX = calculateInitialTotalCoverageIndex(newIndicesX, 1)
        gradientX = (newTotalIndexX - totalCoverageIndex_t) / h
        
        # Reset della posizione x
        newPositions[i][0] -= h
        
        # Calcolo del gradiente rispetto a y
        newPositions[i][1] += h
        newIndicesY = calculateInitialCoverageIndices(targets, newPositions, r, mp)
        newTotalIndexY = calculateInitialTotalCoverageIndex(newIndicesY, 1)
        gradientY = (newTotalIndexY - totalCoverageIndex_t) / h
        
        # Reset della posizione y, anche se non necessario perchè non uso più il dato, ma messo per chiarezza codice
        newPositions[i][1] -= h
        
        # Aggiungi il gradiente dell'agente corrente alla lista dei gradienti
        # gradients_t.append((gradientX, gradientY))
        # Assegna i gradienti calcolati al vettore dei gradienti
        gradients_t[i] = [gradientX, gradientY]
    
    return gradients_t