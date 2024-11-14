##Implémentation du protocole d'identification de Schnoor sur le groupe Zq (Version décrite sur cette page : https://www.emanuelecivini.com/post/schnorr-id/)

from classes import *
import sympy as sp ##Bibliothèque pour générer des nombres premiers aléatoires
from random import randint


def generer_premier(inf,sup):
    return sp.randprime(inf,sup)

def generer_cle(q, g):
    s = randint(2,q-1)
    gs = pow(g,s,q) ## cle = g**s modulo q
    return (s,gs)


def engagement(alice,bob):
    (a,ga) = generer_cle(alice.q,alice.g)
    alice.a=a
    alice.envoyer(bob,"ga",ga)

def defi(alice,bob):
    b= randint(2,bob.q-1)
    bob.b=b
    bob.envoyer(alice,"b",b)
    return b

def reponse(alice,bob):
    s = alice.certificats[bob.id][0]
    c = (alice.a + alice.b*s)
    alice.envoyer(bob,"c",c)

def verification(bob):

    gc = pow(bob.g,bob.c,bob.q)
    t=(bob.ga*pow(bob.gs,bob.b,bob.q))%bob.q
    return t==gc ## t = r*cle^b = g^a*g^bs = g^(a+bs) = g^c




def protocole_authentification_schnoor(alice,bob):

    for i in range(bob.nb_repetitions):


        engagement(alice,bob)

        defi(alice,bob)
        reponse(alice,bob)

        if(not(verification(bob))):
            print(i)
            return False
        
    return True


def authentification(alice,bob):
    alice.envoyer(bob,"gs",alice.certificats[bob.id][1]) ##L'utilisateur envoie sa clé publique

    bob.envoyer(alice,"q",bob.q)
    bob.envoyer(alice,"g",bob.g)

    reussite = protocole_authentification_schnoor(alice,bob)
    print(reussite)

    pass


inf = 2**(k-1)
sup = 2*inf -1
def main(k):
    alice = Utilisateur()
    q = generer_premier(inf,sup)
    g = randint(2,q-1)
    id = 0
    nb_repetitions = 1000

    (s,gs) = generer_cle(q,g)
    alice.certificats[id]=(s,gs)

    bob = Proprietaire(g,q, id, nb_repetitions)

    authentification(alice,bob)

k = 256 ## Nombre de bits utilisés pour la clé
main(k)
