import pickle
import sys
import matplotlib.pyplot as plt
import logging
import numpy as np

from createTheSetOfTargets import printDataset, buildTheSet, plotTrajectories, plotStartingPointOfTrajectories, extractInitialTargetPositions
from createTheSetOfAgents import generateInitialAgentPositions, plotInitialAgentPositions
from initialCoverageIndices import calculateE_00_0, calculateInitialCoverageIndices, calculateInitialTotalCoverageIndex
from plotMergeFunctions import plotTrajectoriesWithAgentStartPoints, plotAll, plotFinalSetWithRadius
from gradient import gradientOfInitialCoverageIndex
from coverageIndices import calculateCoverageIndices, calculateTotalCoverageIndex, calculateTotalCoverageIndexWithoutSigmoid
from testTotalCoverageIndex import plotTotalCoverageIndex, plotTotalCoverageIndexStopped, calculateCoverageIndicesStopped

import v1.coverageAlgorithmV1
import v2.coverageAlgorithmV2
import v3.coverageAlgorithmV3

#---------------------------------------------------------------------------------------------------------

def main():
    
    # DEFINIZIONE PARAMETRI IMPORTANTI
    
    numTargets = 10 # numero di traittorie selezionate, target (barche)
    duration = 150 # secondi di durata delle traiettorie
    numAgents = 4   # numero di agenti (droni)
    initialAreaSize = 200   # dimensione dell'area iniziale dove stanno a t=0 i target e gli agenti
    r = 150 # raggio di visione degli agenti (droni)
    mp = 1   # peak sensing quality
    epsilon = 150  # passi di salita, decide la velocità degli agenti
    lowerboundIndex = 1 # indice di copertura minimo accettabile, =E* nella funzione sigmoidale
    h = 1e-10   # h = sensibilità del calcolo del gradiente
    delta = 30   # distanza di allontanamento tra agenti
   
    
    #------------------------------------------------------------------------------------------
    # 1, 2.1) CARICO IL DATASET E CREO UNO SCENARIO DI TRAIETTORIE DI TARGET SELZIONATE
    
    # Apri il file per scrivere l'output, nel file txt ci metto le traiettorie selezionate
    with open('outputSetTargets.txt', 'w') as f:
        # Salva l'output standard in una variabile per ripristinarlo successivamente
        original_stdout = sys.stdout
        
        # Redirigi l'output standard verso il file
        sys.stdout = f
        
        try:
            with open("dataset.pkl", "rb") as f:
                inputDataset = pickle.load(f)
                print('Dataset caricato correttamente')
        except Exception as e:
            print("Errore durante il caricamento del dataset:", e)
            
        createdDatasetOfTargets = buildTheSet(numTargets, inputDataset, duration)
        printDataset(createdDatasetOfTargets)
        plotTrajectories(createdDatasetOfTargets, plotDir="selectedTrajectories.png")
        
        # Ripristina l'output standard
        sys.stdout = original_stdout
    
    print(f"\n\nE' stato creato uno scenario con {numTargets} traiettorie selezionate della durata di "
      f"{duration} secondi. I dettagli dello scenario sono stati salvati "
      f"in 'outputSetTargets.txt'.\n\n")
    
    
    # # Estrarre solo la parte truncated_measurement
    targets = [truncated_measurement for _, truncated_measurement in createdDatasetOfTargets]
    targetTrajectories = np.array(targets)
    
    print("\nDimensione della lista della parte di 'measurement' delle 'targetTrajectories':")
    print(targetTrajectories.shape)
    
    
    #------------------------------------------------------------------------------------------
    # 2.2) CREO UN GRAFICO DELLE TRAIETTORIE SELEZIONATE, CON SOLO IL LORO PUNTO DI PARTENZA
    
    plotStartingPointOfTrajectories(createdDatasetOfTargets, plotDir="startingPoints.png")
     
     
    #------------------------------------------------------------------------------------------
    # 3) CREO UNO SCENARIO INIZIALE DI AGENTI (DRONI) E CALCOLO GLI INDICI DI COPERTURA A t=0 
    # PER OGNI TARGET
    
    # Estrai le posizioni iniziali dei target dalle misure
    initialTargetPositions = extractInitialTargetPositions(targetTrajectories, numTargets)
    # Stampa le posizioni iniziali dei target
    #VERIFICATO CHE L'HO FATTO CORRETTAMENTE
    print("\n\nPosizioni iniziali dei target:")
    print(initialTargetPositions)
    print(initialTargetPositions.shape)
    
    
    #TODO FARLO PIU OTTIMIZZATO MAGARI USANDO ANCHE initialTargetPositions??? 
    # Genera le posizioni iniziali degli agenti
    initialAgentPositions = generateInitialAgentPositions(numAgents, initialAreaSize, r)
        
    # Stampa le posizioni iniziali degli agenti
    print("\nPosizioni iniziali degli agenti:")
    for i, (x, y) in enumerate(initialAgentPositions):
        print(f"Agente {i+1}: x = {x}, y = {y}")
        
    print(initialAgentPositions.shape)
        
    # Plot delle posizioni iniziali degli agenti
    plotInitialAgentPositions(initialAgentPositions, plotDir="initialAgentPositions.png")
    
    # calcolo E_00_0 come prova, sarebbe E00(0)
    #E_00_0 = calculateE_00_0(createdDatasetOfTargets, initialAgentPositions, r, mp)
    
    # # adesso devo calcolare gli indici di copertura di ogni target j all'istante t=0
    # # CALCOLO INDICI DI COPERTURA ALL'ISTANTE INIZIALE
    # # TODO: controllare che siano tutti >= E*
    initialCoverageIndices = calculateInitialCoverageIndices(targetTrajectories, initialAgentPositions, r, mp)
    print("\n\nINDICI DI COPERTURA INIZIALI E_j AL TEMPO t=0:")
    for i, coverage_index in enumerate(initialCoverageIndices):
        print(f"E_{i}_(0): {coverage_index}")
        
    # ora plotto il grafico delle traiettorie, insieme agli starting point degli agenti
    plotTrajectoriesWithAgentStartPoints(createdDatasetOfTargets, initialAgentPositions, plotDir="trajectoriesWithAgentStartPoints.png")
    
    
    #------------------------------------------------------------------------------------------
    # 4) CALCOLO L'EFFETTIVO INDICE DI COPERTURA COMPLESSIVO ALL'ISTANTE t=0
    
    print("\n")
    
    # QUESTA PARTE SI PUO' ANCHE COMMENTARE, DATO CHE PASSO TUTTO ALLA FUNZIONE GRADIENTE TANTO
    totalCoverageIndex_0 = calculateInitialTotalCoverageIndex(initialCoverageIndices, lowerboundIndex)
    print(f"\nINDICE DI COPERTURA COMPLESSIVO ALL'ISTANTE t=0: \nE(0): {totalCoverageIndex_0}")
    
    # 4.1) CALCOLO GRADIENTE INDICE DI COPERTURA COMPLESSIVO A t=0, PER OGNI AGENTE i
    # initalGradients = gradientOfInitialCoverageIndex(createdDatasetOfTargets, initialAgentPositions, r, mp, lowerboundIndex, h)
    # print("\nGRADIENTE INDICE DI COPERTURA COMPLESSIVO A t=0, PER OGNI AGENTE i:")
    # for i, gradient in enumerate(initalGradients):
    #     print(f"Agente {i+1}: {gradient}")
        
    #------------------------------------------------------------------------------------------
    # 5) ALGORITMO V1
    
    agentTrajectoriesV1 = v1.coverageAlgorithmV1.coverageAlgorithmV1(targetTrajectories, initialAgentPositions, r, mp, lowerboundIndex, h, numAgents, duration, epsilon)
    
    #print("\nShape dell'array agentTrajectoriesV1:")
    #print(agentTrajectoriesV1.shape)
    #print(agentTrajectoriesV1[duration-1].shape)
    
    # # Stampa le traiettorie degli agenti
    # print("\n\nTraiettorie degli agenti:")
    # for i, agent_trajectory in enumerate(agentTrajectoriesV1):
    #     print(f"Agente al tempo {i+1}:\n{agent_trajectory}")
    
    plotAll(createdDatasetOfTargets, agentTrajectoriesV1, plotDir="finalTrajectoriesV1.png")
    
    # # CONTROLLO GLI INDICI DI COPERTURA AL TEMPO FINALE
    # # adesso devo calcolare gli indici di copertura di ogni target j all'istante t=finale
    # # per verificare che siano tutti >= E*, scopo del progetto
    # # TODO: controllare che siano tutti >= E*
    finalCoverageIndicesV1 = calculateCoverageIndices(targetTrajectories, agentTrajectoriesV1[duration-1], duration-1, r, mp)
    print("\nVERSIONE 1 ALGORITMO \nINDICI DI COPERTURA FINALI E_j AL TEMPO t=150:")
    for i, coverage_index in enumerate(finalCoverageIndicesV1):
        print(f"E_{i}_({duration}): {coverage_index}")
    
    # CALCOLO INDICE DI COPERTURA TOTALE ALL'ISTANTE FINALE, PER VEDERE SE MIGLIORA RISPETTO A t=0
    totalCoverageIndexFinal = calculateTotalCoverageIndex(finalCoverageIndicesV1, lowerboundIndex)
    print(f"\nINDICE DI COPERTURA COMPLESSIVO ALL'ISTANTE V1 t=finale: \nE(finale): {totalCoverageIndexFinal}")
    
        
    #------------------------------------------------------------------------------------------
    # 6) ALGORITMO V2
    
    agentTrajectoriesV2 = v2.coverageAlgorithmV2.coverageAlgorithmV2(targetTrajectories, initialAgentPositions, r, mp, lowerboundIndex, h, numAgents, duration, epsilon)
    
    plotAll(createdDatasetOfTargets, agentTrajectoriesV2, plotDir="finalTrajectoriesV2.png")
    
    # # #CONTROLLO GLI INDICI DI COPERTURA AL TEMPO FINALE
    # # # adesso devo calcolare gli indici di copertura di ogni target j all'istante t=finale
    # # # TODO: controllare che siano tutti >= E*
    # # # TODO: cambiare parametri e vedere che succede, sigma e media distribuzione normale
    # # finalCoverageIndicesV2 = calculateCoverageIndices(createdDatasetOfTargets, agentTrajectoriesV2[duration-1], duration-1, r, mp)
    # # print("\nVERSIONE 2 ALGORITMO, AGGIUNTA MOTO BROWNIANO \nINDICI DI COPERTURA FINALI E_j AL TEMPO t=200:")
    # # for i, coverage_index in enumerate(finalCoverageIndicesV2):
    # #     print(f"E_{i}_(200): {coverage_index}")
        
    #------------------------------------------------------------------------------------------
    # 7) ALGORITMO V3
    agentTrajectoriesV3 = v3.coverageAlgorithmV3.coverageAlgorithmV3(targetTrajectories, initialAgentPositions, r, mp, lowerboundIndex, h, numAgents, duration, epsilon, delta)
    
    plotAll(createdDatasetOfTargets, agentTrajectoriesV3, plotDir="finalTrajectoriesV3.png")
    
    # # #CONTROLLO GLI INDICI DI COPERTURA AL TEMPO FINALE
    # # # adesso devo calcolare gli indici di copertura di ogni target j all'istante t=finale
    # # # TODO: controllare che siano tutti >= E*
    # # # TODO: cambiare parametri e vedere che succede, delta distanza nel calcolo del pot repulsivo
    # # finalCoverageIndicesV3 = calculateCoverageIndices(createdDatasetOfTargets, agentTrajectoriesV3[duration-1], duration-1, r, mp)
    # # print("\nVERSIONE 3 ALGORITMO, AGGIUNTA POTENZIALE REPULSIVO \nINDICI DI COPERTURA FINALI E_j AL TEMPO t=200:")
    # # for i, coverage_index in enumerate(finalCoverageIndicesV3):
    # #     print(f"E_{i}_(200): {coverage_index}")
    
    
    #-----------------------------------------------------------------------------------------------------
    #TEST GRAFICO INDICE DI COPERTURA TOTALE--------------------------------------------------------------
    #V1
    totalCoverageIndex_values = []
    for t in range(duration):
        coverageIndices_t = calculateCoverageIndices(targetTrajectories, agentTrajectoriesV1[t], t, r, mp)
        totalCoverageIndex_t = calculateTotalCoverageIndex(coverageIndices_t, lowerboundIndex)
        totalCoverageIndex_values.append(totalCoverageIndex_t)

    print("\nIndice di copertura totale iniziale e finale V1 CLASSICA:\n")
    print(totalCoverageIndex_values[0])
    print(totalCoverageIndex_values[duration-1])
    
    #print(np.array(totalCoverageIndex_values).shape)
    
    # Plotting del totalCoverageIndex nel tempo
    # Chiamata alla funzione per fare il grafico
    plotTotalCoverageIndex(totalCoverageIndex_values, plotDir="V1_totalCoverageIndexOverTime.png")
    
    #-----------------------------------------------------------------------------------------------------
    
    # # #TEST GRAFICO INDICE DI COPERTURA TOTALE--------------------------------------------------------------
    # # #V1, CON TARGET FERMI!!!
    
    # #print(initialTargetPositions)
    # tempTargetPositions = np.tile(initialTargetPositions, (1, duration, 1))
    # #print(tempTargetPositions.shape)
    # #sarà dunque correttamente un numTargets x duration x 2
    # #print(tempTargetPositions[9])
    
    # totalCoverageIndex_values_stoppedTargets = []
    # for t in range(duration):
    #     coverageIndices_t_stop = calculateCoverageIndices(tempTargetPositions, agentTrajectoriesV1[t], t, r, mp)
    #     totalCoverageIndex_t_stop = calculateTotalCoverageIndex(coverageIndices_t_stop, lowerboundIndex)
    #     totalCoverageIndex_values_stoppedTargets.append(totalCoverageIndex_t_stop)
        
    # print("\nIndice di copertura totale iniziale e finale V1 CON TARGET FERMI:\n")
    # print(totalCoverageIndex_values_stoppedTargets[0])
    # print(totalCoverageIndex_values_stoppedTargets[duration-1])

    # # # Plotting del totalCoverageIndex nel tempo
    # # # Chiamata alla funzione per fare il grafico
    # plotTotalCoverageIndexStopped(totalCoverageIndex_values_stoppedTargets, plotDir="V1_totalIndexWithSTOPPEDtarget.png")
    
    # #-----------------------------------------------------------------------------------------------------
    # #TEST GRAFICO INDICE DI COPERTURA TOTALE--------------------------------------------------------------
    # #V1 SENZA SIGMOIDE!!!
    # totalCoverageIndex_values_noSigmoid = []
    # for t in range(duration):
    #     coverageIndices_t_noSigmoid = calculateCoverageIndices(targetTrajectories, agentTrajectoriesV1[t], t, r, mp)
    #     totalCoverageIndex_t_noSigmoid = calculateTotalCoverageIndexWithoutSigmoid(coverageIndices_t_noSigmoid)
    #     totalCoverageIndex_values_noSigmoid.append(totalCoverageIndex_t_noSigmoid)
        
    # print("\nIndice di copertura totale iniziale e finale V1 NO SIGMOIDE:\n")
    # print(totalCoverageIndex_values_noSigmoid[0])
    # print(totalCoverageIndex_values_noSigmoid[duration-1])    
    
    # plotTotalCoverageIndex(totalCoverageIndex_values_noSigmoid, plotDir="V1_totalCoverageIndexOverTimeNoSigmoid.png")
    
    # #-----------------------------------------------------------------------------------------------------

    
