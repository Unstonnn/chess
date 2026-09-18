import pygame
from pygame.locals import *
#pour le rendre dispo de n'importe où
import os
pathname = os.path.dirname(__file__)


class GUIechec (object):

    def __init__(self):
        """
        Initialise une fenètre du jeu d'echec et l'affiche totalement vide.
        Cette classe ne contient aucun attribut publique.
        """

        #initialisation de pygame
        pygame.init()

        self.wPiece = 80
        self.wTapis = 9 * self.wPiece
        self.hTapis = 9 * self.wPiece
        self.hBandeau = 100
        self.rectBandeau = pygame.Rect(0, self.hTapis, self.wTapis, self.hBandeau)
        self.flipNum = False

        #on définit la fenêtre de base de notre jeu
        self.fenetre = pygame.display.set_mode((self.wTapis, self.hTapis + self.hBandeau))
        #un titre sur cette fenêtre
        pygame.display.set_caption("Echiquier")
        #Chargement et collage du fond
        #self.plateau = pygame.Surface((8 * self.wPiece, 8 * self.wPiece))

        #un dictionnaire pour les sprites
        self.sprites = {}

        #les type de pièces possibles
                # Roi: la lettre K (pour King)
                # Dame: la lettre Q (pour Queen)
                # Tour: la lettre R (pour Rook)
                # Fou: la lettre B (pour Bishop)
                # Cavalier: la lettre N (pour kNight)
                # Pion: aucune lettre ne lui est assignée normalement mais nous prendrons P.

        self.pieces = [c + p for c in ('B', 'W') for p in ('K', 'Q', 'R', 'B', 'N', 'P')]

        for p in self.pieces :
                self.sprites[p] = pygame.transform.scale(pygame.image.load(os.path.join(pathname, "Images", F"{p}.png")).convert_alpha(), (self.wPiece * 0.7, self.wPiece * 0.7))

        self.refresh([[0 for i in range(8)] for j in range(8)])


       #circle(surface, color, center, radius)

    def _creerCase(self, c, p, t):
        """
        Créé les cases pour le jeu :
        """

        clrCase = ['white', '#7084B6']

        case = pygame.Surface((self.wPiece, self.wPiece))
        caseRec = Rect(0, 0, self.wPiece, self.wPiece)

        case.fill(pygame.Color(clrCase[c]))

        if p in self.pieces:
            imgRec = self.sprites[p].get_rect()
            imgRec.center = caseRec.center
            case.blit(self.sprites[p], imgRec)

        if t == 1:
            pygame.draw.circle(case, 'red', caseRec.center, self.wPiece // 10)

        return case


    def refresh(self, g1, t = "", g2 = [[0 for i in range(8)] for j in range(8)]):
        """
        Cette méthode rafraichie l'affichage du jeu d'échec conformément à la grille g1 passée en argument.

        g1 est une grille : une liste de 8 listes de 8 éléments par exemple, ou n'importe quel autre objet indexable.

            - g1[0][0] est la case en haut à gauche
            - g1[7][7] est la case en bas à droite
            - g1[0][7] est la case en haut à droite

            Le contenu de la grille g1 définit le dessin de la case, les type de pièces possibles
            - Roi: la lettre K (pour King)
            - Dame: la lettre Q (pour Queen)
            - Tour: la lettre R (pour Rook)
            - Fou: la lettre B (pour Bishop)
            - Cavalier: la lettre N (pour kNight)
            - Pion: aucune lettre ne lui est assignée normalement mais nous prendrons P.

            Précédé d'une lettre B ou W pour la couleur de la pièce. Par exemple le roi blanc est représenté par le str 'WK'.
            N'importe quoi d'autre laissera la case vide.

        t est un texte à afficher à destination des joueurs.

        g2 est une grille : une liste de 8 listes de 8 éléments par exemple, ou n'importe quel autre objet indexable.
        g2 permet d'ajouter un marqueur sur une case. si g2 vaut 0 (int) rien ne se passe, si g2 vaut 1 (int), un point
        rouge marquera la case. Ce paramètre est optionnel, par défaut, g2 est une grille plein de de 0.

        """

        self.fenetre.fill(0x9a5e2a)

        for y in range(8):
            for x in range(8):
                self.fenetre.blit(self._creerCase((x + y)%2, g1[y][x], g2[y][x]), (self.wPiece // 2 + self.wPiece * x, self.wPiece // 2 + self.wPiece * y))

        police = pygame.font.SysFont("Arial Black.ttf", 36)
        recPos = pygame.Rect(self.wPiece // 2, 0, self.wPiece, self.wPiece // 2)

        for i in range(8):
            if not self.flipNum:
                j = i
            else:
                j = 7 - i
            txt = police.render(chr(65 + j), True, 'white')
            txtRect = txt.get_rect()
            recPos.top = 0
            txtRect.center = recPos.center
            self.fenetre.blit(txt, txtRect)
            recPos.bottom = self.hTapis
            txtRect.center = recPos.center
            self.fenetre.blit(txt, txtRect)

            recPos.left = recPos.right

        recPos = pygame.Rect(0, self.wPiece // 2, self.wPiece // 2, self.wPiece)
        for i in range(8):
            if not self.flipNum:
                j = 8 - i
            else:
                j = i + 1
            txt = police.render(str(j), True, 'white')
            txtRect = txt.get_rect()
            recPos.left = 0
            txtRect.center = recPos.center
            self.fenetre.blit(txt, txtRect)
            recPos.right = self.wTapis
            txtRect.center = recPos.center
            self.fenetre.blit(txt, txtRect)

            recPos.top = recPos.bottom

        #zone de texte
        #Une police
        police = pygame.font.SysFont("Arial Black",28)
        #un texte
        texte = police.render(t, True, pygame.Color("#FFFF00"))
        #pour centrer le texte
        rectTexte = texte.get_rect()
        rectTexte.center = self.rectBandeau.center
        self.fenetre.blit(texte, rectTexte)
        #Rafraîchissement de l'écran
        pygame.display.update()

    def messCentre(self, mess):
        """
        Cette méthode permet d'afficher un message plein écran.
        """
        police = pygame.font.Font(os.path.join(pathname, "led.ttf"),80)
        texte = police.render(mess, True, pygame.Color("black"))
        #pour centrer le texte
        rectTexte = texte.get_rect()
        rectTexte.center = self.fenetre.get_rect().center
        self.fenetre.blit(texte,rectTexte)
        #Rafraîchissement de l'écran
        pygame.display.update()

    def waitClick(self):
        """
        Cette méthode attend l'action d'un joueur. Elle gère trois type d'actions :
            - demande fermeture de la fenètre : fermeture propre de la fenètre pygame et fin du programme python.
            - click sur la fenetre : retourne  un tuple qui référence la case cliquée (x, y).
            - Quelques autres touches sont également gérées et retourne la lettre saisie.
        Une fois exécutée, on ne peut sortir de cette méthode que par l'une de ces trois actions.
        """
        continuer = True
        while continuer:
            #Limitation de vitesse de la boucle
            pygame.time.Clock().tick(30)

            for event in pygame.event.get():    #Attente des événements
                if event.type == QUIT:
                    continuer = False
                    pygame.quit()
                    exit()

                if event.type == MOUSEBUTTONDOWN:
                    if event.button == 1:   #Si clic gauche
                        if 0.5 * self.wPiece < event.pos[0] < self.wPiece * 8.5 and 0.5 * self.wPiece < event.pos[1] < self.wPiece * 8.5:
                            return ((event.pos[0] - self.wPiece // 2)//(self.wPiece), (event.pos[1] - self.wPiece // 2)//(self.wPiece))

                if event.type == KEYDOWN:
                    touches = {K_RIGHT : '_R', K_LEFT : '_L', K_UP : '_U', K_DOWN : '_D', K_RETURN : '_E', K_BACKSPACE : '_B', K_ESCAPE : '_S'}
                    touche = event.key
                    if touche in touches:
                        return touches[touche]
                    return event.unicode


if __name__ == "__main__":
    import time

    GUI = GUIechec()
    GUI.flipNum = True
    GUI.refresh([[0 for i in range(8)] for j in range(8)], "Les noirs devant")
    time.sleep(2)
    GUI.flipNum = False
    GUI.refresh([[0 for i in range(8)] for j in range(8)], "Les blancs devant")
    time.sleep(2)

    j = [['BR', 'BN', 'BB', 'BK', 'BQ', 'BB', 'BN', 'BR']] + [['BP' for i in range(8)]] + [[0 for i in range(8)] for j in range(4)] + [['WP' for i in range(8)]] + [['WR', 'WN', 'WB', 'WK', 'WQ', 'WB', 'WN', 'WR']]

    GUI.refresh(j, "A vous de jouer !!")
    time.sleep(2)

    #déplace un cavalier et un pion noirs
    j[0][1] = 0
    j[2][2] = 'BN'
    j[1][4] = 0
    j[2][4] = 'BP'
    j[6][3] = 0
    j[4][3] = 'WP'
    #liste des emplacements possibles pour ce cavalier
    target = [[0, 1, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 1, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0],
              [1, 0, 0, 0, 1, 0, 0, 0],
              [0, 1, 0, 1, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0]]

    GUI.refresh(j, "Emplacements jouables par le cavalier noir", target)

    while True :
        print(GUI.waitClick())

