from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Client, Order, OrderDetail, Produit, Cheese, Wine, Planning, Production,Employe,Fournisseur,SousTraitant
from django.utils import timezone
from django.db import transaction
import json
import datetime

def home(request):
    user_email = request.COOKIES.get('email', None)
    return render(request, 'home.html', {'user_email': user_email})

def produces(request):
    user_email = request.COOKIES.get('email', None)
    products_table = Produit.objects.all()

    products = []
    for product in products_table:
        product_id = product.product_id
        cheese = Cheese.objects.filter(product_id=product_id).first()
        wine = Wine.objects.filter(product_id=product_id).first()

        if cheese:
            products.append({'product_id': product_id, 'name': cheese.name, 'price': cheese.price_per_kg})
        elif wine:
            products.append({'product_id': product_id, 'name': wine.name, 'price': wine.price_per_bottle})

    return render(request, 'produces.html', {'user_email': user_email, 'products': products})

def order_infos(request):
    user_email = request.COOKIES.get('email', None)

    if user_email is not None:
        user_info = Client.objects.get(email=user_email)
        return render(request, 'order_infos.html', {'user_email': user_email, 'user_info': user_info})
    else:
        response = redirect('login')
        response.set_cookie('order_infos', True)
        return response
def employees(request):
    user_email = request.COOKIES.get('email', None)

    # Gérer la modification d'un employé
    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'add':  # Ajouter un nouvel employé
            new_employe = Employe(
                nom=request.POST.get('name'),
                poste=request.POST.get('position'),
                contact={
                    'telephone': request.POST.get('telephone'),
                    'email': request.POST.get('email')
                },
                date_embauche=request.POST.get('hire_date')
            )
            new_employe.save()
            messages.success(request, 'Employé ajouté avec succès.')

        elif action == 'edit':  # Modifier un employé existant
            employe_id = request.POST.get('employe_id')
            employe = Employe.objects.get(employe_id=employe_id)

            employe.nom = request.POST.get('name')
            employe.poste = request.POST.get('position')
            employe.contact['telephone'] = request.POST.get('telephone')
            employe.contact['email'] = request.POST.get('email')
            employe.date_embauche = request.POST.get('hire_date')
            employe.save()
            messages.success(request, 'Employé mis à jour avec succès.')

        elif action == 'delete':  # Supprimer un employé
            employe_id = request.POST.get('employe_id')
            employe = Employe.objects.get(employe_id=employe_id)
            employe.delete()
            messages.success(request, 'Employé supprimé avec succès.')

        return redirect('employees')  # Rediriger vers la page des employés

    employees_list = Employe.objects.all()  # Récupérer tous les employés

    return render(request, 'employees.html', {
        'user_email': user_email,
        'employees': employees_list
    })
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import SousTraitant, Produit  # Assurez-vous que les modèles sont importés
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import SousTraitant, Produit  # Assurez-vous que les modèles sont importés


from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import SousTraitant

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import SousTraitant  # Assurez-vous d'importer votre modèle SousTraitant

def sous_traitants(request):
    # Récupérer tous les sous-traitants
    sous_traitants_list = SousTraitant.objects.all()

    if request.method == 'POST':
        action = request.POST.get('action')
        sous_traitant_id = request.POST.get('sous_traitant_id')
        
        if action == 'delete':
            sous_traitant = get_object_or_404(SousTraitant, sous_traitant_id=sous_traitant_id)
            sous_traitant.delete()
            messages.success(request, 'Sous-traitant supprimé avec succès.')

        elif action == 'add':
            # Ajout d'un nouveau sous-traitant
            nom = request.POST.get('nom')
            contact = {
                "nom_contact": request.POST.get('nom_contact'),
                "telephone": request.POST.get('telephone'),
                "email": request.POST.get('email')
            }
            adresse = {
                "rue": request.POST.get('rue'),
                "ville": request.POST.get('ville'),
                "code_postal": request.POST.get('code_postal'),
                "pays": request.POST.get('pays')
            }
            services_fournis = request.POST.get('services_fournis')

            # Créer et sauvegarder le sous-traitant
            sous_traitant = SousTraitant(
                nom=nom,
                contact=contact,
                adresse=adresse,
                services_fournis=services_fournis
            )
            sous_traitant.save()
            messages.success(request, 'Sous-traitant ajouté avec succès.')

        elif action == 'update':
            # Mise à jour d'un sous-traitant
            sous_traitant = get_object_or_404(SousTraitant, sous_traitant_id=sous_traitant_id)
            sous_traitant.nom = request.POST.get('nom')
            sous_traitant.contact = {
                "nom_contact": request.POST.get('nom_contact'),
                "telephone": request.POST.get('telephone'),
                "email": request.POST.get('email')
            }
            sous_traitant.adresse = {
                "rue": request.POST.get('rue'),
                "ville": request.POST.get('ville'),
                "code_postal": request.POST.get('code_postal'),
                "pays": request.POST.get('pays')
            }
            sous_traitant.services_fournis = request.POST.get('services_fournis')
            sous_traitant.save()
            messages.success(request, 'Sous-traitant mis à jour avec succès.')

        return redirect('sous_traitants')  # Redirige vers la même page après modification

    return render(request, 'sous_traitants.html', {'sous_traitants': sous_traitants_list})

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Planning, Employe, Produit  # Assurez-vous que les modèles sont importés

