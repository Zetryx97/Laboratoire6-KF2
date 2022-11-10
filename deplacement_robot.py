##Gabriel Lessard - Samy Tétrault - Guillaume Légaré
#Laboratoire 6 KF2
#Cette classe s'occupe de faire bouger le robot en fonction de la touche que l'utilisateur va appuyer.

import cv2
import numpy as np
from moteur import Moteur
from time import sleep
from moteur import Moteur

class DéplacementRobot:

    def __init__(self):
        self.moteur_Robot = Moteur()
        self.doit_lire_touche = True
        self.vitesse = 0.5

        
        self.img = np.zeros((512,512,3),np.uint8)
        self.etat_robot = 0 #immobile

    def deplacer_robot(self):
        print("----Menu pour robot----")
        print("Avancer-'w', Reculer-'s', Tourner sur place  à gauche-'a', Tourner sur place  à droite-'d', Freiner-'space'")
        cv2.imshow('Labo 1', self.img)
        while self.doit_lire_touche:
            key = cv2.waitKey(100)
            if key == ord('w'):
                self.etat_robot = 1 #translation
                self.moteur_Robot.avancer(self.vitesse)
            elif key == ord('s'):
                self.etat_robot = 1 #translation
                self.moteur_Robot.reculer(self.vitesse)
            elif key == ord('d'):
                self.etat_robot = 2 #rotation
                self.moteur_Robot.tourner_droite(self.vitesse)
            elif key == ord('a'):
                self.etat_robot = 2 #rotation
                self.moteur_Robot.tourner_gauche(self.vitesse)
            elif key == ord(' '):
                self.etat_robot = 0 #immobile
                self.moteur_Robot.freiner()
            elif key == ord('q'):
                self.etat_robot = 0 #immobile
                self.moteur_Robot.freiner()
                self.moteur_Robot.arreter()
                self.doit_lire_touche = False


if __name__ == "__main__":
    mouvement_robot = DéplacementRobot()

    mouvement_robot.deplacer_robot()