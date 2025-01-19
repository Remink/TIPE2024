

class Utilisateur:

    def __init__(self):

        #Variables permanentes
        self.cle = dict()


        #Variables liée à une authentification
        self.q = 0
        self.g = 0
        #Variables liées à une seule execution du protocole
        self.a = 0
        self.b=0

    def envoyer(self,proprietaire,objet,val):
        if(objet=="gs"):
            proprietaire.gs = val
        if(objet=="ga"):
            proprietaire.ga = val
        elif(objet=="c"):
            proprietaire.c = val

        
class Proprietaire:

    def __init__(self,g,q, id, nb_repetitions):
        
        #Variable permanentes
        self.g = g
        self.q = q
        self.id = id
        self.nb_repetitions = nb_repetitions
        
        #Variables liées à une authentification
        self.gs = 0
        #Variables liées à une seule execution du protocole
        self.ga = 0
        self.b = 0
        self.c = 0
    
    def envoyer(self,utilisateur,objet,val):
        if(objet=="g"):
            utilisateur.g = val
        if(objet=="q"):
            utilisateur.q = val
        elif(objet=="b"):
            utilisateur.b = val