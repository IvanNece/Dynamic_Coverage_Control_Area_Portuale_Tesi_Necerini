import os
import matplotlib.pyplot as plt
import numpy as np

#--------------------------------------------------------------------------------------------------------

def plotTrajectoriesWithAgentStartPoints(dataset, agentPositions, plotDir=None):
    plt.figure(figsize=(10, 8))
    
    # Plot delle traiettorie dei target
    for i, (_, measurement) in enumerate(dataset):
        x = measurement[:, 0]  
        y = measurement[:, 1]  
        color = plt.get_cmap('tab10')(i)  
        plt.plot(x, y, color=color, label=f'Traiettoria {i+1}', zorder=1)
    
        # Punto all'inizio e alla fine della traiettoria con simboli diversi
        if(i==0):
            plt.plot(x[0], y[0], marker='o', markersize=8, color=color, zorder=3, label='Inizio')
        else:
            plt.plot(x[0], y[0], marker='o', markersize=8, color=color, zorder=3)
        
        if(i==0):
            plt.plot(x[-1], y[-1], marker='s', markersize=8, color=color, zorder=3, label='Fine')
        else:
            plt.plot(x[-1], y[-1], marker='s', markersize=8, color=color, zorder=3)
    
    # Plot dei punti di partenza degli agenti
    agent_x = [pos[0] for pos in agentPositions]
    agent_y = [pos[1] for pos in agentPositions]
    plt.scatter(agent_x, agent_y, color='red', label='Posizioni iniziali degli agenti', zorder=2)
    
    plt.xlabel('Coordinate x')
    plt.ylabel('Coordinate y')
    plt.title('Traiettorie dei target e posizioni iniziali degli agenti')
    plt.legend(loc='upper left', bbox_to_anchor=(1, 1))
    plt.grid(True)
    
    if plotDir:
        imageDir = os.path.join(os.getcwd(), "Images")
        os.makedirs(imageDir, exist_ok=True)
        plt.savefig(os.path.join(imageDir, plotDir), bbox_inches='tight')
    else:
        plt.show()
        
        
#--------------------------------------------------------------------------------------------------------

def plotAll(targetTrajectories, agentTrajectories, plotDir=None):
    plt.figure(figsize=(10, 8))
    
    # Plot delle traiettorie dei target
    for i, (_, measurement) in enumerate(targetTrajectories):
        x = measurement[:, 0]  
        y = measurement[:, 1]  
        color = plt.get_cmap('tab10')(i)  
        plt.plot(x, y, color=color, label=f'Target {i+1}', zorder=1)
    
        # Punto all'inizio e alla fine della traiettoria con simboli diversi
        if(i==0):
            plt.plot(x[0], y[0], marker='o', markersize=8, color=color, zorder=3, label='Inizio target')
            plt.plot(x[-1], y[-1], marker='s', markersize=8, color=color, zorder=3, label='Fine target')
        else:
            plt.plot(x[0], y[0], marker='o', markersize=8, color=color, zorder=3)
            plt.plot(x[-1], y[-1], marker='s', markersize=8, color=color, zorder=3)
    
    
    # Plot delle traiettorie degli agenti
    for j in range(agentTrajectories.shape[1]):  # itera su ogni agente
        agent_x = agentTrajectories[:, j, 0]
        agent_y = agentTrajectories[:, j, 1]
        plt.plot(agent_x, agent_y, linestyle='--', color='red', zorder=2)  # traiettorie degli agenti in rosso
        if j == 0:
            plt.scatter(agent_x[0], agent_y[0], color='red', marker='o', s=100, zorder=4, label='Inizio Agenti')
            plt.scatter(agent_x[-1], agent_y[-1], color='red', marker='x', s=100, zorder=4, label='Fine Agenti')
        else:
            plt.scatter(agent_x[0], agent_y[0], color='red', marker='o', s=100, zorder=4)
            plt.scatter(agent_x[-1], agent_y[-1], color='red', marker='x', s=100, zorder=4)
            
            
    # Parte finale
    plt.xlabel('Coordinate x')
    plt.ylabel('Coordinate y')
    plt.title('Traiettorie dei targets e degli agenti')
    plt.legend(loc='upper left', bbox_to_anchor=(1, 1))
    plt.grid(True)
    
    if plotDir:
        imageDir = os.path.join(os.getcwd(), "Images")
        os.makedirs(imageDir, exist_ok=True)
        plt.savefig(os.path.join(imageDir, plotDir), bbox_inches='tight')
    else:
        plt.show()
        
        
#--------------------------------------------------------------------------------------------------------


def plotFinalSetWithRadius(targetTrajectories, agentTrajectories, duration, r, plotDir=None):
    # estraggo posizioni finali degli agenti
    finalAgentPositions = agentTrajectories[duration-1]
    # shape (4,2)
    #print(finalAgentPositions.shape)

    # estraggo posizioni finali dei target
    finalTargetPositions = targetTrajectories[:, duration-1, :]
    # shape (10,2)
    #print(finalTargetPositions.shape)
    
    # Colori differenti per ciascun agente
    colors = ['red', 'blue', 'green', 'orange']

    fig, ax = plt.subplots(figsize=(10, 10))
    # Plot posizioni finali dei target
    ax.scatter(finalTargetPositions[:, 0], finalTargetPositions[:, 1], marker='s', label='Targets')

    # Plot posizioni finali degli agenti con cerchi di copertura
    for i, (x, y) in enumerate(finalAgentPositions):
        ax.scatter(x, y, marker='x', color=colors[i], label=f'Agente {i+1}')
        circle = plt.Circle((x, y), r, edgecolor=colors[i], facecolor=colors[i], fill=True, alpha=0.1, linestyle='--', linewidth=2)
        ax.add_artist(circle)
        
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_title('Posizioni finali di target e agenti con aree di copertura, ALGORITMO V3')
    ax.legend()
    plt.grid(True)
    plt.axis('equal')
    
    # Set limits to ensure all circles are fully visible
    padding = r + 50  # aggiungi un padding per assicurarti che i cerchi siano visibili
    all_positions = np.vstack((finalTargetPositions, finalAgentPositions))
    x_min, y_min = np.min(all_positions, axis=0) - padding
    x_max = 400  # Imposta il limite massimo dell'asse X a 400
    y_max = np.max(all_positions[:, 1]) + padding
    ax.set_xlim(x_min, x_max)
    ax.set_ylim(0, 400)  # Imposta y_min a 0 per evitare valori negativi
    
    if plotDir:
        imageDir = os.path.join(os.getcwd(), "Images")
        os.makedirs(imageDir, exist_ok=True)
        plt.savefig(os.path.join(imageDir, plotDir), bbox_inches='tight')
    else:
        plt.show()
    

