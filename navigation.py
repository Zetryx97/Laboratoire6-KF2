#Gabriel Lessard - Samy Tétrault - Guillaume Légaré
#Laboratoire 6 KF2
#Cette classe va permettre de calculer l'orientation et la position du robot lorsqu'il se déplace

from time import sleep
import threading
from moteur import Moteur
from deplacement_robot import DéplacementRobot
from icm20948 import ICM20948

class Navigation:

    def __init__(self):
        self.moteur = Moteur()
        self.deplacement_robot = DéplacementRobot()
        self.ÉTAT_IMMOBILE = "immobile"
        self.ÉTAT_ROTATION = "rotation"
        self.ÉTAT_TRANSLATION= "translation"
        self.imu = ICM20948()

    def orientation_position(self):
        #NB:
        #ax, ay,az = Une accélération en fraction de g selon un des axes
        #gx,gy,gz = Une vitesse de rotation en DPS selon un des axes 
        #DPS = Degré Par Seconde        
        
        while self.deplacement_robot.doit_lire_touche :
            sleep(0.05)
            ax, ay, az, gx, gy, gz = self.imu.read_accelerometer_gyro_data()
            match self.deplacement_robot.deplacer_robot:
                case "translation":
                    break
                
                case "immobile":
                    break
                    
                case "rotation":
                    break
                
                case _:
                    print('Erreur de etat robot')


    def demarer_robot_navigation(self):
        th_orientation = threading.Thread(target=self.orientation_position)
        th_deplacement = threading.Thread(target=self.deplacement_robot.deplacer_robot)
        th_orientation.start()
        th_deplacement.start()
        while self.deplacement_robot.doit_lire_touche :
            sleep(1)
        
if __name__ == "__main__":
    navigation = Navigation()
    navigation.demarer_robot_navigation()