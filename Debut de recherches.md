# TIPE2024

## Notions utiles :


#### Def : Système de preuve interactive : 

Machine abstraite composée d'un prouveur et d'un vérificateur. 
Le prouveur souhaite convaincre le vérificateur de la véracité d'une proposition, et possède une capacité de calcul illimité.
Le vérificateur a des ressources limités.
Le protocole peut être interactif ou non interactif.

	
Protocole interactif : Trois phases :
	-Engagement : Le prouveur envoie un premier message au vérificateur
	- Défis : Message du vérificateur au prouveur
	- Réponse : Le vérificateur répond au prouveur. Le prouveur peut alors décider d'accepter la preuve, de la refuser, ou de réitérer le processus jusqu'à ce qu'il soit satisfait.


Le Protocole doit être : 

- Complet : Si le protocole est suivit et que l'affirmation du prouveur est vrai, le vérificateur doit finir par accepter la preuve

- Robuste : Si la proposition est fausse, un prouveur malveillant ne peut pas convaincre un vérificateur honnête que l'affirmation est vraie avec une forte probabilité.



#### Def : Preuve à divulgation nulle de connaissance (ZKP) :

Système de preuve interactive devant vérifier une troisième propriété :
	
- Aucun apport de connaissance : Si le vérificateur est convaincu que la proposition est vraie, il n'apprend rien de plus que le fait que cette proposition soit vraie (Par exemple, si la proposition est "Le prouveur connait un certain secret", le vérificateur pourra affirmer avec une forte probabilité que le prouveur connait le secret, sans rien apprendre de plus sur ce secret).



## Exemple de ZKP :
On notera P le prouveur et V le vérificateur

###  3-Coloration de graphe : 

P veut montrer à V qu'il connait une 3-Coloration d'un certain graphe.

Protocole : 	
-> P permute les couleurs de son graphe de manière aléatoire, et chiffre chaque nœud du graphe, puis l'envoie à V

-> V demande à P de lui révéler la couleur de deux nœuds adjacents qu'il a choisit.

-> P envoie à V les clés de déchiffrement des deux nœuds. V peut alors vérifier que les nœuds ont deux couleurs différentes.


Comme tous problème NP complet  peut se traduire en problème de 3-coloration de graphe, on peut donc construire une ZKP pour tous problème NP complet


### Sudoku


### Protocoles Sigma : Ex : Protocole d'identification de Schnorr

Données publiques :
q un nombre premier
G : groupe cyclique d'ordre q (q éléments) engendré par un vecteur g d'ordre q
( $a^q$ = 1 et $\forall p< q,  a^p \neq 1$  )

v = $g^S$ où S est un entier entre 1 et n-1 connu uniquement du prouveur (Logarithme discret de v)



Protocole


|              | Prouveur                                                                | Vérificateur                                                                                                                                                                                |
| ------------ | ----------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Engagement   | a<- entier entre 1 et q-1 pris au hasard<br>R <- $g^a$ <br>Envoie R<br> | <br><br>Reçoit R = $g^a$ mais ne connais pas a                                                                                                                                              |
| Défi         | <br>Reçoit b                                                            | b <- entier entre 1 et q-1 pris au hasard<br>Envoie b                                                                                                                                       |
| Réponse      | c <- a + b$*$s<br>Envoie c                                              | <br>Reçoit c = a + b$*$s mais ne connait pas a et s                                                                                                                                         |
| Vérification |                                                                         | <br>T <- R$* v^b$ <br><br>Si T = $g^c$ , accepte ou recommence<br>Si T $\neq$ $g^c$, refuse<br><br>(Si tout s'est bien déroulé,<br> T =$g^c$$*$$v^b$ = $g^{a - bs}$$*$$g^{bs}$ = $g^a$ = R) |

-> Chiffrement de El Gamal utilise des clés de ce type
