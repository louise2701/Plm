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


def stock_management(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        action = request.POST.get('action')
        amount = int(request.POST.get('amount', 0))

        try:
            product = Produit.objects.get(product_id=product_id)

            if action == 'increase':
                product.stock += amount  # Augmenter le stock
            elif action == 'decrease':
                product.stock -= amount  # Réduire le stock
                if product.stock < 0:
                    product.stock = 0  # S'assurer que le stock ne devienne pas négatif

            product.save()  # Enregistrer les modifications
            messages.success(request, f'Stock updated for {product.product_id}.')

        except Produit.DoesNotExist:
            messages.error(request, 'Product not found.')

        return redirect('stock_management')  # Rediriger vers la même page après la modification

    # Charger les données JSON depuis le fichier
    with open('data.json') as f:
        data = json.load(f)

    products = []
    for product in Produit.objects.all():
        product_id = product.product_id
        stock = product.stock

        # Rechercher le nom du produit dans order_fiche_produit
        fiche_produit = next((item for item in data['order_fiche_produit'] if item['product_id'] == product_id), None)
        product_name = fiche_produit['nom'] if fiche_produit else f"Produit {product_id}"

        products.append({
            'product_id': product_id,
            'name': product_name,  # Utiliser le nom du produit ici
            'stock': stock,
        })

    return render(request, 'stock_management.html', {'products': products})
def fournisseurs(request):
    # Récupérer tous les fournisseurs
    fournisseurs_list = Fournisseur.objects.all()

    if request.method == 'POST':
        action = request.POST.get('action')
        fournisseur_id = request.POST.get('fournisseur_id')
        
        if action == 'delete':
            fournisseur = get_object_or_404(Fournisseur, fournisseur_id=fournisseur_id)
            fournisseur.delete()
            messages.success(request, 'Fournisseur supprimé avec succès.')

        elif action == 'add':
            # Ajout d'un nouveau fournisseur
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
            produits_fournis = request.POST.get('produits_fournis')  # Cette partie pourrait être plus complexe selon votre structure
            fournisseur = Fournisseur(nom=nom, contact=contact, adresse=adresse)
            fournisseur.save()
            messages.success(request, 'Fournisseur ajouté avec succès.')

        elif action == 'update':
            # Mise à jour d'un fournisseur
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


def warehouse_management(request):
    if request.method == 'POST':
        warehouse_id = request.POST.get('warehouse_id')
        new_address = request.POST.get('address')
        new_postal_code = request.POST.get('postal_code')

        # Mise à jour de la base de données (JSON ou DB)
        try:
            with open('data.json') as f:
                data = json.load(f)

            warehouse = next((item for item in data['order_warehouse'] if item['warehouse_id'] == int(warehouse_id)), None)
            if warehouse:
                warehouse['address'] = new_address
                warehouse['postal_code'] = new_postal_code
                
                # Sauvegarder les modifications dans le fichier
                with open('data.json', 'w') as f:
                    json.dump(data, f)
                    
                messages.success(request, 'Entrepôt mis à jour avec succès.')
            else:
                messages.error(request, 'Entrepôt non trouvé.')

        except Exception as e:
            messages.error(request, f'Erreur lors de la mise à jour: {e}')

        return redirect('warehouse_management')  # Rediriger vers la page après modification

    # Charger les données JSON depuis le fichier
    with open('data.json') as f:
        data = json.load(f)

    warehouses = []
    for warehouse in data['order_warehouse']:
        warehouses.append({
            'warehouse_id': warehouse['warehouse_id'],
            'address': warehouse['address'],
            'postal_code': warehouse['postal_code'],
            'zone': warehouse['zone'],
        })

    return render(request, 'warehouse_management.html', {'warehouses': warehouses})

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

def order_management(request):
    if request.method == 'POST':
        # Récupérer les données du formulaire
        order_id = request.POST.get('order_id')
        status = request.POST.get('status')

        # Mise à jour de la base de données (JSON ou DB)
        try:
            with open('data.json') as f:
                data = json.load(f)

            order = next((item for item in data['order_order'] if item['order_id'] == int(order_id)), None)
            if order:
                order['status'] = status
                
                # Sauvegarder les modifications dans le fichier
                with open('data.json', 'w') as f:
                    json.dump(data, f)
                    
                messages.success(request, 'Commande mise à jour avec succès.')
            else:
                messages.error(request, 'Commande non trouvée.')

        except Exception as e:
            messages.error(request, f'Erreur lors de la mise à jour: {e}')

        return redirect('order_management')  # Rediriger vers la page après modification

    # Charger les données JSON depuis le fichier
    with open('data.json') as f:
        data = json.load(f)

    # Créer une liste des commandes avec leurs détails
    orders = []
    for order in data['order_order']:
        order_id = order['order_id']
        details = [detail for detail in data['order_orderdetail'] if detail['order_id'] == order_id]

        # Ajouter les informations des produits
        products_info = []
        for detail in details:
            product_id = detail['product_id']
            product = next((item for item in data['order_fiche_produit'] if item['product_id'] == product_id), None)
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
            'status': order['status'],
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
