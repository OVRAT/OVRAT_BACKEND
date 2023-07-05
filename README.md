# OVRAT_BACKEND
These are all backend modules for the OVRAT project structure



# Description de l'API





## Configuration et Installation

Ici il s'agit de comment installer et cofiguer le projet chez soit



* clonner de repositiry
* installez python dans votre machine
* installez *VIRTUELEN* via la commande 
---
    pip install virtualenvwraper-win
---
* créez un environement vituel via la commande
---
    mkvirtualen non_env
--- 
* ouvrez le repo avec vs code, ouvrez le terminal
* activez l'nvironnement virtuel avec la commande 
---
    workon nom_env 
---
* Installez les dépendences via la commande 
---
    pip install -r requirements.txt
---

* Tapez la commande suivante pour lancer le projet
---
    py mannage.py runserver
---
## API Reference

#### Get all items


```http
  POST /api/token/
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `username`      | `string` | **Required**.  |
| `password`      | `string` | **Required**.  |

ici il s'agit de la route qui va permettre d'avoir un token d'authentification


