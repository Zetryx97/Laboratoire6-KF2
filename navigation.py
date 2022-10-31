#Gabriel Lessard - Samy Tétrault - Guillaume Légaré
#Laboratoire 6 KF2
#Cette classe va permettre de calculer l'orientation et la position du robot lorsqu'il se déplace

# Note: Il y aura toujours une accélération verticale vers le bas de 1 g, pouvez-vous expliquer pourquoi?
# Reponsse : La terre a une force gravitationelle de 1g, ce qui attire tout vers le bas.

from time import sleep
import threading
from moteur import Moteur
from deplacement_robot import DéplacementRobot
from icm20948 import ICM20948

class Navigation:

    def __init__(self):
        self.moteur = Moteur()
        self.deplacement_robot = DéplacementRobot()
        self.imu = ICM20948()
        self.gx_biais = 0
        self.gy_biais = 0
        self.gz_biais = 0
        self.ax_biais = 0
        self.ay_biais = 0
        self.az_biais = 0
        self.tab_fenetre_gx = [0]
        self.tab_fenetre_gy = [0]
        self.tab_fenetre_gz = [0]
        self.tab_fenetre_ax = [0]
        self.tab_fenetre_ay = [0]
        self.tab_fenetre_az = [0]
        self.FENETRE = 10

    def orientation_position(self):
        #NB:
        #ax, ay,az = Une accélération en fraction de g selon un des axes
        #gx,gy,gz = Une vitesse de rotation en DPS selon un des axes 
        #DPS = Degré Par Seconde        
        
        while self.deplacement_robot.doit_lire_touche :
            sleep(0.05)
            ax, ay, az, gx, gy, gz = self.imu.read_accelerometer_gyro_data()
            match self.deplacement_robot.deplacer_robot:
            
                case "immobile":
                    self.gx_biais = gx
                    self.gy_biais = gy
                    self.gz_biais = gz
                    self.ax_biais = ax
                    self.ay_biais = ay
                    self.az_biais = az
                    self.ajout_val_tab_moyenne(self.tab_fenetre_gx,self.gx_biais)
                    self.ajout_val_tab_moyenne(self.tab_fenetre_gy,self.gy_biais)
                    self.ajout_val_tab_moyenne(self.tab_fenetre_gz,self.gz_biais)
                    self.ajout_val_tab_moyenne(self.tab_fenetre_ax,self.ax_biais)
                    self.ajout_val_tab_moyenne(self.tab_fenetre_ay,self.ay_biais)
                    self.ajout_val_tab_moyenne(self.tab_fenetre_az,self.az_biais)
                    break
                    
                case "translation":
                    ax_corriger = ax - self.calculer_moyenne_fenetrer(self.tab_fenetre_ax)
                    ax_corriger = ay - self.calculer_moyenne_fenetrer(self.tab_fenetre_ay)
                    az_corriger = az - self.calculer_moyenne_fenetrer(self.tab_fenetre_az)
                    break
                    
                case "rotation":
                    gx_corriger = gx - self.calculer_moyenne_fenetrer(self.tab_fenetre_gx)
                    gx_corriger = gy - self.calculer_moyenne_fenetrer(self.tab_fenetre_gy)
                    gz_corriger = gz - self.calculer_moyenne_fenetrer(self.tab_fenetre_gz)
                    break
                
                case _:
                    print('Erreur avec l\'état du robot.')


    def demarer_robot_navigation(self):
        th_orientation = threading.Thread(target=self.orientation_position)
        th_deplacement = threading.Thread(target=self.deplacement_robot.deplacer_robot)
        th_orientation.start()
        th_deplacement.start()
        while self.deplacement_robot.doit_lire_touche :
            sleep(1)

    def calculer_moyenne_fenetrer(self,tab_moyenne):
        moyenne = sum(tab_moyenne)/len(tab_moyenne)
        return (moyenne)
    
    def ajout_val_tab_moyenne(self,tab_fenetre,val):
        tab_fenetre.append(val)        
        if len(tab_fenetre)>self.FENETRE:
            del tab_fenetre[0]
        
if __name__ == "__main__":
    navigation = Navigation()
    navigation.demarer_robot_navigation()