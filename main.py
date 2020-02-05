#Auteur --> aiglematth
#But    --> Corps de notre serveur WEB

#Imports
from socket import socket, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR
from http   import *
from server import *

#Variables
BIND = ("", 80)

#Main
with socket(AF_INET, SOCK_STREAM) as sock:

    sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1) #Permet de réutiliser le socket si celui-ci est en time_wait (pas totalement fermé)
    sock.bind(BIND)
    sock.listen(5)

    print("### Lancement du serveur ###")

    while True:
        try:
            print("--- Attente ---")
            (client, infos) = sock.accept()
            print(f"### {infos} ###")
            SockHTTP(client).run()
        except KeyboardInterrupt:
            break