def planning(request):
    # Récupérer tous les plannings
    planning_list = Planning.objects.all()

    if request.method == 'POST':
        action = request.POST.get('action')
        planning_id = request.POST.get('planning_id')

        if action == 'delete':
            planning = get_object_or_404(Planning, planning_id=planning_id)
            planning.delete()
            messages.success(request, 'Planning supprimé avec succès.')

        elif action == 'add':
            # Ajout d'un nouveau planning
            date = request.POST.get('date')
            shift = request.POST.get('shift')
            employes_assignes = request.POST.get('employes_assignes')
            produits_prepares = request.POST.get('produits_prepares')
            commentaires = request.POST.get('commentaires')

            planning = Planning(
                date=date,
                shift=shift,
                employes_assignes_id=employes_assignes,
                produits_prepares_id=produits_prepares,
                commentaires=commentaires
            )
            planning.save()
            messages.success(request, 'Planning ajouté avec succès.')

        elif action == 'update':
            # Mise à jour d'un planning
            planning = get_object_or_404(Planning, planning_id=planning_id)
            planning.date = request.POST.get('date')
            planning.shift = request.POST.get('shift')
            planning.employes_assignes_id = request.POST.get('employes_assignes')
            planning.produits_prepares_id = request.POST.get('produits_prepares')
            planning.commentaires = request.POST.get('commentaires')
            planning.save()
            messages.success(request, 'Planning mis à jour avec succès.')

        return redirect('planning')  # Redirige vers la même page après modification

    # Récupérer les employés et les produits pour les afficher dans les formulaires
    employes = Employe.objects.all()
    produits = Produit.objects.all()

    return render(request, 'planning.html', {
        'plannings': planning_list,
        'employes': employes,
        'produits': produits
    })
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Production, Planning, Produit  # Assurez-vous que les modèles sont importés

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Production, Planning, Produit
import json

from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Production, Produit
import json

from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Production, Produit, Planning
import json

def production(request):
    if request.method == 'POST':
        # Action de création ou de modification
        production_id = request.POST.get('production_id')
        action = request.POST.get('action')

        if action == 'delete':
            try:
                production = Production.objects.get(production_id=production_id)
                production.delete()
                messages.success(request, 'Production supprimée avec succès.')
            except Production.DoesNotExist:
                messages.error(request, 'Production non trouvée.')

        elif action == 'edit':
            try:
                production = Production.objects.get(production_id=production_id)
                production.date_production = request.POST.get('date_production')
                production.planning_id_id = request.POST.get('planning_id')
                production.product_id_id = request.POST.get('product_id')
                production.quantite_produite = request.POST.get('quantite_produite')
                production.temps_de_production = request.POST.get('temps_de_production')
                production.status = request.POST.get('status')
                production.commentaires = request.POST.get('commentaires')
                production.save()
                messages.success(request, 'Production mise à jour avec succès.')
            except Production.DoesNotExist:
                messages.error(request, 'Production non trouvée.')

        elif action == 'create':
            new_production = Production(
                date_production=request.POST.get('date_production'),
                planning_id_id=request.POST.get('planning_id'),
                product_id_id=request.POST.get('product_id'),
                quantite_produite=request.POST.get('quantite_produite'),
                temps_de_production=request.POST.get('temps_de_production'),
                status=request.POST.get('status'),
                commentaires=request.POST.get('commentaires')
            )
            new_production.save()
            messages.success(request, 'Nouvelle production créée avec succès.')

        return redirect('production_management')  # Rediriger vers la même page

    # Charger les données JSON depuis le fichier
    with open('data.json') as f:
        data = json.load(f)

    productions = []
    for production in Production.objects.all():
        product = production.product_id

        # Rechercher le nom du produit dans order_fiche_produit
        fiche_produit = next((item for item in data['order_fiche_produit'] if item['product_id'] == product.product_id), None)
        product_name = fiche_produit['nom'] if fiche_produit else f"Produit {product.product_id}"

        productions.append({
            'production': production,
            'product_name': product_name,  # Utiliser le nom du produit ici
        })

    # Récupérer les plannings et produits pour les sélections
    plannings = Planning.objects.all()
    produits = Produit.objects.all()

    return render(request, 'production.html', {'productions': productions, 'plannings': plannings, 'produits': produits})


from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Produit
import json

from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Produit
from .models import Warehouse
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Warehouse, Produit, Cheese, Wine, SousTraitant
import json

from django.shortcuts import render
from django.contrib import messages
from .models import Warehouse, Produit, Cheese, Wine, SousTraitant
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Warehouse, Produit, OrderStockProduct, Cheese, Wine, SousTraitant
from django.db.models import Q

from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Warehouse, Produit, OrderStockProduct
from django.db import transaction
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Warehouse, Produit, OrderStockProduct

from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Warehouse, Produit, OrderStockProduct, Cheese, Wine, SousTraitant
from django.db.models import Q
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Warehouse, Produit, OrderStockProduct, Cheese, Wine, SousTraitant
from django.db.models import Q

from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Warehouse, Produit, OrderStockProduct, Cheese, Wine, SousTraitant
from django.db.models import Q

