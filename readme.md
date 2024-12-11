### Commande à lancer pour le projet : 
cd "repertoire ou se situe le projet"

python create_database.py
python manage.py makemigrations

python manage.py migrate

python manage.py load_data

python manage.py runserver

### Fonctionnalités : 

Se renseigner différence entre sous-traitant et fournisseur 

Fournisseurs : fonction recherche (pays, produit, nom, usine livrée), rajouter la colonne du matériel fournit + usine livrée), ajouter prix 

Entrepôts/usine : pour les fromages et les vins : fonction recherche (lieu, produit et nom) - ajouter la gestion des stocks dns les entrepôts + ajoout colonne emballage et sous traitant, ajouter prix 

Dans les usines : on fait le vin et les fromages : on fait appel à un sous traitant pour les emballages (fromages et bouteilles) 

Gestion des commandes : détail livraison à la grande distribution 

Distribution : transport des stocks (entreprises de transport) à inclure dans la base de données, fonction de recherche (produit, nom, lieu), ajouter colonne , ajouter gain 

Ajouter des statistiques et finances pour la distribution (comment ils nous ont acheté le fromage) 

 

Onglet finances/statistique qui reprend le coût du produit et son revenue (par gamme et par produit) 

Catalogue produit : références, ingrédients, poids et détails packaging..... (avec fonction de recherche) 
Gestion des tâches : assigner des tâches à des employés = pour synchroniser avec un planning les tâches de tout le monde
page employés : fonctions et contact