#------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------
    #TEST GRAFICO INDICE DI COPERTURA TOTALE--------------------------------------------------------------
    #V2
    totalCoverageIndex_valuesV2 = []
    for t in range(duration):
        coverageIndices_tV2 = calculateCoverageIndices(targetTrajectories, agentTrajectoriesV2[t], t, r, mp)
        totalCoverageIndex_tV2 = calculateTotalCoverageIndex(coverageIndices_tV2, lowerboundIndex)
        totalCoverageIndex_valuesV2.append(totalCoverageIndex_tV2)


    finalCoverageIndicesV2 = calculateCoverageIndices(targetTrajectories, agentTrajectoriesV2[duration-1], duration-1, r, mp)
    print("\nVERSIONE 2 ALGORITMO \nINDICI DI COPERTURA FINALI E_j AL TEMPO t=150:")
    for i, coverage_index in enumerate(finalCoverageIndicesV2):
        print(f"E_{i}_({duration}): {coverage_index}")
    

    print("\nIndice di copertura totale iniziale e finale V2 CLASSICA:\n")
    print(totalCoverageIndex_valuesV2[0])
    print(totalCoverageIndex_valuesV2[duration-1])
    
    #print(np.array(totalCoverageIndex_values).shape)
    
    # Plotting del totalCoverageIndex nel tempo
    # Chiamata alla funzione per fare il grafico
    plotTotalCoverageIndex(totalCoverageIndex_valuesV2, plotDir="V2_totalCoverageIndexOverTime.png")


