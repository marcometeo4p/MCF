import numpy as np
def somma_naturali(n):
    """
    Calcola la somma dei primi n numeri naturali.

    Args:
        n (int): Il numero fino al quale calcolare la somma.

    Returns:
        int: La somma dei primi n numeri naturali.
    """
    if n < 0:
        raise ValueError("Il numero deve essere non negativo.")
    return np.sum(np.arange(n + 1)) 

def somma_sqrt(n):
    """
    Calcola la somma delle radici quadrate dei primi n numeri naturali.

    Args:
        n (int): Il numero fino al quale calcolare la somma delle radici quadrate.

    Returns:
        float: La somma delle radici quadrate dei primi n numeri naturali.
    """
    if n < 0:
        raise ValueError("Il numero deve essere non negativo.")
    return np.sum(np.sqrt(np.arange(n + 1)))

def somma_prod(n):
    """
    Calcola la somma e il prodotto dei primi n numeri naturali.

    Args:
        n (int): Il numero fino al quale calcolare la somma e il prodotto.

    Returns:
        tuple: Una tupla contenente la somma e il prodotto dei primi n numeri naturali.
    """
    if n < 0:
        raise ValueError("Il numero deve essere non negativo.")
    somma = somma_naturali(n)
    prodotto = 1
    for i in range(1, n + 1):
        prodotto=prodotto * i
    #prodotto = np.prod(np.arange(1, n + 1))
    return somma, prodotto

def somma_alfa(n, alfa=1.0):
    """
    Calcola la somma dei primi n numeri naturali elevati a una potenza alfa.

    Args:
        n (int): Il numero fino al quale calcolare la somma.
        alfa (float): La potenza alla quale elevare i numeri naturali.

    Returns:
        float: La somma dei primi n numeri naturali elevati a potenza alfa.
    """
    if n < 0:
        raise ValueError("Il numero deve essere non negativo.")
    return np.sum(np.arange(n + 1) ** alfa)