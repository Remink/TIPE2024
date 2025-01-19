##Implémentation d'une version du protocole d'identification de Schnoor sur le groupe Zq en supprimant la contrainte "g est un générateur d'ordre q de Zq"

from classes import *
import sympy as sp ##Bibliothèque pour générer des nombres premiers aléatoires
from random import randint
import hashlib as h
import time as time

## Complexités :
## Multiplication_mod(nb_bits) : O(k^2)
## Add(nb_bits) : O(k)
## Exponentiation modulaire avec exposant de k bits : C = k*Multiplication_mod(k) -> O(k^2)
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
    s = alice.cle[bob.id][1]
    c = (alice.a + alice.b*s)
    alice.envoyer(bob,"c",c)

def verification(bob): ## C = (2k+1)*Multiplication_mod(k)

    gc = pow(bob.g,bob.c,bob.q)
    t=(bob.ga*pow(bob.gs,bob.b,bob.q))%bob.q
    return t==gc 




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

def reponse2(alice,bob): ## Réponse et verification d'une autre version usuelle du protocole
                        ## C = Multiplication_mod(k) + Add(k) Envoyer(k)
    s = alice.cle[bob.id][1]
    c = (alice.a -alice.b*s)%(alice.q-1)
    alice.envoyer(bob,"c",c)

def verification2(alice,bob): ## C = 2k*Multiplication_mod(k)
    return bob.ga == (pow(bob.g,bob.c,bob.q)*pow(bob.gs,bob.b,bob.q))%bob.q

def test_protocole(alice,bob): ## C = (3k+1)*Multiplication_mod(k) + Add(k) + 3*Envoyer(k)
    engagement(alice,bob)
    defi(alice,bob)
    reponse2(alice,bob)
    if( verification2(alice,bob)):
        print("Bob accepte")
    else:
        print("Bob refuse")




def extracteur_connaissance(alice,bob):
    print("Extracteur de connaissance :")
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
    print("La clé  extraite est :" + str(int(s2)))
    print("la clé d'alice est : " + str(alice.cle[bob.id][1]))

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
    alice.envoyer(bob,"gs",alice.cle[bob.id][0]) ##L'utilisateur envoie sa clé publique

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
    #q=306325249809660913702757124705583996247
    g = randint(2,q-1)
    #g=239683428503087279526511909399209980359


    id = 0
    nb_repetitions = 100

    (s,gs) = generer_cle(q,g)


    alice.cle[id]=(gs,s)

    bob = Proprietaire(g,q, id, nb_repetitions)

    authentification(alice,bob)
    extracteur_connaissance(alice,bob)
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

    test_protocole(alice,bob)

 


k = 128 ## Nombre de bits utilisés pour la clé
main(k)


def test_rapidite_bruteforce(k):
    inf = 2**(k-1)
    sup = 2*inf -1
    q = sp.nextprime(inf)
    g = randint(2,q-1)
    s,gs = generer_cle(q,g)

    puissance_g = g
    t0 = time.time()
    i=1
    while puissance_g!=gs:
        puissance_g = puissance_g*g %q
        i+=1
    tf = time.time()
    calcule_ordre(g,q)
    print("temps, s, resultat du bruteforce")
    print(tf-t0, s,i)

def calcule_ordre(g,q):
    puissance_g = g
    i=1
    t0= time.time()
    while puissance_g!=1:
        puissance_g=puissance_g*g %q
        i+=1
    tf = time.time()
    print(pow(g,i,q))
    return(i, tf-t0)


def temps_calcul_ordre_maximal(k_max):
    tab_temps = []
    for k in range(2,k_max+1):
        print(k)
        trouve = False
        q = sp.nextprime(2**(k-1))
        g = randint(2**(k-1),q-1)
        while not(trouve):
            ordre,t = calcule_ordre(g,q)

            if ordre == q:
                trouve= True
                tab_temps.append(t)
            else:
                g= randint(2,q-1)
    print(tab_temps)

#q = generer_premier(2**(k-1),2**k)
#g = randint(2,q-1)
##print(calcule_ordre (g,q))
#print(q)
#print(g)
#print((q-1))
#print(sp.factorint(((q-1)//2)))
#print(sp.divisors((q-1)//2))


def calcul_ordre_rapide(g,q):
    ordres_possibles = sp.divisors((q-1)//2)
    ordres_possibles.append((q-1)//2)
    ordres_possibles.append(q-1)
    for i in ordres_possibles:
        if(pow(g,i,q)==1):
            return i
    return -1
##print(calcule_ordre(g,q))
#print(q)
#print(calcul_ordre_rapide(g,q))




