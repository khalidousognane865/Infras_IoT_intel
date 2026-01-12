#  Infrastructure IoT Intelligente : Pipeline de Streaming Temps Réel

##  Description du Projet
Ce projet est une implémentation complète d'un pipeline d'ingénierie des données (Data Engineering Pipeline) conçu pour traiter des flux de données IoT en temps réel.

L'objectif est de simuler une flotte de capteurs connectés, d'ingérer leurs données à haute fréquence (chaque 3 seconde), et de les traiter à la volée pour détecter des anomalies critiques (ex: surchauffe) avant le stockage durable .

##  Architecture Technique
![Architecture Diagram](./diagrams/Architecture.png)

Le projet repose sur une architecture conteneurisée via **Docker** :
* **Source** : Script Python simulant des capteurs IoT (Température, Humidité, Geolocation) générant des données au format JSON.
* **Ingestion (Message Broker)** : **Apache Kafka** & Zookeeper pour gérer le flux de données à haut débit et découpler les services.
* **Traitement (Stream Processing)** : **Apache Spark (Structured Streaming)** pour consommer les topics Kafka, parser les données JSON complexes et appliquer des règles métier en temps réel (filtrage, ajout d'alertes `is_critical`).
* **Stockage** : **MongoDB** pour la persistance des données enrichies.
* **Visualisation (À venir)** : Grafana.

##  Stack Technologique
* **Langage** : Python 3.9 (PySpark, Kafka-Python)
* **Containerisation** : Docker & Docker Compose
* **Big Data** : Apache Kafka 7.4, Apache Spark 3.5
* **Base de données** : MongoDB 6.0
* **OS** : Développement sous Windows

## Comment lancer le projet

### Pré-requis
* Docker Desktop installé et démarré .

### Installation
1.  Cloner le repo :
    ```bash
    git clone [https://github.com/TON_PSEUDO/iot-realtime-pipeline.git](https://github.com/khalidousognane865/Infras_IoT_intel.git)
    ```
2.  Lancer l'infrastructure DoCker :
    ```bash
    docker-compose up -d
    ```

### Utilisation
1.  **Lancer le générateur de données ** (Simulateur IoT) :
    ```bash
    python scripts/iot_generator.py
    ```
2.  **Lancer le Job Spark** (Traitement & Écriture vers MongoDB) :
    *Cette commande télécharge automatiquement les connecteurs Kafka et MongoDB compatibles.*
    ```bash
    docker exec -it spark-master /opt/spark/bin/spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.1,org.mongodb.spark:mongo-spark-connector_2.12:10.3.0 /app/scripts/spark_streaming.py
    ```

##  Résultats
Le pipeline traite les données et les injecte en temps réel dans MongoDB.
Voici un aperçu des données stockées avec le champ calculé `is_critical` :

![Résultats MongoDB](./diagrams/mongodb_resulte.jpg)

##  Prochaines étapes
* [x] Connecter le flux de sortie Spark vers MongoDB (Sink).
* [ ] Créer un dashboard de monitoring interactif avec Grafana.
* [ ] Déployer l'architecture sur le Cloud (AWS ou Azure).