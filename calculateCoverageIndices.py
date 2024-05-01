

# calcolo degli indici di copertura al tempo t=0 per ogni target j
def calculateInitialCoverageIndices(targets: list, initialAgents: list):
    
    trajectory0 = targets[0]
    measurement0 = trajectory0[1]
    qx0 = measurement0[0, 0]
    #se metto :,0 ottengo tutte le coordinate x di tutte le traiettorie
    qy0 = measurement0[0, 1]
    
    print("Coordinate del target 0 al tempo t=0:\n")
    print(qx0)
    print("\n")
    print(qy0)
    
    #TODO MI TORNA CHE PRENDO (X,Y) DELLE MEASUREMENT DEL TARGET 0 AL TEMPO 0 (PRIMA RIGA OUTOPUT)
    