def warehouse_management(request):
    # Collect search filters from GET request
    location_filter = request.GET.get('location', '')
    product_filter = request.GET.get('product', '')
    warehouse_filter = request.GET.get('warehouse', '')

    # Start by querying all warehouses
    warehouses = Warehouse.objects.all()

    # Filter warehouses by location if specified
    if location_filter:
        warehouses = warehouses.filter(address__icontains=location_filter)

    # Filter warehouses by warehouse_id if specified
    if warehouse_filter:
        warehouses = warehouses.filter(warehouse_id=warehouse_filter)

    # Prepare the list of warehouse data including related product details
    warehouse_data = []
    for warehouse in warehouses:
        if product_filter:
            cheeses = Cheese.objects.filter(name__icontains=product_filter)
            wines = Wine.objects.filter(name__icontains=product_filter)
        else:
            cheeses = Cheese.objects.all()
            wines = Wine.objects.all()

        for cheese in cheeses:
            stock_entry = OrderStockProduct.objects.filter(product=cheese.product_id, warehouse=warehouse).first()
            if stock_entry:
                subcontractor = SousTraitant.objects.filter(produits_traites=cheese.product_id).first()
                warehouse_data.append({
                    'warehouse_id': warehouse.warehouse_id,
                    'address': warehouse.address,
                    'postal_code': warehouse.postal_code,
                    'zone': warehouse.zone,
                    'product_name': cheese.name,
                    'product_id': cheese.product_id.product_id,  # Pass only the product ID
                    'product_type': 'Cheese',
                    'stock': stock_entry.stock,
                    'price': cheese.price_per_kg,
                    'subcontractor': subcontractor.nom if subcontractor else "None specified"
                })

        for wine in wines:
            stock_entry = OrderStockProduct.objects.filter(product=wine.product_id, warehouse=warehouse).first()
            if stock_entry:
                subcontractor = SousTraitant.objects.filter(produits_traites=wine.product_id).first()
                warehouse_data.append({
                    'warehouse_id': warehouse.warehouse_id,
                    'address': warehouse.address,
                    'postal_code': warehouse.postal_code,
                    'zone': warehouse.zone,
                    'product_name': wine.name,
                    'product_id': wine.product_id.product_id,  # Pass only the product ID
                    'product_type': 'Wine',
                    'stock': stock_entry.stock,
                    'price': wine.price_per_bottle,
                    'subcontractor': subcontractor.nom if subcontractor else "None specified"
                })

    # Handling the stock update form (POST request)
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        warehouse_id = request.POST.get('warehouse_id')
        action = request.POST.get('action')
        amount = int(request.POST.get('amount', 0))

        try:
            # Retrieve the product and warehouse using product_id and warehouse_id
            product = Produit.objects.get(product_id=product_id)
            warehouse = Warehouse.objects.get(warehouse_id=warehouse_id)

            # Get the OrderStockProduct entry for this product in the warehouse
            stock_entry = OrderStockProduct.objects.filter(product=product, warehouse=warehouse).first()

            if not stock_entry:
                # If no existing stock entry, create a new one with the specified stock amount
                stock_entry = OrderStockProduct(product=product, warehouse=warehouse, stock=0)

            # Update stock based on the action
            if action == 'increase':
                stock_entry.stock += amount  # Increase stock
            elif action == 'decrease':
                stock_entry.stock -= amount  # Decrease stock
                if stock_entry.stock < 0:
                    stock_entry.stock = 0  # Ensure stock doesn't go negative

            stock_entry.save()  # Save the updated stock entry
            messages.success(request, f"Stock updated for {product.product_id} in {warehouse.address}.")
        except (Produit.DoesNotExist, Warehouse.DoesNotExist):
            messages.error(request, 'Product or Warehouse not found.')

        return redirect('warehouse_management')  # Rediriger vers la même page après la modification

    products = Produit.objects.all()

    return render(request, 'warehouse_management.html', {'warehouse_data': warehouse_data, 'products': products})