# # #TEST GRAFICO INDICE DI COPERTURA TOTALE--------------------------------------------------------------
#     # #V2, CON TARGET FERMI!!!
    
#     #print(initialTargetPositions)
#     tempTargetPositions = np.tile(initialTargetPositions, (1, duration, 1))
#     #print(tempTargetPositions.shape)
#     #sarà dunque correttamente un numTargets x duration x 2
#     #print(tempTargetPositions[9])
    
#     totalCoverageIndex_values_stoppedTargetsV2 = []
#     for t in range(duration):
#         coverageIndices_t_stopV2 = calculateCoverageIndices(tempTargetPositions, agentTrajectoriesV2[t], t, r, mp)
#         totalCoverageIndex_t_stopV2 = calculateTotalCoverageIndex(coverageIndices_t_stopV2, lowerboundIndex)
#         totalCoverageIndex_values_stoppedTargetsV2.append(totalCoverageIndex_t_stopV2)
        
#     print("\nIndice di copertura totale iniziale e finale V2 CON TARGET FERMI:\n")
#     print(totalCoverageIndex_values_stoppedTargetsV2[0])
#     print(totalCoverageIndex_values_stoppedTargetsV2[duration-1])

#     # # Plotting del totalCoverageIndex nel tempo
#     # # Chiamata alla funzione per fare il grafico
#     plotTotalCoverageIndexStopped(totalCoverageIndex_values_stoppedTargetsV2, plotDir="V2_totalIndexWithSTOPPEDtarget.png")

