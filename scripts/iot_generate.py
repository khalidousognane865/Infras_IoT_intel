import json 
import time
import random
from datetime import datetime
from random import choice
from kafka import KafkaProducer


#Configuration kafka
KAFKA_TOPIC="iot_sensor_data"
KAFKA_BOOTSTRAP_SERVERS=['localhost:9092'] #adresse du broker kafka Docker
#Configuration du simulateur
SENSOR_ID_1="sensor_alpha_01"  #identifiantr du capteur 1
SENSOR_ID_2="sensor_alpha_02"  #identifiant du capteur 2
LOCATION="Champs_zone_A"  # ou se trouve le capteur
INTERVAL= 3 # l'interval en s entre deux envois

#Initialisation du producteur Kafka
#value_serializer : transforme automatiquement nos dos dictionnaires Python en JSON binaire
producer=KafkaProducer(
    bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

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

    #On choisit aléatoirement un des deux capteurs 
    sensor_id=random.choice([SENSOR_ID_1,SENSOR_ID_2])
    #On crée la structure de la donnée
    data={
        "sensor_id":sensor_id,
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

    #Simuler une panne rare (1 chance sur 10) pour tester le futur monitoring
    if random.randint(1,10)==1:
        data["metrics"]["temperature"]=999.9 # valeurs aberante
        data["status"]= "ERROR"
    return data
    
def main():
    print(f"---Démarrage des capteurs vers Kafka {KAFKA_BOOTSTRAP_SERVERS}---")
    print("Appuyer sur CTRL+C pour arréter.")        
    try:
        while True:
            #Génération des données
            record=generateur_sensor_data()
            #Envoi de la donnée à Kafka
            #On envoie la donnée dans le "tuyau" (topic) 
            producer.send(KAFKA_TOPIC, value=record)

            #On force l'envoi immédiat pourt etre sur que ce n'est pas bloqué en mémoire tampon
            
            #Conversion en json (sérialisation)
            json_record=json.dumps(record)
            producer.flush()
            #On affiche pour l'instant ,plus tard on l'enverra à Kafka
            print(f"✅ Donnée envoyée à Kafka [{record['sensor_id']}]: {record['metrics']['temperature']}°C")

            #pause
            time.sleep(INTERVAL)
    except KeyboardInterrupt:
        print("\n --- Arret du simulateur---")
        producer.close()


if __name__== "__main__":
    main()

    