def stock_management(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        action = request.POST.get('action')
        amount = int(request.POST.get('amount', 0))

        try:
            product = Produit.objects.get(product_id=product_id)

            if action == 'increase':
                product.stock += amount
            elif action == 'decrease':
                product.stock -= amount
                if product.stock < 0:
                    product.stock = 0

            product.save()
            messages.success(request, f'Stock updated for {product.product_id}.')

        except Produit.DoesNotExist:
            messages.error(request, 'Product not found.')

        return redirect('warehouse_management')  # Rediriger vers la page d'administration des entrepôts

    # Charger les données des produits
    products = Produit.objects.all()

    return render(request, 'warehouse_management.html', {'products': products})

from django.db.models import Q

def fournisseurs(request):
    # Récupérer tous les fournisseurs
    fournisseurs_list = Fournisseur.objects.all()

    # Vérifie si une recherche a été effectuée
    if request.GET.get('search'):
        search_query = request.GET.get('search')
        # Filtrage des fournisseurs selon les critères
        fournisseurs_list = fournisseurs_list.filter(
            Q(nom__icontains=search_query) |  # Recherche par nom
            Q(contact__icontains=search_query) |  # Recherche dans les informations de contact
            Q(adresse__icontains=search_query) |  # Recherche dans les adresses (pays, ville, etc.)
            Q(materiel_fournit__icontains=search_query) |  # Recherche par matériel fourni
            Q(usine_livree__icontains=search_query)  # Recherche par usine livrée
        )

    if request.method == 'POST':
        action = request.POST.get('action')
        fournisseur_id = request.POST.get('fournisseur_id')

        if action == 'delete':
            # Supprimer un fournisseur
            fournisseur = get_object_or_404(Fournisseur, fournisseur_id=fournisseur_id)
            fournisseur.delete()
            messages.success(request, 'Fournisseur supprimé avec succès.')

        elif action == 'add':
            # Ajouter un nouveau fournisseur
            nom = request.POST.get('nom')
            contact = {
                "nom_contact": request.POST.get('nom_contact'),
                "telephone": request.POST.get('telephone'),
                "email": request.POST.get('email')
            }
            adresse = {
                "rue": request.POST.get('rue'),
                "ville": request.POST.get('ville'),
                "code_postal": request.POST.get('code_postal'),
                "pays": request.POST.get('pays')
            }
            materiel_fournit = request.POST.get('materiel_fournit')
            usine_livree = request.POST.get('usine_livree')
            prix = request.POST.get('prix')

            fournisseur = Fournisseur(
                nom=nom, 
                contact=contact, 
                adresse=adresse, 
                materiel_fournit=materiel_fournit,
                usine_livree=usine_livree,
                prix=prix
            )
            fournisseur.save()
            messages.success(request, 'Fournisseur ajouté avec succès.')

        elif action == 'update':
            # Mettre à jour un fournisseur
            fournisseur = get_object_or_404(Fournisseur, fournisseur_id=fournisseur_id)
            fournisseur.nom = request.POST.get('nom')
            fournisseur.contact = {
                "nom_contact": request.POST.get('nom_contact'),
                "telephone": request.POST.get('telephone'),
                "email": request.POST.get('email')
            }
            fournisseur.adresse = {
                "rue": request.POST.get('rue'),
                "ville": request.POST.get('ville'),
                "code_postal": request.POST.get('code_postal'),
                "pays": request.POST.get('pays')
            }
            fournisseur.materiel_fournit = request.POST.get('materiel_fournit')
            fournisseur.usine_livree = request.POST.get('usine_livree')
            fournisseur.prix = request.POST.get('prix')
            fournisseur.save()
            messages.success(request, 'Fournisseur mis à jour avec succès.')

        return redirect('fournisseurs')  # Redirige vers la même page après modification

    return render(request, 'fournisseurs.html', {'fournisseurs': fournisseurs_list})





from django.shortcuts import render, redirect
from django.contrib import messages
import json
import os

def catalog_management(request):
    # Chemin vers le fichier JSON
    json_file_path = 'data.json'

    # Gérer la modification ou la suppression d'un produit
    if request.method == 'POST':
        action = request.POST.get('action')

        with open(json_file_path, 'r') as f:
            data = json.load(f)

        if action == 'add':  # Ajouter un nouveau produit
            new_product = {
                "product_id": request.POST.get('product_id'),
                "reference": request.POST.get('reference'),
                "nom": request.POST.get('name'),
                "ingredients": request.POST.get('ingredients').split(','),  # Convertir en liste
                "processus_de_fabrication": request.POST.get('manufacturing_process'),
                "specifications": {
                    "poids": request.POST.get('weight'),
                    "durée_d_affinage": request.POST.get('ripening_duration'),
                    "type_de_fromage": request.POST.get('cheese_type')
                },
                "version": {
                    "numero_version": 1,
                    "date_modification": "2024-01-01",
                    "modifications": "Produit ajouté."
                }
            }
            data['order_fiche_produit'].append(new_product)
            messages.success(request, 'Produit ajouté avec succès.')

        elif action == 'edit':  # Modifier un produit existant
            product_id = request.POST.get('product_id')
            for product in data['order_fiche_produit']:
                if product['product_id'] == product_id:
                    product['reference'] = request.POST.get('reference')
                    product['nom'] = request.POST.get('name')
                    product['ingredients'] = request.POST.get('ingredients').split(',')
                    product['processus_de_fabrication'] = request.POST.get('manufacturing_process')
                    product['specifications']['poids'] = request.POST.get('weight')
                    product['specifications']['durée_d_affinage'] = request.POST.get('ripening_duration')
                    product['specifications']['type_de_fromage'] = request.POST.get('cheese_type')
                    product['version']['date_modification'] = "2024-01-01"
                    product['version']['modifications'] = "Produit modifié."
                    messages.success(request, 'Produit mis à jour avec succès.')
                    break

        elif action == 'delete':  # Supprimer un produit
            product_id = request.POST.get('product_id')
            data['order_fiche_produit'] = [
                product for product in data['order_fiche_produit'] if product['product_id'] != product_id
            ]
            messages.success(request, 'Produit supprimé avec succès.')

        # Écrire les données mises à jour dans le fichier JSON
        with open(json_file_path, 'w') as f:
            json.dump(data, f, indent=4)

        return redirect('product_catalog')  # Rediriger vers la page de gestion des produits

    # Charger les produits existants depuis le fichier JSON
    with open(json_file_path, 'r') as f:
        data = json.load(f)

    products_list = data['order_fiche_produit']  # Récupérer tous les produits

    return render(request, 'catalog_management.html', {
        'products': products_list
    })


from django.shortcuts import render
from .models import Warehouse, Produit
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Warehouse, Produit, Cheese, Wine
from django.db.models import Q
from django.shortcuts import render
from .models import Warehouse, Cheese, Wine, SousTraitant, Produit
from django.shortcuts import render
from .models import Warehouse, Cheese, Wine, SousTraitant, Produit

from django.shortcuts import render
from .models import Warehouse, Cheese, Wine, SousTraitant, Produit

from django.shortcuts import render
from .models import Warehouse, Cheese, Wine, SousTraitant, Produit

from django.shortcuts import render
from .models import Warehouse, Produit, Cheese, Wine

from django.shortcuts import render
from .models import Warehouse, Produit, Cheese, Wine
from django.shortcuts import render
from .models import Warehouse, Produit, Cheese, Wine, SousTraitant


def client_management(request):
    if request.method == 'POST':
        # Récupérer les données du formulaire
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        phone_number = request.POST.get('phone_number')
        address = request.POST.get('address')
        postal_code = request.POST.get('postal_code')

        # Mise à jour de la base de données (JSON ou DB)
        try:
            with open('data.json') as f:
                data = json.load(f)

            client = next((item for item in data['order_client'] if item['email'] == email), None)
            if client:
                client['first_name'] = first_name
                client['last_name'] = last_name
                client['phone_number'] = phone_number
                client['address'] = address
                client['postal_code'] = postal_code
                
                # Sauvegarder les modifications dans le fichier
                with open('data.json', 'w') as f:
                    json.dump(data, f)
                    
                messages.success(request, 'Client mis à jour avec succès.')
            else:
                messages.error(request, 'Client non trouvé.')

        except Exception as e:
            messages.error(request, f'Erreur lors de la mise à jour: {e}')

        return redirect('client_management')  # Rediriger vers la page après modification

    # Charger les données JSON depuis le fichier
    with open('data.json') as f:
        data = json.load(f)

    clients = data['order_client']
    return render(request, 'client_management.html', {'clients': clients})


import json
from django.shortcuts import render, redirect
from django.contrib import messages

import json
from django.shortcuts import render, redirect
from django.contrib import messages

def order_management(request):
    if request.method == 'POST':
        # Retrieve form data
        order_id = request.POST.get('order_id')
        status = request.POST.get('status')
        delivery_mode = request.POST.get('delivery_mode')
        delivery_option = request.POST.get('delivery_option')

        # Update the database (JSON or DB)
        try:
            with open('data.json') as f:
                data = json.load(f)

            # Find the specific order
            order = next((item for item in data['order_order'] if item['order_id'] == int(order_id)), None)
            if order:
                # Update the fields
                order['status'] = status
                order['delivery_mode'] = delivery_mode
                order['delivery_option'] = delivery_option
                
                # Save the updated data to the file
                with open('data.json', 'w') as f:
                    json.dump(data, f, indent=4)
                
                messages.success(request, 'Order updated successfully.')
            else:
                messages.error(request, 'Order not found.')

        except Exception as e:
            messages.error(request, f'Error while updating order: {e}')

        return redirect('order_management')  # Redirect to the page after modification

    # Load the JSON data from the file
    try:
        with open('data.json') as f:
            data = json.load(f)
    except Exception as e:
        messages.error(request, f'Error loading data: {e}')
        return render(request, 'order_management.html', {'orders': []})

    # Create a list of orders with their details
    orders = []
    for order in data.get('order_order', []):
        order_id = order['order_id']
        details = [detail for detail in data.get('order_orderdetail', []) if detail['order_id'] == order_id]

        # Add product information
        products_info = []
        for detail in details:
            product_id = detail['product_id']
            product = next((item for item in data.get('order_fiche_produit', []) if item['product_id'] == product_id), None)
            if product:
                products_info.append({
                    'product_id': product_id,
                    'name': product['nom'],
                    'quantity': detail['quantity'],
                })

        orders.append({
            'order_id': order_id,
            'order_date': order['order_date'],
            'delivery_date': order['delivery_date'],
            'delivery_address': order['delivery_address'],
            'delivery_option': order['delivery_option'],
            'status': order['status'],
            'delivery_mode': order['delivery_mode'],
            'products': products_info,
        })

    return render(request, 'order_management.html', {'orders': orders})



def calculate_total_price(cartItems, delivery_option):
    total_price = 0

    for item in cartItems:
        quantity = cartItems[item]['quantity']
        product_price = cartItems[item]['price']
        total_price += product_price * quantity
    
    if delivery_option == 'Express':
        total_price += 5  # Adding delivery cost for express option

    return total_price

def confirm_order(request):
    if 'confirm' in request.POST:
        user_email = request.COOKIES.get('email', None)
        cartItems = json.loads(request.POST.get('cartItems'))

        order_date = timezone.now()
        delivery_option = request.POST.get('delivery_option')[0].upper() + request.POST.get('delivery_option')[1:]
        delivery_date = order_date + timezone.timedelta(days=1 if delivery_option == 'Express' else 3)
        delivery_address = request.POST.get('delivery_address')
        delivery_postal_code = request.POST.get('delivery_postal_code')
        status = 'Pending'
        total_price = calculate_total_price(cartItems, delivery_option)
        credit_card = request.POST.get('credit_card')

        with transaction.atomic():
            new_order = Order(
                order_date=order_date,
                delivery_date=delivery_date,
                delivery_option=delivery_option,
                delivery_address=delivery_address,
                delivery_postal_code=delivery_postal_code,
                status=status,
                total_price=total_price,
                credit_card=credit_card,
                email_id=Client.objects.get(email=user_email)  # ForeignKey relationship
            )
            new_order.save()

            for item in cartItems:
                product_id = cartItems[item]['product_id']
                quantity = cartItems[item]['quantity']
                new_order_detail = OrderDetail(order=new_order, product_id=Produit.objects.get(produit_id=product_id), quantity=quantity)  # ForeignKey relationship
                new_order_detail.save()
        
        request.session['order_date'] = int(order_date.timestamp())
        request.session['total_price'] = total_price
        request.session['delivery_option'] = delivery_option
        request.session['cartItems'] = cartItems

        return redirect('order_confirmed', new_order.order_id)

    return redirect('order_infos')

def order_confirmed(request, order_id):
    user_email = request.COOKIES.get('email', None)

    stored_order_date_timestamp = request.session.get('order_date')
    order_date = datetime.datetime.fromtimestamp(stored_order_date_timestamp) if stored_order_date_timestamp else None
    total_price = request.session.get('total_price')
    delivery_option = request.session.get('delivery_option')
    cartItems = request.session.get('cartItems')

    return render(request, 'order_confirmed.html', {
        'user_email': user_email,
        'order_id': order_id,
        'order_date': order_date,
        'total_price': total_price,
        'delivery_option': delivery_option,
        'cartItems': cartItems
    })

def order_history(request, order_id):
    user_email = request.COOKIES.get('email', None)
    order = Order.objects.get(order_id=order_id)
    order_details = OrderDetail.objects.filter(order=order)

    products = {}
    for order_detail in order_details:
        product_id = order_detail.product_id
        quantity = order_detail.quantity

        cheese = Cheese.objects.filter(product_id=product_id).first()
        wine = Wine.objects.filter(product_id=product_id).first()

        if cheese:
            products[product_id] = {'name': cheese.name, 'price': cheese.price_per_kg, 'quantity': quantity}
        elif wine:
            products[product_id] = {'name': wine.name, 'price': wine.price_per_bottle, 'quantity': quantity}

    return render(request, 'order_history.html', {
        'user_email': user_email,
        'order_id': order_id,
        'order_date': order.order_date,
        'total_price': order.total_price,
        'delivery_option': order.delivery_option,
        'cartItems': products
    })

def login(request):
    if 'login_submit' in request.POST:
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = Client.objects.filter(email=email, password=password).first()
        if not user:
            return render(request, 'login.html', {'error': 'Wrong email or password'})
        else:
            response = redirect('home')
            response.set_cookie('email', email)
            return response

    return render(request, 'login.html')

def signin(request):
    if 'signin_submit' in request.POST:
        email = request.POST.get('email')
        password = request.POST.get('password')
        phone_number = request.POST.get('phone_number')

        if Client.objects.filter(email=email).exists():
            return render(request, 'signin.html', {'error': 'Email already used'})
        else:
            new_user = Client(email=email, password=password, phone_number=phone_number)
            new_user.save()
            response = redirect('home')
            response.set_cookie('email', email)
            return response

    return render(request, 'signin.html')

def account(request):
    user_email = request.COOKIES.get('email', None)
    user_info = Client.objects.get(email=user_email)
    user_orders = Order.objects.filter(email_id=user_email)

    if 'modify_user_info' in request.POST:
        new_first_name = request.POST.get('first_name')
        new_last_name = request.POST.get('last_name')
        new_phone_number = request.POST.get('phone_number')
        new_address = request.POST.get('address')
        new_postal_code = request.POST.get('postal_code')
        new_registered_credit_card = request.POST.get('credit_card')

        user_info.first_name = new_first_name
        user_info.last_name = new_last_name
        user_info.phone_number = new_phone_number
        user_info.address = new_address
        user_info.postal_code = new_postal_code
        user_info.registered_credit_card = new_registered_credit_card
        user_info.save()

        return render(request, 'account.html', {
            'user_email': user_email, 
            'user_info': user_info, 
            'user_orders': user_orders, 
            'confirm_info': 'User informations modified!'
        })

    return render(request, 'account.html', {
        'user_email': user_email, 
        'user_info': user_info, 
        'user_orders': user_orders
    })
import matplotlib.pyplot as plt
from io import BytesIO
import base64
from django.shortcuts import render
from django.db.models import Sum, F, Count
from .models import OrderDetail, Cheese, Wine, Produit, OrderStockProduct

import matplotlib.pyplot as plt
from io import BytesIO
import base64
from django.shortcuts import render
from django.db.models import Sum, F
from .models import OrderDetail, Cheese, Wine, Produit, OrderStockProduct
import plotly.graph_objects as go
from django.shortcuts import render
from django.db.models import Sum, F
from .models import OrderDetail, Cheese, Wine, Produit, OrderStockProduct

import plotly.graph_objects as go
from django.shortcuts import render
from django.db.models import Sum, F
from .models import OrderDetail, Cheese, Wine, Produit, OrderStockProduct

import plotly.graph_objects as go
from django.shortcuts import render
from django.db.models import Sum, F
from .models import OrderDetail, Cheese, Wine, Produit, OrderStockProduct
import plotly.graph_objects as go
from django.shortcuts import render
from django.db.models import Sum, F
from .models import OrderDetail, Cheese, Wine, Produit, OrderStockProduct

import plotly.graph_objects as go
from django.shortcuts import render
from django.db.models import Sum, F
from .models import OrderDetail, Cheese, Wine, Produit, OrderStockProduct

import plotly.graph_objects as go
from django.shortcuts import render
from django.db.models import Sum, F
from .models import OrderDetail, Cheese, Wine, Produit, OrderStockProduct, Warehouse

import plotly.graph_objects as go
from django.shortcuts import render
from django.db.models import Sum, F
from .models import OrderDetail, Cheese, Wine, Produit, OrderStockProduct, Warehouse

import plotly.graph_objects as go
from django.shortcuts import render
from django.db.models import Sum, F
from .models import OrderDetail, Cheese, Wine, Produit, OrderStockProduct, Warehouse

import plotly.graph_objects as go
from django.shortcuts import render
from django.db.models import Sum, F
from .models import OrderDetail, Cheese, Wine, Produit, OrderStockProduct, Warehouse
import plotly.graph_objects as go
from django.shortcuts import render
from django.db.models import Sum, F
from .models import OrderDetail, Cheese, Wine, Produit, OrderStockProduct, Warehouse
import plotly.graph_objects as go
from django.shortcuts import render
from django.db.models import Sum, F
from .models import OrderDetail, Cheese, Wine, Produit, OrderStockProduct, Warehouse

import plotly.graph_objects as go
from django.shortcuts import render
from django.db.models import Sum, F
from .models import OrderDetail, Cheese, Wine, Produit, OrderStockProduct, Warehouse
import plotly.graph_objects as go
from django.shortcuts import render
from .models import OrderStockProduct, Cheese, Wine, Warehouse, Produit

import plotly.graph_objects as go
from django.shortcuts import render
from django.db.models import Sum, F
from .models import OrderDetail, Cheese, Wine, Produit, OrderStockProduct, Warehouse

from django.shortcuts import render
from django.db.models import Sum, F
from order.models import (
    OrderHistoriqueVentes, ProduitOrderHistorique, Produit, Client
)
import plotly.graph_objects as go
from django.db.models import Sum, F
from django.shortcuts import render
import plotly.graph_objects as go
from django.db.models import Sum, F
from django.shortcuts import render
import plotly.graph_objects as go
from .models import OrderHistoriqueVentes, ProduitOrderHistorique, Cheese, Wine, Produit
from django.db.models import Sum, F
from .models import ProduitOrderHistorique, Cheese, Wine
from django.db.models import Sum, F
from .models import OrderDetail, ProduitOrderHistorique, Cheese, Wine, Produit
import plotly.graph_objects as go

from django.db.models import Sum, F
from django.shortcuts import render
from .models import OrderDetail, ProduitOrderHistorique, Cheese, Wine, Produit
import plotly.graph_objs as go
from django.db.models import Sum, F
from django.shortcuts import render
from .models import ProduitOrderHistorique, Cheese, Wine, Produit
import plotly.graph_objs as go
from django.db.models import Sum, F
from django.shortcuts import render
import plotly.graph_objs as go
from .models import OrderHistoriqueVentes, ProduitOrderHistorique, Produit, Cheese, Wine
import plotly.express as px


from django.db.models import Sum, F
from django.shortcuts import render
import plotly.graph_objs as go
from .models import OrderHistoriqueVentes, ProduitOrderHistorique, Produit, Cheese, Wine
import plotly.express as px

from django.db.models import Sum, F
import plotly.graph_objs as go
from django.shortcuts import render
from .models import OrderHistoriqueVentes, ProduitOrderHistorique, Client
from django.db.models import Sum, F
import plotly.graph_objs as go
from django.shortcuts import render
from .models import OrderHistoriqueVentes, ProduitOrderHistorique, Client, Produit, Cheese, Wine

def statistics_view(request):
    # Chiffre d'affaires par produit (Fromages)
    cheese_revenue = ProduitOrderHistorique.objects.filter(produits_id__in=Cheese.objects.values('product_id'))
    cheese_revenue = cheese_revenue.values('produits_id').annotate(
        total_revenue=Sum(F('quantite') * F('produits_id__cheese__price_per_kg'))
    )
    
    # Chiffre d'affaire par produit (Vins)
    wine_revenue = ProduitOrderHistorique.objects.filter(produits_id__in=Wine.objects.values('product_id'))
    wine_revenue = wine_revenue.values('produits_id').annotate(
        total_revenue=Sum(F('quantite') * F('produits_id__wine__price_per_bottle'))
    )
    
    # Stocks disponibles par produit
    stock_data = OrderStockProduct.objects.all().values('product__product_id').annotate(total_stock=Sum('stock'))

    # Graphique pour le chiffre d'affaires
    product_names = []
    product_revenues = []

    # Pour Fromages (Récupérer le nom du produit via Cheese)
    for revenue in list(cheese_revenue):
        product_name = Cheese.objects.get(product_id=revenue['produits_id']).name  # Get the cheese name from Cheese table
        total_revenue = revenue['total_revenue']
        product_names.append(product_name)
        product_revenues.append(total_revenue)

    # Pour Vins (Récupérer le nom du produit via Wine)
    for revenue in list(wine_revenue):
        product_name = Wine.objects.get(product_id=revenue['produits_id']).name  # Get the wine name from Wine table
        total_revenue = revenue['total_revenue']
        product_names.append(product_name)
        product_revenues.append(total_revenue)

    # Graphique en barres pour le Chiffre d'Affaires
    fig_revenue = go.Figure(data=[go.Bar(x=product_names, y=product_revenues, name='Chiffre d\'affaires')])
    fig_revenue.update_layout(title='Chiffre d\'affaires par produit', xaxis_title='Produit', yaxis_title='Chiffre d\'affaires')

    # Graphique pour les stocks
    product_names_stock = []
    product_stocks = []

    # Pour chaque produit dans les stocks
    for stock in stock_data:
        # Récupérer le nom du produit depuis la table Cheese ou Wine
        try:
            product_name = Cheese.objects.get(product_id=stock['product__product_id']).name  # Cheese table
        except Cheese.DoesNotExist:
            try:
                product_name = Wine.objects.get(product_id=stock['product__product_id']).name  # Wine table
            except Wine.DoesNotExist:
                product_name = Produit.objects.get(product_id=stock['product__product_id']).__str__()  # Fallback to Produit table

        total_stock = stock['total_stock']
        product_names_stock.append(product_name)
        product_stocks.append(total_stock)

    # Graphique en barres pour le Stock disponible
    fig_stock = go.Figure(data=[go.Bar(x=product_names_stock, y=product_stocks, name='Stock')])
    fig_stock.update_layout(title='Stocks disponibles par produit', xaxis_title='Produit', yaxis_title='Stock')

    # Chiffre d'affaire au cours du temps (par date)
    revenue_by_date = ProduitOrderHistorique.objects.values('historiqueventes_id__date').annotate(
        total_revenue=Sum( F('amount'))
    ).order_by('historiqueventes_id__date')

    dates = [entry['historiqueventes_id__date'] for entry in revenue_by_date]
    revenues = [entry['total_revenue'] for entry in revenue_by_date]

    # Graphique linéaire pour le chiffre d'affaires au fil du temps
    fig_line = go.Figure(data=[go.Scatter(x=dates, y=revenues, mode='lines', name='Chiffre d\'affaires par Date')])
    fig_line.update_layout(
        title='Chiffre d\'affaires au fil du temps',
        xaxis_title='Date',
        yaxis_title='Chiffre d\'affaires'
    )

    # Graphique circulaire (camembert) pour la Répartition des Stocks
    fig_pie = go.Figure(data=[go.Pie(labels=product_names_stock, values=product_stocks, hole=0.3)])
    fig_pie.update_layout(title='Répartition des Stocks par Produit')
     # Répartition des stocks par entrepôt et produit
    stock_data_warehouse = OrderStockProduct.objects.all()

    warehouse_names = []
    product_names_warehouse = []
    stock_values_warehouse = []

    # Remplir les données pour le graphique de stocks par entrepôt et produit
    for stock in stock_data_warehouse:
        warehouse = Warehouse.objects.get(warehouse_id=stock.warehouse_id)
        product = Produit.objects.get(product_id=stock.product_id)

        # Ajouter l'entrepôt
        warehouse_names.append(warehouse.address)

        # Essayer de récupérer le nom du produit dans les tables Cheese, Wine, ou Produit
        try:
            # Essayer d'abord de récupérer le produit dans la table Cheese
            product_name = Cheese.objects.get(product_id=stock.product_id).name
        except Cheese.DoesNotExist:
            try:
                # Si le produit n'est pas trouvé dans Cheese, essayer dans la table Wine
                product_name = Wine.objects.get(product_id=stock.product_id).name
            except Wine.DoesNotExist:
                # Si le produit n'est trouvé ni dans Cheese ni dans Wine, le récupérer dans la table Produit
                product_name = Produit.objects.get(product_id=stock.product_id).__str__()

        product_names_warehouse.append(product_name)  # Nom du produit
        stock_values_warehouse.append(stock.stock)  # Valeur du stock pour ce produit dans l'entrepôt

    # Créer le graphique à barres pour la répartition des stocks par entrepôt et produit
    fig_warehouse_stock = go.Figure()

    # Obtenez les entrepôts uniques et produits uniques
    unique_warehouse_names = list(set(warehouse_names))  # Obtenir les entrepôts uniques
    unique_product_names = list(set(product_names_warehouse))  # Obtenir les produits uniques

    # Créer un dictionnaire pour stocker les valeurs des produits pour chaque entrepôt
    warehouse_product_stock = {warehouse: [] for warehouse in unique_warehouse_names}

    # Organiser les stocks par entrepôt et produit
    for warehouse in unique_warehouse_names:
        for product in unique_product_names:
            stock_value = sum(
                [stock_values_warehouse[i] for i in range(len(warehouse_names))
                 if warehouse_names[i] == warehouse and product_names_warehouse[i] == product]
            )
            warehouse_product_stock[warehouse].append(stock_value)

    # Ajouter chaque produit dans le graphique
    for i, product_name in enumerate(unique_product_names):
        fig_warehouse_stock.add_trace(go.Bar(
            x=unique_warehouse_names,
            y=[warehouse_product_stock[warehouse][i] for warehouse in unique_warehouse_names],
            name=product_name,
            hoverinfo='x+y+name',  # Afficher les informations au survol
        ))

    # Améliorer la lisibilité du graphique
    fig_warehouse_stock.update_layout(
        title='Répartition des Stocks par Entrepôt et Produit',
        xaxis_title='Entrepôt',
        yaxis_title='Stock',
        barmode='stack',  # Barres empilées pour afficher plusieurs produits par entrepôt
        xaxis_tickangle=45,  # Rotation des étiquettes de l'axe X pour les rendre plus lisibles
        plot_bgcolor='rgba(240, 240, 240, 0.9)',  # Couleur de fond pour le graphique
        margin=dict(l=40, r=40, t=40, b=100),  # Ajuster les marges pour une meilleure lisibilité
        height=500,  # Ajuster la hauteur du graphique pour le rendre plus lisible
    )

    # Ventes par client
    client_revenue = ProduitOrderHistorique.objects.values('historiqueventes_id__client_email').annotate(
        total_revenue=Sum(F('quantite') * F('amount'))
    )

    client_names = []
    client_revenues = []

    # Pour chaque client, récupérer les ventes
    for client in list(client_revenue):
        client_email = OrderHistoriqueVentes.objects.get(id=client['historiqueventes_id__client_email']).client_email.email  # Get the email of the client
        total_revenue = client['total_revenue']
        client_names.append(client_email)
        client_revenues.append(total_revenue)

    # Graphique des ventes par client (barres)
    fig_client_revenue = go.Figure(data=[go.Bar(x=client_names, y=client_revenues, name='Ventes par Client')])
    fig_client_revenue.update_layout(
        title='Ventes par Client',
        xaxis_title='Client',
        yaxis_title='Chiffre d\'Affaires'
    )

    # Quantité vendue par produit (Graphique circulaire)
    quantity_sold_by_product = ProduitOrderHistorique.objects.values('produits_id').annotate(
        total_quantity=Sum('quantite')
    )

    product_names_quantity = []
    product_quantities = []

    # Pour chaque produit, récupérer la quantité vendue
    for product in list(quantity_sold_by_product):
        # Récupérer le nom du produit depuis Cheese ou Wine en fonction de l'ID du produit
        try:
            # Essayer d'abord de récupérer le produit dans la table Cheese
            product_name = Cheese.objects.get(product_id=product['produits_id']).name
        except Cheese.DoesNotExist:
            try:
                # Si le produit n'est pas trouvé dans Cheese, essayer dans la table Wine
                product_name = Wine.objects.get(product_id=product['produits_id']).name
            except Wine.DoesNotExist:
                # Si le produit n'est trouvé ni dans Cheese ni dans Wine, le récupérer depuis la table Produit
                product_name = Produit.objects.get(product_id=product['produits_id']).__str__()

        total_quantity = product['total_quantity']
        product_names_quantity.append(product_name)
        product_quantities.append(total_quantity)

    # Graphique circulaire (camembert) pour la quantité vendue par produit
    fig_quantity_pie = go.Figure(data=[go.Pie(labels=product_names_quantity, values=product_quantities, hole=0.3)])
    fig_quantity_pie.update_layout(title='Quantité vendue par Produit')
    # Récupérer l'historique des ventes
    historique_sales = []

    # Récupérer toutes les ventes et leurs détails
    ventes = ProduitOrderHistorique.objects.select_related('historiqueventes_id', 'produits_id').all()

    for vente in ventes:
        # Récupérer les détails du produit et du client
        client_email = vente.historiqueventes_id.client_email.email
        quantite = vente.quantite
        total_price = vente.amount
        product_id = vente.produits_id.product_id

        # Récupérer le nom du produit à partir de Cheese, Wine, ou Produit
        try:
            # Vérifier si le produit est dans la table Cheese
            product_name = Cheese.objects.get(product_id=product_id).name
        except Cheese.DoesNotExist:
            try:
                # Vérifier si le produit est dans la table Wine
                product_name = Wine.objects.get(product_id=product_id).name
            except Wine.DoesNotExist:
                # Si le produit n'est pas trouvé dans Cheese ni Wine, le récupérer dans la table Produit
                product_name = Produit.objects.get(product_id=product_id).__str__()

        # Ajouter les données à l'historique des ventes
        sale_data = {
            'date': vente.historiqueventes_id.date,
            'client_email': client_email,
            'product_name': product_name,
            'quantite': quantite,
            'total_price': total_price
        }
        historique_sales.append(sale_data)


    # Convertir les graphiques Plotly en HTML
    revenue_graph = fig_revenue.to_html(full_html=False)
    stock_graph = fig_stock.to_html(full_html=False)
    line_graph = fig_line.to_html(full_html=False)
    pie_graph = fig_pie.to_html(full_html=False)
    
    warehouse_stock_graph = fig_warehouse_stock.to_html(full_html=False)
    client_revenue_graph = fig_client_revenue.to_html(full_html=False)
    quantity_pie_graph = fig_quantity_pie.to_html(full_html=False)

    # Passer les données et graphiques au template
    return render(request, 'statistics_view.html', {
        'historique_sales': historique_sales,
        'revenue_graph': revenue_graph,
        'stock_graph': stock_graph,
        'line_graph': line_graph,
        'pie_graph': pie_graph,
        'warehouse_stock_graph': warehouse_stock_graph,
        'client_revenue_graph': client_revenue_graph,
        'quantity_pie_graph': quantity_pie_graph,  # Ajouter le graphique de la quantité vendue
    })

def contact(request):
    user_email = request.COOKIES.get('email', None)

    if 'contact_submit' in request.POST:
        name = request.POST.get('name')
        email_contact = request.POST.get('email_contact')
        message = request.POST.get('message')

        # Assuming you have a Contact model defined
        new_message = Contact(name=name, email=email_contact, message=message)
        new_message.save()

        return render(request, 'contact.html', {'user_email': user_email, 'confirm': 'Message sent!'})

    return render(request, 'contact.html', {'user_email': user_email})

def logout(request):
    response = redirect('home')
    response.delete_cookie('email')
    return response
