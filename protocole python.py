##Implémentation du protocole d'identification de Schnoor sur le groupe Zq (Version décrite sur cette page : https://www.emanuelecivini.com/post/schnorr-id/)

import sympy as sp ##Bibliothèque pour générer des nombres premiers aléatoires
from random import randint

def generer_premier(inf,sup):
    return sp.randprime(inf,sup)

def generer_cle(q, g):
    s = randint(2,q-1)
    cle = pow(g,s,q) ## cle = g**s modulo q
    return (s,cle)


def engagement(q, g):
    (a,r) = generer_cle(q,g)
    return (a,r)

def defi(q):
    b= randint(2,q-1)
    return b

def reponse(q,a,b,s):
    c = (a + b*s)
    return c

def verification(q,g,r,b,c,cle):

    verif = pow(g,c,q)
    t=(r*pow(cle,b,q))%q
    return t==verif ## t = r*cle^b = g^a*g^bs = g^(a+bs) = g^c



def protocole(q,g): ## q est un nombre premier, q est un entier entre 2 et q-1, tout deux sont connu des deux participants
    (s,cle)= generer_cle(q,g)

    (a,r) = engagement(q,g)

    b = defi(q)
    c=reponse(q,a,b,s)

    test = verification(q,g,r,b,c,cle)
    print(test)





def main(k):

    inf = 2**(k-1)
    sup = 2*inf -1
    q = generer_premier(inf,sup)
    g = randint(2,q-1)

    protocole(q,g)

k = 256 ## Nombre de bits utilisés pour la clé
main(k)