#------------------------------------------------------------------------------------------

#------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------
    #TEST GRAFICO INDICE DI COPERTURA TOTALE--------------------------------------------------------------
    #V3
    totalCoverageIndex_valuesV3 = []
    for t in range(duration):
        coverageIndices_tV3 = calculateCoverageIndices(targetTrajectories, agentTrajectoriesV3[t], t, r, mp)
        totalCoverageIndex_tV3 = calculateTotalCoverageIndex(coverageIndices_tV3, lowerboundIndex)
        totalCoverageIndex_valuesV3.append(totalCoverageIndex_tV3)


    finalCoverageIndicesV3 = calculateCoverageIndices(targetTrajectories, agentTrajectoriesV3[duration-1], duration-1, r, mp)
    print("\nVERSIONE 3 ALGORITMO \nINDICI DI COPERTURA FINALI E_j AL TEMPO t=150:")
    for i, coverage_index in enumerate(finalCoverageIndicesV3):
        print(f"E_{i}_({duration}): {coverage_index}")
    
    print("\nIndice di copertura totale iniziale e finale V3 CLASSICA:\n")
    print(totalCoverageIndex_valuesV3[0])
    print(totalCoverageIndex_valuesV3[duration-1])
    
    #print(np.array(totalCoverageIndex_values).shape)
    
    # Plotting del totalCoverageIndex nel tempo
    # Chiamata alla funzione per fare il grafico
    plotTotalCoverageIndex(totalCoverageIndex_valuesV3, plotDir="V3_totalCoverageIndexOverTime.png")


