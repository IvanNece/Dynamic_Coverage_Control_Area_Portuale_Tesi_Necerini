import os
import numpy as np
import matplotlib.pyplot as plt

#--------------------------------------------------------------------------------------------------------


def generateInitialAgentPositions(numAgents: int, initialAreaSize: int, r):
    if numAgents == 4:
        # Posizioni specificate per 4 agenti
        initialAgentPositions = [(50, 50), (50, 150), (150, 50), (150, 150)]
    else:
        # Calcola la dimensione della griglia
        grid_size = int(np.sqrt(numAgents))
        if grid_size * grid_size < numAgents:
            grid_size += 1

        # Calcola le distanze tra gli agenti per coprire l'area 200x200
        x_spacing = (initialAreaSize - 100) / (grid_size - 1)
        y_spacing = (initialAreaSize - 100) / (grid_size - 1)

        # Lista per memorizzare le posizioni degli agenti
        initialAgentPositions = []

        # Genera le posizioni degli agenti distribuendoli uniformemente
        for i in range(grid_size):
            for j in range(grid_size):
                if len(initialAgentPositions) < numAgents:
                    x = 50 + j * x_spacing
                    y = 50 + i * y_spacing
                    initialAgentPositions.append((x, y))
    
    return np.array(initialAgentPositions, dtype=float)

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