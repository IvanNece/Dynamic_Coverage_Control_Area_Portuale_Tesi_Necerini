import numpy as np
import torch

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


# # AL TEMPO t GENERICO
# # Utilizzo formula classica differenze finite, wikipedia
# # Funzione per calcolare il gradiente dell'indice di copertura totale E(t) rispetto alle posizioni degli agenti i
# def gradientOfCoverageIndex(targets, agentsPosition, t, r, mp, lb, h):
    
#     # h = PASSO DELLE DIFFERENZE FINITE, sensibilità del calcolo del gradiente
    
#     # Inizializza un array di zeri per i gradienti
#     gradients_t = np.zeros((len(agentsPosition), 2)) 
    
#     coverageIndices = calculateCoverageIndices(targets, agentsPosition, t, r, mp)

#     totalCoverageIndex_t = calculateTotalCoverageIndex(coverageIndices, lb) 
    
#     #TODO CONTROLLO CHE SIA CORRETTA LA FORMA DEGLI ARRAY CHE PASSO (fatto, corretto)
#     # print(gradients_t.shape)
#     # print(agentsPosition.shape)
#     # #print(coverageIndices.shape)
#     # print(targets.shape)
    
#     #todo magari passo delle posizioni sbagliate, lo verifico, così se è corretto, vuol dire che è 
#     #todo sbagliato proprio il calcolo del gradiente 
    
#     #TODO STAMPARE POSIZIONE TARGET IN TUTTE LE ITERAZIONI (fatto, corretto) 
#     # print(f"Posizioni dei target al tempo {t}:")
#     # for target in targets:
#     #     print(target[t])
#     #TODO STAMPARE POSIZIONI AGENTI IN TUTTE LE ITERAZIONI (anche nel caso di target fermi) (fatto, corretto)
#     # Stampa le posizioni degli agenti
#     # print(f"Posizioni degli agenti al tempo {t}:")
#     # for agent in agentsPosition:
#     #     print(agent)
    
#     #TODO STAMPARE GRADIENTE
    
#     #TODO STAMPARE POSIZIONE DOPO L'INCREMENTO 
    
#     # Iterazione su ciascun agente per calcolare il gradiente
#     for i in range(len(agentsPosition)):
#         # Copia profonda delle posizioni iniziali degli agenti
#         # newPositions = [list(pos) for pos in agentsPosition]
#         newPositions = np.copy(agentsPosition)  # Usa np.copy per una copia profonda
        
#         # Calcolo del gradiente rispetto a x
#         newPositions[i][0] += h
#         newIndicesX = calculateCoverageIndices(targets, newPositions, t, r, mp)
#         newTotalIndexX = calculateTotalCoverageIndex(newIndicesX, lb)
#         gradientX = (newTotalIndexX - totalCoverageIndex_t) / h
        
#         # Reset della posizione x
#         newPositions[i][0] -= h
        
#         # Calcolo del gradiente rispetto a y
#         newPositions[i][1] += h
#         newIndicesY = calculateCoverageIndices(targets, newPositions, t, r, mp)
#         newTotalIndexY = calculateTotalCoverageIndex(newIndicesY, lb)
#         gradientY = (newTotalIndexY - totalCoverageIndex_t) / h
        
#         # Reset della posizione y, anche se non necessario perchè non uso più il dato, ma messo per chiarezza codice
#         newPositions[i][1] -= h
        
#         # Aggiungi il gradiente dell'agente corrente alla lista dei gradienti
#         # gradients_t.append((gradientX, gradientY))
#         # Assegna i gradienti calcolati al vettore dei gradienti
#         gradients_t[i] = [gradientX, gradientY]
        
        
#     # # Debug: Stampa i gradienti calcolati
#     # print(f"Gradients at time {t}:\n{gradients_t}\n")
    
#     #gradients_t = perturbGradientIfCloseToZero(gradients_t)
#     #print(f"Perturbed gradients at time {t}:\n{gradients_t}\n")
    
#     return gradients_t


#----------------------------------------------------------------------------------------

# CALCOLO GRADIENTE CON PYTORCH
def gradientOfCoverageIndex(targets, agentsPosition, t, r, mp, lb, h):
    agentsPosition_torch = torch.tensor(agentsPosition, requires_grad=True, dtype=torch.float32)
    
    coverageIndices = calculateCoverageIndices(targets, agentsPosition_torch, t, r, mp)
    totalCoverageIndex_t = calculateTotalCoverageIndex(coverageIndices, lb)
    
    # Assicuriamoci che totalCoverageIndex_t richieda gradienti
    totalCoverageIndex_t = totalCoverageIndex_t.requires_grad_(True)
    
    totalCoverageIndex_t.backward()
    
    # Verifica che i gradienti siano calcolati
    if agentsPosition_torch.grad is None:
        raise RuntimeError("I gradienti non sono stati calcolati correttamente.")
    
    #gradients_t = agentsPosition_torch.grad.numpy()
    gradients_t = agentsPosition_torch.grad.detach().numpy()
    
    #print(f"Gradients at time {t}:\n{gradients_t}\n")
    #print(f"Gradients shape: {gradients_t.shape}")
    
    return gradients_t

    """
    agentsPosition_torch = torch.tensor(agentsPosition, requires_grad=True, dtype=torch.float32): Converte l'array agentsPosition in un tensore PyTorch e abilita il calcolo automatico dei gradienti impostando requires_grad=True. Questo consente di tracciare tutte le operazioni eseguite su agentsPosition_torch.

coverageIndices = calculateCoverageIndices(targets, agentsPosition_torch, t, r, mp): Calcola gli indici di copertura utilizzando le posizioni degli agenti rappresentate come tensori PyTorch. La funzione calculateCoverageIndices non è definita qui, ma si presume che utilizzi PyTorch per i calcoli.

totalCoverageIndex_t = calculateTotalCoverageIndex(coverageIndices, lb): Calcola l'indice di copertura totale a partire dagli indici di copertura individuali. Anche questa funzione si presume utilizzi PyTorch.

totalCoverageIndex_t = totalCoverageIndex_t.requires_grad_(True): Assicura che totalCoverageIndex_t richieda gradienti, il che è necessario per la successiva operazione di backpropagation.

totalCoverageIndex_t.backward(): Esegue la backpropagation per calcolare i gradienti dell'indice di copertura totale rispetto alle posizioni degli agenti. PyTorch costruisce dinamicamente il grafo computazionale e, con questa chiamata, calcola i gradienti rispetto a tutte le variabili che hanno contribuito a totalCoverageIndex_t.

if agentsPosition_torch.grad is None: Verifica che i gradienti siano stati effettivamente calcolati. Se agentsPosition_torch.grad è None, significa che qualcosa è andato storto durante la backpropagation.

gradients_t = agentsPosition_torch.grad.detach().numpy(): Estrae i gradienti calcolati, li disconnette dal grafo computazionale di PyTorch utilizzando detach() e li converte in un array NumPy per un'ulteriore elaborazione al di fuori del contesto di PyTorch. Questo è necessario perché i gradienti inizialmente sono ancora legati al grafo computazionale e sono rappresentati come tensori PyTorch.

Le righe commentate con # sono utilizzate per il debug e mostrano i gradienti calcolati e la loro forma, ma sono state disattivate per l'esecuzione normale.
    """