import os
import numpy as np
import matplotlib.pyplot as plt

#--------------------------------------------------------------------------------------------------------

def generateInitialAgentPositions(numAgents: int, initialAreaSize: int, r):
    # Calcola il numero di celle in cui distribuire gli agenti
    # Dato che ogni agente copre un'area di raggio 'r', possiamo approssimare che un agente copre un quadrato di lato 'r'
    cellSize = r * np.sqrt(2) / 2
    numRows = int(initialAreaSize / cellSize)
    numCols = int(np.ceil(numAgents / numRows))
    
    # Lista per memorizzare le posizioni degli agenti
    initialAgentPositions = []

    # Genera le posizioni degli agenti distribuendoli equamente nelle celle
    for i in range(numRows):
        for j in range(numCols):
            if len(initialAgentPositions) < numAgents:
                # Calcola le coordinate del centro della cella
                x_center = (j + 0.5) * cellSize
                y_center = (i + 0.5) * cellSize
                
                # Aggiungi la posizione dell'agente alla lista
                initialAgentPositions.append((x_center, y_center))
    
    return np.array(initialAgentPositions)

#--------------------------------------------------------------------------------------------------------

# def generateInitialAgentPositions(numAgents: int, initialAreaSize: int):
#     # Calcola il numero di celle in cui distribuire gli agenti
#     numRows = int(np.sqrt(numAgents))
#     numCols = int(np.ceil(numAgents / numRows))
    
#     # Calcola le dimensioni di ciascuna cella
#     cellSizeX = initialAreaSize / numCols
#     cellSizeY = initialAreaSize / numRows
    
#     # Lista per memorizzare le posizioni degli agenti
#     initialAgentPositions = []
    
#     # Genera le posizioni degli agenti distribuendoli equamente nelle celle
#     for i in range(numRows):
#         for j in range(numCols):
#             if len(initialAgentPositions) < numAgents:
#                 # Calcola le coordinate del centro della cella
#                 x_center = (j + 0.5) * cellSizeX
#                 y_center = (i + 0.5) * cellSizeY
                
#                 # Aggiungi la posizione dell'agente alla lista
#                 initialAgentPositions.append((x_center, y_center))
    
#     return initialAgentPositions


#--------------------------------------------------------------------------------------------------------

def plotInitialAgentPositions(initialAgentPositions: list, plotDir = None):
    plt.figure(figsize=(10, 8))
    
    # Estrai le coordinate x e y delle posizioni degli agenti
    agent_x = [pos[0] for pos in initialAgentPositions]
    agent_y = [pos[1] for pos in initialAgentPositions]
    
    # Plot delle posizioni iniziali degli agenti
    
    plt.scatter(agent_x, agent_y, color='red', label='Posizioni iniziali degli agenti')
    plt.xlabel('Coordinate x')
    plt.ylabel('Coordinate y')
    plt.title('Posizioni iniziali degli agenti')
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