# Airflow Lab2


## Introduction
Ce projet illustre l’orchestration de workflows complexes avec **Apache Airflow** pour un pipeline de machine learning et la gestion d’une API Flask pour le monitoring.

Deux DAGs principaux sont utilisés :

- **Airflow_Lab2** : orchestre le pipeline de machine learning et les notifications par e-mail.  
- **Airflow_Lab2_Flask** : gère le cycle de vie de l’API Flask pour vérifier l’état du pipeline.

Une vidéo tutorielle est disponible pour ce laboratoire : [Airflow Lab2 Tutorial Video](lien_vers_la_video)

---

## Prérequis
Avant de commencer, assurez-vous d’avoir :  

- Une compréhension de base d’**Apache Airflow**.  
- **Apache Airflow** installé et configuré.  
- Les packages Python nécessaires installés (notamment **Flask**).  
- Un compte Gmail avec un mot de passe d’application pour l’envoi d’e-mails.  

---

## Configuration des notifications par e-mail

### 1. Obtenir le mot de passe de l’application
Suivez les instructions fournies [ici](lien) pour générer votre mot de passe SMTP.

### 2. Ajouter les informations SMTP dans `airflow.cfg`
1. Localisez le fichier `airflow.cfg` dans votre installation Airflow.  
2. Ouvrez-le avec un éditeur de texte.  
3. Recherchez la section `[smtp]`.  
4. Modifiez les paramètres avec vos informations :

```ini
smtp_host = smtp.gmail.com
smtp_starttls = True
smtp_ssl = False
smtp_user = VOTRE_EMAIL@gmail.com
smtp_password = MOT_DE_PASSE_GENERÉ
smtp_port = 587
smtp_mail_from = VOTRE_EMAIL@gmail.com
smtp_timeout = 30
smtp_retry_limit = 5

Après cette configuration, Airflow pourra envoyer des notifications par e-mail.


# Cloner le dépôt
git clone https://github.com/VOTRE_UTILISATEUR/VOTRE_REPO.git
cd VOTRE_REPO

# Créer un environnement virtuel et installer les dépendances
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Initialiser Airflow
airflow db init

Usage
# Démarrer Airflow en mode standalone
airflow standalone

# Accéder à l'interface Airflow
# Ouvrir http://localhost:8080 dans votre navigateur

# Lancer manuellement le DAG
airflow dags trigger Airflow_Lab2

## Conclusion

Ce projet démontre :

- L’orchestration d’un pipeline complet de machine learning avec Airflow.
- L’intégration de notifications par e-mail pour le suivi des tâches.
- La gestion d’une API Flask pour un monitoring en temps réel du pipeline.

Grâce à cette structure, le workflow est scalable, maintenable, et offre une visibilité proactive sur les performances du pipeline.

