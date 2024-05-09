import numpy as np

from initialCoverageIndices import calculateInitialCoverageIndices, calculateInitialTotalCoverageIndex
from coverageIndices import calculateCoverageIndices, calculateTotalCoverageIndex

#--------------------------------------------------------------------------------------------------------

# AL TEMPO 0
# Utilizzo formula classica differenze finite, wikipedia
# Funzione per calcolare il gradiente dell'indice di copertura totale E(0) rispetto alle posizioni degli agenti
def gradientOfInitialCoverageIndex(targets, initialAgents, r, mp, lb=1, h=1e-2):
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

def perturbGradientIfCloseToZero(gradients, epsilon=1e-4, threshold=1e-5):
    """
    Applica una piccola perturbazione ai gradienti che sono vicini allo zero per prevenire la stagnazione.
    
    Args:
    gradients (np.array): Array di gradienti.
    epsilon (float): Magnitudine della perturbazione da applicare.
    threshold (float): Soglia per determinare se un gradiente è vicino a zero.
    
    Returns:
    np.array: Gradienti perturbati.
    """
    
    magnitudes = np.linalg.norm(gradients, axis=1, keepdims=True)  # Calcola la norma di ogni vettore gradiente
    smallGradients = magnitudes < threshold  # Trova i gradienti che sono più piccoli della soglia
    perturbations = epsilon * np.random.normal(size=gradients.shape)  # Crea perturbazioni casuali con la stessa forma dell'array dei gradienti
    
    # Applica le perturbazioni solo dove i gradienti sono piccoli
    # Dato che `smallGradients` ha una forma (n, 1) e `gradients` ha forma (n, 2), dobbiamo riformattare `smallGradients`
    smallGradients = np.repeat(smallGradients, gradients.shape[1], axis=1)  # Ripete la colonna booleana per ogni dimensione del gradiente
    
    gradients[smallGradients] = perturbations[smallGradients]  # Sostituisce i gradienti piccoli con le perturbazioni
    return gradients


#--------------------------------------------------------------------------------------------------------


# AL TEMPO t GENERICO
# Utilizzo formula classica differenze finite, wikipedia
# Funzione per calcolare il gradiente dell'indice di copertura totale E(t) rispetto alle posizioni degli agenti i
def gradientOfCoverageIndex(targets, agentsPosition, t, r, mp, lb=1, h=1e-2):
    
    # h = PASSO DELLE DIFFERENZE FINITE, sensibilità del calcolo del gradiente
    
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
        
    gradients_t = perturbGradientIfCloseToZero(gradients_t)
    
    return gradients_t