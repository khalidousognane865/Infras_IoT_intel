import json 
import time
import random
from datetime import datetime


#Configuration du simulateur
SENSOR_ID="sensor_alpha_01"  #identifiantr du capteur
LOCATION="Champs_zone_A"  # ou se trouve le capteur
INTERVAL= 3 # l'interval en s entre deux envois

def generateur_sensor_data():
    """
    Généré un dictionnaire représentant une lecture de captreur
    """
    #on simule d'abord:
    #  le température entre 25,0 et 37.0 degrés
    temperature=round(random.uniform(25.0,37.0),1)

    #Humidité  du sol entre 20% et 80%
    humidity_sol=round(random.uniform(20.0,80.0),1)
    
    #Humidité  de l'air entre 10% et 40%
    humidity_air=round(random.uniform(10.0,40.0),1)

    #Luminosité 
    luminosite=round(random.uniform(0,100000),1)

    #On crée la structure de la donnée 
    data={
        "sensor_id":SENSOR_ID,
        "location":LOCATION,
        "timestamp":datetime.now().isoformat(), #format standard ISO 8601
        "metrics":{
            "temperature":temperature,
            "humidite du Sol":humidity_sol,
            "humidite de l'air":humidity_air,
            "luminosité":luminosite
        },
        "status":"OK"
     }

    #Simuler une panne rare (1 chance sur 1) pour tester le futur monitoring
    if random.randint(1,20)==1:
        data["metrics"]["temperature"]=999.9 # valeurs aberante
        data["status"]= "ERROR"
    return data
    
def main():
    print(f"---Démarrage du capteur {SENSOR_ID}---")
    print("Appuyer sur CTRL+C pour arréter.")        
    try:
        while True:
            #Génération des données
            record=generateur_sensor_data()

            #Conversion en json (sérialisation)
            json_record=json.dumps(record)

            #On affiche pour l'instant ,plus tard on l'enverra à Kafka
            print(f"Envoie de la donnée:{json_record}")

            #pause
            time.sleep(INTERVAL)
    except KeyboardInterrupt:
        print("\n --- Arret du simulateur---")


if __name__== "__main__":
    main()

    