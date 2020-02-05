#Auteur --> aiglematth
#But    --> On gert l'aspect réseau de notre serveur Web

#Imports
from http      import *

#Classes
class SockHTTP():
    """
    Classe qui permet de gérer un client qui communique via le protocole HTTP
    """
    def __init__(self, client):
        """
        On est dans le constructeur
        :param client: Un socket permettant de communiquer avec le client
        """
        self.MAX    = 65535
        self.client = client
        self.client.settimeout(10)

    def run(self):
        """
        On run
        """
        try:
            req = self.client.recv(self.MAX).decode()
            rep = FinalHTTP(req)
            rep = str(rep).encode()
            self.client.send(rep)
        except:
            pass
        finally:
            self.client.close()
