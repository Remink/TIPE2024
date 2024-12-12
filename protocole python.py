##Implémentation d'une version du protocole d'identification de Schnoor sur le groupe Zq en supprimant la contrainte "g est un générateur d'ordre q de Zq"

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
    return t==gc ## t = ga*gs^b = g^a*g^bs = g^(a+bs) = g^c




def protocole_authentification_schnoor(alice,bob):
    print("Protocole d'authentification de schnorr")
    for i in range(bob.nb_repetitions):


        engagement(alice,bob)

        defi(alice,bob)
        reponse(alice,bob)

        if(not(verification(bob))):
            print("Bob n'accepte pas")
            return False
    
    print("Bob accepte")
    return True

def reponse2(alice,bob):
    s = alice.certificats[bob.id][0]
    c = (alice.a - alice.b*s)% alice.q
    alice.envoyer(bob,"c",c)

def verification2(alice,bob):
    ##print(bob.ga)
    ##print((pow(bob.g,bob.c,bob.q)*pow(bob.gs,bob.b,bob.q)%bob.q))
    return bob.ga == (pow(bob.g,bob.c,bob.q)*pow(bob.gs,bob.b,bob.q))

def test_protocole(alice,bob):
    print("Protocole vu dans la littérature, mais ne marche pas si g n'est pas d'ordre q :")
    engagement(alice,bob)
    defi(alice,bob)
    reponse2(alice,bob)
    if( verification2(alice,bob)):
        print("Bob accepte")
    else:
        print("Bob refuse")




def protocole_defectueux(alice,bob):
    print("Protocole defectueux :")
    engagement(alice,bob)
    defi(alice,bob)
    reponse(alice,bob)

    b1=bob.b
    c1=bob.c

    defi(alice,bob)
    reponse(alice,bob)
    b2=bob.b
    c2=bob.c

    s2 = ((c1-c2)//(b1-b2))
    print("La clé que bob a extraire est :" + str(int(s2)))
    print("la clé d'alice est : " + str(alice.certificats[bob.id][0]))


def authentification(alice,bob):
    alice.envoyer(bob,"gs",alice.certificats[bob.id][1]) ##L'utilisateur envoie sa clé publique

    bob.envoyer(alice,"q",bob.q)
    bob.envoyer(alice,"g",bob.g)

    reussite = protocole_authentification_schnoor(alice,bob)
    

    pass



def main(k):
    inf = 2**(k-1)
    sup = 2*inf -1
    alice = Utilisateur()
    q = generer_premier(inf,sup)
    g = randint(2,q-1)
    id = 0
    nb_repetitions = 100

    (s,gs) = generer_cle(q,g)
    alice.certificats[id]=(s,gs)

    bob = Proprietaire(g,q, id, nb_repetitions)

    authentification(alice,bob)
    protocole_defectueux(alice,bob)
    test_protocole(alice,bob)

k = 64 ## Nombre de bits utilisés pour la clé
main(k)
