import os
import matplotlib.pyplot as plt

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
    plt.title('Traiettorie delle barche (Targets) e Posizioni iniziali degli agenti')
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
    plt.title('Traiettorie delle barche (Targets) e degli agenti (Droni)')
    plt.legend(loc='upper left', bbox_to_anchor=(1, 1))
    plt.grid(True)
    
    if plotDir:
        imageDir = os.path.join(os.getcwd(), "Images")
        os.makedirs(imageDir, exist_ok=True)
        plt.savefig(os.path.join(imageDir, plotDir), bbox_inches='tight')
    else:
        plt.show()

