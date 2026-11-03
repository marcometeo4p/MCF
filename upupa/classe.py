import numpy as np

class corpo_celeste:
    def __init__(self, nome:str, massa:float, raggio:float, posizione:list, velocita:list):
        self.nome = nome
        self.massa = massa
        self.raggio = raggio
        self.posizione = np.array(posizione, dtype=float)  # (x,y,z)
        self.velocita = np.array(velocita, dtype=float)  # (vx,vy,vz)

        self.cronologia_posizioni:list = [] #lista vuota per appendere le informazioni di posizione nel tempo
        self.cronologia_velocita:list = [] #lista vuota per appendere le informazioni di velocità nel tempo
        self.età :float = 0.0 #tempo trascorso in secondi
        self.cronologia_età:list = [] #lista vuota per appendere le informazioni di età nel tempo

        self._controlla()

    def _controlla(self):
        """
        Controlla se le proprietà del corpo celeste sono valide.
        """
        if not isinstance(self.nome, str):
            raise ValueError("Il nome deve essere una stringa.")
        if not isinstance(self.massa, (int, float)) or self.massa <= 0:
            raise ValueError("La massa deve essere un numero positivo.")
        if not isinstance(self.raggio, (int, float)) or self.raggio <= 0:
            raise ValueError("Il raggio deve essere un numero positivo.")
        if not isinstance(self.posizione, np.ndarray) or self.posizione.shape != (3,):
            raise ValueError("La posizione deve essere un array numpy di dimensione 3.")
        if not isinstance(self.velocita, np.ndarray) or self.velocita.shape != (3,):
            raise ValueError("La velocità deve essere un array numpy di dimensione 3.")

    def _controllo_collisione(self, altro_corpo) -> bool:
        """
        Controlla se questo corpo celeste collide con un altro corpo celeste.

        :param altro_corpo: Un'istanza di corpo_celeste con cui controllare la collisione.
        :return: True se i corpi collidono, False altrimenti.
        """
        if not isinstance(altro_corpo, corpo_celeste):
            raise ValueError("L'altro corpo deve essere un'istanza di corpo_celeste.")
        
        distanza = self.distanza_da(altro_corpo)
        raggio_totale = self.raggio + altro_corpo.raggio
        
        return distanza <= raggio_totale

    @property
    def età(self) -> float:
        """
        Restituisce l'età del corpo celeste in secondi.
        """
        return self.età
    @età.setter
    def età(self, valore: float):
        """
        Imposta l'età del corpo celeste in secondi.

        :param valore: L'età da impostare.
        """
        if not isinstance(valore, (int, float)) or valore < 0:
            raise ValueError("L'età deve essere un numero non negativo.")
        self.età = valore

    def aggiorna_cronologia(self):
        """
        Aggiorna le cronologie di posizione, velocità ed età del corpo celeste, appendendo i valori correnti.
        """
        self.cronologia_posizioni.append(self.posizione.copy())
        self.cronologia_velocita.append(self.velocita.copy())
        self.cronologia_età.append(self.età)
    
    def __str__(self):
        s="Corpo Celeste: {self.nome}\n, Massa: {self.massa} kg\n, Raggio: {self.raggio} m\n, Posizione: {self.posizione}\n, Velocità: {self.velocita}\n, Età: {self.età} s"
        return format(s)
    
    def distanza_da(self, altro_corpo) -> float:
        """
        Calcola la distanza tra questo corpo celeste e un altro corpo celeste.

        :param altro_corpo: Un'istanza di corpo_celeste con cui calcolare la distanza.
        :return: La distanza tra i due corpi celesti.
        """
        #np.linalg.norm(self.posizione - altro_corpo.posizione)
        if not isinstance(altro_corpo, corpo_celeste):
            raise ValueError("L'altro corpo deve essere un'istanza di corpo_celeste.")
        delta_r_array = []
        for i in range(3):
            '''if not isinstance(altro_corpo.posizione[i], (int, float)):
                raise ValueError("Le coordinate della posizione dell'altro corpo devono essere numeri.")'''
            ((altro_corpo.posizione[i] - self.posizione[i])**2).append(delta_r_array)
        return  np.sqrt(sum(delta_r_array))
