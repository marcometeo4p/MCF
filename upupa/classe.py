import numpy as np

class corpo_celeste:
    def __init__(self, nome:str, massa:float, raggio:float, posizione:list, velocita:list):
        self._nome = nome
        self._massa = massa
        self._raggio = raggio
        self._posizione = np.array(posizione, dtype=float)  # (x,y,z)
        self._velocita = np.array(velocita, dtype=float)  # (vx,vy,vz)

        self._cronologia_posizioni:list = [] #lista vuota per appendere le informazioni di posizione nel tempo
        self._cronologia_velocita:list = [] #lista vuota per appendere le informazioni di velocità nel tempo
        self._età :float = 0.0 #tempo trascorso in secondi
        self._cronologia_età:list = [] #lista vuota per appendere le informazioni di età nel tempo

        self._controlla()

    def _controlla(self):
        """
        Controlla se le proprietà del corpo celeste sono valide.
        """
        if not isinstance(self._nome, str):
            raise ValueError("Il nome deve essere una stringa.")
        if not isinstance(self._massa, (int, float)) or self._massa <= 0:
            raise ValueError("La massa deve essere un numero positivo.")
        if not isinstance(self._raggio, (int, float)) or self._raggio <= 0:
            raise ValueError("Il raggio deve essere un numero positivo.")
        if not isinstance(self._posizione, np.ndarray) or self._posizione.shape != (3,):
            raise ValueError("La posizione deve essere un array numpy di dimensione 3.")
        if not isinstance(self._velocita, np.ndarray) or self._velocita.shape != (3,):
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
    def nome(self) -> str:
        """
        Restituisce il nome del corpo celeste.
        """
        return self._nome
    @property
    def età(self) -> float:
        """
        Restituisce l'età del corpo celeste in secondi.
        """
        return self._età
    @property
    def massa(self) -> float:
        """
        Restituisce la massa del corpo celeste in kg.
        """
        return self._massa
    @property
    def raggio(self) -> float:
        """
        Restituisce il raggio del corpo celeste in metri.
        """
        return self._raggio
    @property
    def cronologia_posizioni(self) -> list:
        """
        Restituisce la cronologia delle posizioni del corpo celeste.
        """
        return self._cronologia_posizioni
    @property
    def cronologia_velocita(self) -> list:
        """
        Restituisce la cronologia delle velocità del corpo celeste.
        """
        return self._cronologia_velocita
    @property
    def cronologia_età(self) -> list:
        """
        Restituisce la cronologia delle età del corpo celeste.
        """
        return self._cronologia_età 
    @property
    def posizione(self) -> np.ndarray:
        """
        Restituisce la posizione del corpo celeste come array numpy.
        """
        return self._posizione
    @property
    def velocita(self) -> np.ndarray:
        """
        Restituisce la velocità del corpo celeste come array numpy.
        """
        return self._velocita
    @nome.setter
    def nome(self, valore: str):
        """
        Imposta il nome del corpo celeste.

        :param valore: Il nome da impostare.
        """
        if not isinstance(valore, str):
            raise ValueError("Il nome deve essere una stringa.")
        self._nome = valore
    @cronologia_posizioni.setter
    def cronologia_posizioni(self, valore: list):
        """
        Imposta la cronologia delle posizioni del corpo celeste.

        :param valore: La lista di posizioni da impostare.
        """
        if not isinstance(valore, list):
            raise ValueError("La cronologia delle posizioni deve essere una lista.")
        self._cronologia_posizioni = valore
    @cronologia_velocita.setter
    def cronologia_velocita(self, valore: list):
        """
        Imposta la cronologia delle velocità del corpo celeste.

        :param valore: La lista di velocità da impostare.
        """
        if not isinstance(valore, list):
            raise ValueError("La cronologia delle velocità deve essere una lista.")
        self._cronologia_velocita = valore
    @cronologia_età.setter
    def cronologia_età(self, valore: list):
        """
        Imposta la cronologia delle età del corpo celeste.

        :param valore: La lista di età da impostare.
        """
        if not isinstance(valore, list):
            raise ValueError("La cronologia delle età deve essere una lista.")
        self._cronologia_età = valore
    @posizione.setter
    def posizione(self, valore: list):
        """
        Imposta la posizione del corpo celeste.

        :param valore: La lista di coordinate da impostare.
        """
        if not isinstance(valore, (list, np.ndarray)) or len(valore) != 3:
            raise ValueError("La posizione deve essere una lista o un array numpy di dimensione 3.")
        self._posizione = np.array(valore, dtype=float)
    @velocita.setter
    def velocita(self, valore: list):
        """
        Imposta la velocità del corpo celeste.

        :param valore: La lista di componenti di velocità da impostare.
        """
        if not isinstance(valore, (list, np.ndarray)) or len(valore) != 3:
            raise ValueError("La velocità deve essere una lista o un array numpy di dimensione 3.")
        self._velocita = np.array(valore, dtype=float)
    @massa.setter
    def massa(self, valore: float):
        """
        Imposta la massa del corpo celeste in kg.

        :param valore: La massa da impostare.
        """
        if not isinstance(valore, (int, float)) or valore <= 0:
            raise ValueError("La massa deve essere un numero positivo.")
        self._massa = valore
    @raggio.setter
    def raggio(self, valore: float):
        """
        Imposta il raggio del corpo celeste in metri.

        :param valore: Il raggio da impostare.
        """
        if not isinstance(valore, (int, float)) or valore <= 0:
            raise ValueError("Il raggio deve essere un numero positivo.")
        self._raggio = valore
    @età.setter
    def età(self, valore: float):
        """
        Imposta l'età del corpo celeste in secondi.

        :param valore: L'età da impostare.
        """
        if not isinstance(valore, (int, float)) or valore < 0:
            raise ValueError("L'età deve essere un numero non negativo.")
        self._età = valore


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
        if not isinstance(altro_corpo, corpo_celeste):
            raise ValueError("L'altro corpo deve essere un'istanza di corpo_celeste.")
        # Sfrutta appieno NumPy: molto più veloce e senza cicli for buggati
        return float(np.linalg.norm(self.posizione - altro_corpo.posizione))
