##Implémentation d'une version du protocole d'identification de Schnoor sur le groupe Zq en supprimant la contrainte "g est un générateur d'ordre q de Zq"

from classes import *
import sympy as sp ##Bibliothèque pour générer des nombres premiers aléatoires
from random import randint
import hashlib as h
from time import *

## Complexités :
## Multiplication_mod(nb_bits)
## Add(nb_bits)
## Exponentiation modulaire avec exposant de k bits : C = k*Multiplication_mod(k)
## Envoyer(nb_bits)

def generer_premier(inf,sup):
    return sp.randprime(inf,sup)

def generer_cle(q, g): ## C = k*Multiplication_mod(k)
    s = randint(2,q-1)
    gs = pow(g,s,q) ## cle = g**s modulo q
    return (s,gs)


def engagement(alice,bob): ## C = k*Multiplication_mod(k) + Envoyer(k)
    (a,ga) = generer_cle(alice.q,alice.g)
    alice.a=a
    alice.envoyer(bob,"ga",ga)

def defi(alice,bob): ## C = Envoyer(k)
    b= randint(2,bob.q-1)
    bob.b=b
    bob.envoyer(alice,"b",b)
    return b

def reponse(alice,bob): ## C = Add(k) + Multiplication(k) + Envoyer(2k)
    s = alice.certificats[bob.id][1]
    c = (alice.a + alice.b*s)
    alice.envoyer(bob,"c",c)

def verification(bob): ## C = (2k+1)*Multiplication_mod(k)

    gc = pow(bob.g,bob.c,bob.q)
    t=(bob.ga*pow(bob.gs,bob.b,bob.q))%bob.q
    return t==gc ## t = ga*gs^b = g^a*g^bs = g^(a+bs) = g^c




def protocole_authentification_schnoor(alice,bob): ## C = (3k+1)*Multiplication_mod(k) + Multiplication(k) + 2*Envoyer(k) + Envoyer(2k)
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

def reponse2(alice,bob): ## Réponse et verification de la version usuelle du protocole
                        ## C = Multiplication_mod(k) + Add(k) Envoyer(k)
    s = alice.certificats[bob.id][0]
    c = (alice.a - alice.b*s)% alice.q
    alice.envoyer(bob,"c",c)

def verification2(alice,bob): ## C = 2k*Multiplication_mod(k)
    return bob.ga == (pow(bob.g,bob.c,bob.q)*pow(bob.gs,bob.b,bob.q))

def test_protocole(alice,bob): ## C = (3k+1)*Multiplication_mod(k) + Add(k) + 3*Envoyer(k)
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

def tentative_triche(alice,bob):
    print("Tentative de triche d'Alice, qu'on suppose ne pas connaître la clé privée.")
    nb_succes = 0
    nb_tentatives = 10_000
    for i in range(nb_tentatives):
        engagement(alice,bob)
        defi(alice,bob)
        ## Réponse d'Alice 

        ##Stratégie 1
        faux_s,faux_gs = generer_cle(alice.q,alice.g)
        faux_c = alice.a + alice.b*faux_s

        ##Stratégie 2
        ##faux_c = randint(2,(alice.q)^2)
        alice.envoyer(bob,"c",faux_c)

        if(verification(bob)):
            nb_succes+=1
    print("nombre de succès :")
    print(nb_succes)
    print("nombre de tentatives :")
    print(nb_tentatives)



def authentification(alice,bob):
    alice.envoyer(bob,"gs",alice.certificats[bob.id][0]) ##L'utilisateur envoie sa clé publique

    bob.envoyer(alice,"q",bob.q)
    bob.envoyer(alice,"g",bob.g)

    reussite = protocole_authentification_schnoor(alice,bob)

    pass


#Fonctions pour le protocole non interractif
def hacher(g,q,ga,date): ## C = Hash(3k +...)
    text= str(g) + str(q) + str(ga) + str(date)
    ##print(text)
    hash_code = h.md5(text.encode()).digest()
    number = int.from_bytes(hash_code,'big')
    return number

def generer_preuve(alice,bob,gs,g,q,s): ## C = k*Multiplication_mod(k) + Hash(3k+...) + Add(k) + Multiplication(k) + Envoyer(3k)

    (a,ga) = generer_cle(alice.q,alice.g)
    b = hacher(alice.g,alice.q,ga,0)
    c= a+b*s
    preuve = (ga,c)
    envoyer_preuve(alice,bob,preuve)

def envoyer_preuve(alice,bob,preuve): ## C = Hash(3k+...)
    bob.ga=preuve[0]
    bob.c = preuve[1]
    bob.b = hacher(bob.g,bob.q,bob.ga,0)

def verifier_preuve(bob):
    if(verification(bob)):
        print("bob accepte")
    else:
        print("bob refuse")
##Ctotale = k*Multiplication_mod(k) + Multiplication(k) + Add(k) + 2*Hash(3k+...) + Envoyer(3k)


def main(k):
    inf = 2**(k-1)
    sup = 2*inf -1
    alice = Utilisateur()
    q = generer_premier(inf,sup)
    g = randint(2,q-1)
    id = 0
    nb_repetitions = 100

    (s,gs) = generer_cle(q,g)
    alice.certificats[id]=(gs,s)

    bob = Proprietaire(g,q, id, nb_repetitions)

    authentification(alice,bob)
    ##protocole_defectueux(alice,bob)
    ##test_protocole(alice,bob)
    ##tentative_triche(alice,bob)


    print("g :")
    print(g)
    print("q : ")
    print(q)
    print("s :")
    print(s)
    print("gs :")
    print(gs)
    hacher(g,q,0,0)

    print("Protocole non interactif : ")
    generer_preuve(alice,bob,gs,g,q,s)
    verifier_preuve(bob)
    

k = 64 ## Nombre de bits utilisés pour la clé
main(k)
