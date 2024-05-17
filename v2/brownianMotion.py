import numpy as np
import matplotlib.pyplot as plt

#-------------------------------------------------------------------------------------------------------

def normalDistribution(mu, sigma, n):
    """Restituisce n campioni dalla distribuzione gaussiana N(μ, σ²)."""
    return np.random.normal(mu, sigma, n)


def uniformDistribution(n):
    """Restituisce n campioni dalla distribuzione uniforme U(0, 2π)."""
    return np.random.uniform(0, 2 * np.pi, n)

#-------------------------------------------------------------------------------------------------------

def brownianMotionDef(t, mu, sigma, n):
    """
    Calcola il moto browniano per n punti temporali.

    Parameters:
    t (array-like): Punti temporali.
    mu (float): Media della distribuzione gaussiana.
    sigma (float): Deviazione standard della distribuzione gaussiana.
    n (int): Numero di campioni da generare.

    Returns:
    array: Matrice 2D con vettori [x, y] per ogni punto temporale.
    """
    
    #Qui viene chiamata la funzione uniformDistribution(n) che restituisce n campioni dalla distribuzione
    #uniforme U(0, 2π). Rappresenta gli angoli direzionali causali del movimento browniano.
    theta_i = uniformDistribution(n)
    
    #Qui viene chiamata la funzione normalDistribution(mu, sigma, n) che restituisce n campioni 
    #dalla distribuzione gaussiana N(μ, σ²). Questo rappresenta le intensità (lunghezze) 
    #casuali del movimento.
    gauss_i = normalDistribution(mu, sigma, n)

    #vengono calcolate le coordinate x e y dei vettori di movimento. Si usano le funzioni trigonometriche
    #cos e sin per determinare le componenti orizzontali e verticali del vettore rispettivamente.
    x = gauss_i * np.cos(theta_i)
    y = gauss_i * np.sin(theta_i)

    #Le coordinate x e y vengono combinate in una matrice 2D usando np.vstack((x, y)), che impila 
    #gli array x e y verticalmente. La .T trasposta la matrice, quindi ogni riga rappresenta un 
    #vettore [x, y] per ogni punto temporale. Il risultato è una matrice con forma (n, 2) dove
    #n è il numero di campioni.
    return np.vstack((x, y)).T

#-------------------------------------------------------------------------------------------------------

# ESEMPIO DI UTILIZZO

# # Parametri
# duration = 10  # Cambia questo valore con la durata desiderata
# t = np.arange(duration)  # Punti temporali da 1 a duration
# mu = 0
# sigma = 1
# n = len(t)

# print("Vettore t:", t)  # Stampa il vettore t

# # Calcola il moto browniano
# m_i_t = brownianMotionDef(t, mu, sigma, n)

# # Visualizza il risultato
# plt.plot(m_i_t[:, 0], m_i_t[:, 1], 'o')
# plt.xlabel('x')
# plt.ylabel('y')
# plt.title('Moto Browniano')
# plt.grid(True)
# plt.show()