# # #TEST GRAFICO INDICE DI COPERTURA TOTALE--------------------------------------------------------------
#     # #V3, CON TARGET FERMI!!!
    
#     #print(initialTargetPositions)
#     tempTargetPositions = np.tile(initialTargetPositions, (1, duration, 1))
#     #print(tempTargetPositions.shape)
#     #sarà dunque correttamente un numTargets x duration x 2
#     #print(tempTargetPositions[9])
    
#     totalCoverageIndex_values_stoppedTargetsV3 = []
#     for t in range(duration):
#         coverageIndices_t_stopV3 = calculateCoverageIndices(tempTargetPositions, agentTrajectoriesV3[t], t, r, mp)
#         totalCoverageIndex_t_stopV3 = calculateTotalCoverageIndex(coverageIndices_t_stopV3, lowerboundIndex)
#         totalCoverageIndex_values_stoppedTargetsV3.append(totalCoverageIndex_t_stopV3)
        
#     print("\nIndice di copertura totale iniziale e finale V3 CON TARGET FERMI:\n")
#     print(totalCoverageIndex_values_stoppedTargetsV3[0])
#     print(totalCoverageIndex_values_stoppedTargetsV3[duration-1])

#     # # Plotting del totalCoverageIndex nel tempo
#     # # Chiamata alla funzione per fare il grafico
#     plotTotalCoverageIndexStopped(totalCoverageIndex_values_stoppedTargetsV3, plotDir="V3_totalIndexWithSTOPPEDtarget.png")


#------------------------------------------------------------------------------------------

    #GRAFICO FINALE
    plotFinalSetWithRadius(targetTrajectories, agentTrajectoriesV3, duration, r, plotDir="finalSetWithRadius.png")

#------------------------------------------------------------------------------------------

if __name__ == "__main__":
    main()