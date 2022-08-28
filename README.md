[![forthebadge](https://forthebadge.com/images/badges/made-with-python.svg)](https://forthebadge.com) [![forthebadge](https://forthebadge.com/images/badges/built-with-love.svg)](https://forthebadge.com)

# Projet 12 : Développez une architecture back-end sécurisée en utilisant Django ORM

*** voir https://openclassrooms.com/fr/paths/518/projects/840/assignment ***


 ## Logiciels
 
 ```
Windows 11
Python 3.10.1
pytest - voir requirements.txt
```

## Initialisation du projet sous windows

### Windows 
```
git clone https://github.com/jsoques1/Epic_event.git

cd Epic_event
python -m venv env 
env\Scripts\activate

pip install -r requirements.txt
```

### Base de données

Les données pour l'accès à la base de données via django se trouve dans le fichier .env du git/

Créer la base de données avec SQL shell (psql) : 
```
CREATE DATABASE dbcrm;
\c dbcrm
\q
```

Migrer la base de données :

```
python manage.py migrate
```

Créer un super utilisateur admin/EpicEvent1 :

```
python manage.py createsuperuser
```

## Traces du CRM

Les traces du CRM sont généréés dans le fichiers traces.log


## Tests intégration / unitaires  

- Pour effectuer l'ensemble des tests unitaires et d'intégration, entrer la commande :

```
pytest
```

- Pour otbenir la couverture des tests dans le répertoire htmlcov, entrer la commande :

```
pytest --cov=. --cov-report html
```

## Documentation API Postman

La documentation est disponible sur le web : 

https://documenter.getpostman.com/view/20394225/VUqpsHZu


## ERD

Le diagramme est disponible dans le GIT sous forme PDF : 

ERD.drawio.pdf


## Rapports

Les captures d'écran des derniers rapports de tests sont disponibles dans le dossier 'reports'.

- [pytest] pytest_report.png

- [Couverture] coverage_report.png 

