#Auteur --> aiglematth
#But    --> Offrir les outils pour recevoir / envoyer via le protocole HTTP

#Imports
from os import chroot

#Classes
class HTTP():
    """
    Contient les constantes dont nous auront besoin^^
    """
    def __init__(self):
        """
        Constructeur de la classe
        """
        self.SEPARATEUR_LIGNE = "\r\n"
        self.FIN_PAQUET       = "\r\n\r\n"
        self.SEPARATEUR_GET   = "?"
        self.SEPARATEUR_DATA  = "&"
        self.EGAL             = "="
        self.EGAL_CHAMP       = ":"
        self.code_for         = {
            "200" : "OK",
            "404" : "Not Found"
        }

class ParseHTTP(HTTP):
    """
    Classe ParseHttp :
    Permet de parser une requête HTTP
    """
    def __init__(self, req):
        """
        Constructeur de la classe
        :param req: La requete à parser
        """
        self.req              = req
        self.dic              = None
        HTTP.__init__(self)

    def parse(self):
        """
        Parser de la requete :
        HTTP --> fin de ligne    :> \r\n
             --> fin de requete  :> \r\n\r\n
             --> separateur      :> :
             --> param POST|GET  :> SEPARATEUR & VALEUR =
        {
            METHODE : valeur,
            FICHIER : valeur,
            VERSION : valeur,
            champ : valeur,
            champ : valeur,
            champ : valeur,
            [...],
            POST  : {
                        champ : valeur,
                        champ : valeur,
                        champ : valeur,
                        [...],
                        champ : valeur
                    },
            GET  : {
                        champ : valeur,
                        champ : valeur,
                        champ : valeur,
                        [...],
                        champ : valeur
                    },
        }
        """
        #Variables
        dic = {}
        #On split tout le corps du message
        champs = self.req.split(self.SEPARATEUR_LIGNE)
        #Maintenant on commence le remplissage
        dic["METHODE"] = champs[0].split(" ")[0].strip()
        dic["FICHIER"] = champs[0].split(" ")[1].strip()
        dic["VERSION"] = champs[0].split(" ")[2].strip()
        champs.__delitem__(0)
        #On tcheck si il y a des parametres passées en GET
        dic["GET"] = {}
        fichier    = dic["FICHIER"].split(self.SEPARATEUR_GET)
        dic["FICHIER"] = dic["FICHIER"].split(self.SEPARATEUR_GET)[0]
        if dic["FICHIER"] == "/":
            dic["FICHIER"] = "/index.html"
        if len(fichier) > 1:
            for data_brut in fichier[1].split(self.SEPARATEUR_DATA):
                try:
                    (champ, value) = data_brut.split(self.EGAL)
                except:
                    champ = data_brut.split(self.EGAL)[0]
                    value = ""
                finally:
                    dic["GET"][champ.strip()] = value.strip()
        #Maintenant on va tcheck les paramètres passées en POST
        if dic["METHODE"] == "POST":
            data_brut = champs[len(champs) - 1].split(self.SEPARATEUR_DATA)
            for data in data_brut:
                try:
                    (champ, value) = data_brut.split(self.EGAL)
                except:
                    champ = data_brut.split(self.EGAL)[0]
                    value = ""
                finally:
                    dic["POST"][champ.strip()] = value.strip()
        champs.__delitem__(len(champs) - 1)
        #On remplit les autres champs
        for champ in champs:
            try:
                (champ, value) = champ.split(self.EGAL_CHAMP)
            except:
                champ = champ.split(self.EGAL_CHAMP)[0]
                value = ""
            finally:
                if champ != "":
                    dic[champ.strip()] = value.strip()
        #On met tout ca dans notre self.dic
        self.dic = dic

class ReponseHTTP(HTTP):
    """
    On forme la requête réponse...on se contentera de la base ^^
    """
    def __init__(self, code, html=""):
        """
        Constructeur de la classe
        :param code: Code réponse, on va définir juste OK(200) et NOT_FOUND(404)
        :param html: Le code html
        """
        self.code     = code
        self.html     = html
        self.response = None
        HTTP.__init__(self)
        self.construct()

    def construct(self):
        """
        On construit la reponse
        """
        rep = f"HTTP/1.1 {self.code} {self.code_for[self.code]}{self.FIN_PAQUET}"
        if self.html != "":
            rep += self.html
            rep += self.FIN_PAQUET
        self.response = rep

    def __str__(self):
        return self.response

class FinalHTTP(ParseHTTP):
    """
    Va être utilisée afin de créer rapidement la réponse
    """
    def __init__(self, req):
        self.finalRep = ""
        self.code     = None
        ParseHTTP.__init__(self, req)
        self.parse()
        self.final()

    def final(self):
        """
        Permet de remplir finalRep
        """
        #On se chroot dans le dossier actuel
        chroot(".")
        html        = None
        htmlContent = ""
        try:
            with open("html/" + self.dic["FICHIER"][1:], "r") as file:
                html = file.readlines()
            for line in html:
                htmlContent += line
            self.code = "200"
        except:
            self.code = "404"
        finally:
            self.finalRep = ReponseHTTP(self.code, html=htmlContent)
            self.finalRep = str(self.finalRep)

    def __str__(self):
        return self.finalRep
