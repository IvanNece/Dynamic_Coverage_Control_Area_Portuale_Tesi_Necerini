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
