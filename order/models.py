from django.db import models
from django.db.models import UniqueConstraint


# Modèle pour les clients
class Client(models.Model):
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)  # Considérer l'utilisation d'un hachage pour les mots de passe
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=15)
    address = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=10)
    registered_credit_card = models.CharField(max_length=16)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.email})"


# Modèle pour les produits
class Produit(models.Model):
    product_id = models.AutoField(primary_key=True)
    #stock = models.IntegerField(default=0)  # Champ pour le stock
    

    def __str__(self):
        return f"Produit {self.product_id}"


# Modèle pour les fournisseurs
class Fournisseur(models.Model):
    fournisseur_id = models.AutoField(primary_key=True)
    nom = models.CharField(max_length=50)
    contact = models.JSONField()  # Contient nom_contact, telephone, email
    adresse = models.JSONField()  # Contient rue, ville, code_postal, pays
    materiel_fournit = models.CharField(max_length=255, null=True, blank=True)
    usine_livree = models.CharField(max_length=255, null=True, blank=True)
    prix = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return self.nom


# Modèle pour les sous-traitants
class SousTraitant(models.Model):
    sous_traitant_id = models.AutoField(primary_key=True)
    nom = models.CharField(max_length=50)
    contact = models.JSONField()
    adresse = models.JSONField()
    services_fournis = models.JSONField()
    produits_traites = models.ForeignKey(Produit, on_delete=models.CASCADE)

    def __str__(self):
        return self.nom


# Modèle pour les employés
class Employe(models.Model):
    employe_id = models.AutoField(primary_key=True)
    nom = models.CharField(max_length=50)
    poste = models.CharField(max_length=50)
    contact = models.JSONField()
    adresse = models.JSONField()
    date_embauche = models.DateField()
    competences = models.JSONField()
    mdp = models.CharField(max_length=128)  # Pour le mot de passe

    def __str__(self):
        return self.nom


# Modèle pour les commandes
class Order(models.Model):
    order_id = models.AutoField(primary_key=True)
    order_date = models.DateField()
    delivery_date = models.DateField()
    delivery_option = models.CharField(max_length=8, choices=[
        ('Express', 'Express'),
        ('Standard', 'Standard'),
    ])
    delivery_address = models.CharField(max_length=100)
    delivery_postal_code = models.CharField(max_length=10)
    status = models.CharField(max_length=10, choices=[
        ('Pending', 'Pending'),
        ('Confirmed', 'Confirmed'),
        ('In transit', 'In transit'),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled'),
    ])
    delivery_mode = models.CharField(max_length=10, choices=[
        ('Train', 'Train'),
        ('Airplane', 'Airplane'),
        ('Truck', 'Truck'),
        ('Ship', 'Ship'),
    ])
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    credit_card = models.CharField(max_length=16)
    email_id = models.ForeignKey(Client, on_delete=models.CASCADE)

    def __str__(self):
        return f"Order {self.order_id} by {self.email_id}"


# Modèle pour les détails de commande
class OrderDetail(models.Model):
    orderdetail_id = models.AutoField(primary_key=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product_id = models.ForeignKey(Produit, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    def __str__(self):
        return f"Detail {self.orderdetail_id} for Order {self.order_id}"


# Modèle pour les fromages
class Cheese(models.Model):
    cheese_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    price_per_kg = models.DecimalField(max_digits=10, decimal_places=2)
    origin = models.CharField(max_length=50)
    product_id = models.ForeignKey(Produit, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


# Modèle pour les vins
class Wine(models.Model):
    wine_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    price_per_bottle = models.DecimalField(max_digits=10, decimal_places=2)
    origin = models.CharField(max_length=50)
    product_id = models.ForeignKey(Produit, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Planning(models.Model):
    planning_id = models.AutoField(primary_key=True)
    date = models.DateField()
    shift = models.CharField(max_length=10, choices=[
        ('Matin', 'Matin'),
        ('Après-midi', 'Après-midi'),
        ('Nuit', 'Nuit')
    ])
    employes_assignes = models.ForeignKey(Employe, on_delete=models.CASCADE) # Relation M2M avec Employé
    produits_prepares = models.ForeignKey(Produit, on_delete=models.CASCADE)  # Relation M2M avec Produit
    commentaires = models.TextField()

    def __str__(self):
        return f'Planning {self.planning_id} - {self.date}'



class ProduitPreparation(models.Model):
    planning = models.ForeignKey('Planning', on_delete=models.CASCADE)
    produit = models.ForeignKey('Produit', on_delete=models.CASCADE)
    quantite = models.PositiveIntegerField()

    class Meta:
        constraints = [
            UniqueConstraint(fields=['planning', 'produit'], name='unique_planning_produit')
        ]  # Ensures that a product can only be prepared once per planning

    def __str__(self):
        return f'{self.quantite} of {self.produit} for Planning {self.planning}'


# Modèle pour la production
class Production(models.Model):
    production_id = models.AutoField(primary_key=True)
    planning_id = models.ForeignKey(Planning, on_delete=models.CASCADE)
    date_production = models.DateField()
    product_id = models.ForeignKey(Produit, on_delete=models.CASCADE)
    quantite_produite = models.IntegerField()
    temps_de_production = models.CharField(max_length=10)  # Format 'Xh'
    status = models.CharField(max_length=10, choices=[
        ('Terminé', 'Terminé'),
        ('En cours', 'En cours'),
        ('Annulé', 'Annulé')
    ])
    commentaires = models.TextField()

    def __str__(self):
        return f"Production {self.production_id} - {self.product_id} on {self.date_production}"


# Modèle pour l'entrepôt
class Warehouse(models.Model):
    warehouse_id = models.AutoField(primary_key=True)
    address = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=10)
    zone = models.CharField(max_length=50)

    def __str__(self):
        return f"Warehouse {self.warehouse_id} - {self.address}"
    
# Modèle pour la gestion des stocks des produits dans les entrepôts
class OrderStockProduct(models.Model):
    stockproduct_id = models.IntegerField(primary_key=True)
    product = models.ForeignKey(Produit, on_delete=models.CASCADE)
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE)
    stock = models.IntegerField()

    class Meta:
        unique_together = ('product', 'warehouse')  # Empêche les doublons pour le même produit dans le même entrepôt

    def __str__(self):
        return f"Stock_product {self.stockproduct_id} for Product {self.product.name} in Warehouse {self.warehouse.warehouse_id} - Stock: {self.stock}"

class OrderHistoriqueVentes(models.Model):
    id = models.AutoField(primary_key=True)
    date = models.DateField()
    client_email = models.ForeignKey(Client, on_delete=models.CASCADE)

    def __str__(self):
        return f"Historique vente {self.id} - {self.client_email.email} - {self.date}"

class ProduitOrderHistorique(models.Model):
    id = models.AutoField(primary_key=True)
    historiqueventes_id = models.ForeignKey(OrderHistoriqueVentes, on_delete=models.CASCADE)
    produits_id = models.ForeignKey(Produit, on_delete=models.CASCADE)
    quantite = models.IntegerField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Produit {self.produits_id.name} - Quantité: {self.quantite} - Montant: {self.amount}"
