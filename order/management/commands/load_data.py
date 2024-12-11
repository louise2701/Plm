from django.core.management.base import BaseCommand
from django.db import transaction
from order.models import (
    Client, Order, Produit, Cheese, Wine,
    OrderDetail, Warehouse, Production,
    SousTraitant, Employe, Fournisseur, Planning,ProduitPreparation,OrderStockProduct,OrderHistoriqueVentes, ProduitOrderHistorique
)
import json

class Command(BaseCommand):
    help = 'Load data from JSON file'

    def handle(self, *args, **options):
        file_path = 'data.json'  # Assurez-vous que le chemin est correct

        with open(file_path) as f:
            data = json.load(f)

        self.load_data(Client, data.get('order_client', []))
        self.load_data(Produit, data.get('order_product', []))
        self.load_data(Cheese, data.get('order_cheese', []))
        self.load_data(Wine, data.get('order_wine', []))
        self.load_data(Order, data.get('order_order', []))
        self.load_data(OrderDetail, data.get('order_orderdetail', []))
        self.load_data(Warehouse, data.get('order_warehouse', []))
        self.load_data(Employe, data.get('order_employes', []))
        self.load_data(Fournisseur, data.get('order_fournisseurs', []))
        self.load_data(Planning, data.get('order_planning', []))
        self.load_data(ProduitPreparation, data.get('ProduitPreparation', []))
        self.load_data(Production, data.get('order_production', []))
        self.load_data(SousTraitant, data.get('order_sous_traitants', []))
        self.load_data(OrderStockProduct, data.get('order_stockProduct', []))
        self.load_data(OrderHistoriqueVentes, data.get('order_historiqueventes', []))
        self.load_data(ProduitOrderHistorique, data.get('order_produithistoriqueventes', []))

    @transaction.atomic
    def load_data(self, model, data_list):
        unique_fields = {
            'Client': 'email',
            'Order': 'order_id',
            'Produit': 'product_id',
            'Cheese': 'cheese_id',
            'Wine': 'wine_id',
            'OrderDetail': 'orderdetail_id',
            'Warehouse': 'warehouse_id',
            'Planning': 'planning_id',
            'Production': 'production_id',
            'SousTraitant': 'sous_traitant_id',
            'Employe': 'employe_id',
            'Fournisseur': 'fournisseur_id',
            'OrderStockProduct': 'stockproduct_id',
            'OrderHistoriqueVentes': 'id',
            'ProduitOrderHistorique': 'id',
        }

        model_name = model.__name__
        unique_field = unique_fields.get(model_name)

        if unique_field is None:
            self.stdout.write(self.style.ERROR(f'Unique field not defined for {model_name}'))
            return

        # Récupérer les entrées existantes
        existing_entries = model.objects.filter(**{f'{unique_field}__in': [entry.get(unique_field) for entry in data_list]})
        existing_ids = set(getattr(entry, unique_field) for entry in existing_entries)

        new_entries = []

        for entry in data_list:
            if entry.get(unique_field) not in existing_ids:
                # Gérer les relations de clé étrangère
                if model_name == 'Order':
                    email = entry.get('email_id')
                    if email:
                        try:
                            entry['email_id'] = Client.objects.get(email=email)
                        except Client.DoesNotExist:
                            self.stdout.write(self.style.ERROR(f'Client with email {email} does not exist'))
                            continue

                if model_name in ['Cheese', 'Wine']:
                    product_id = entry.get('product_id')
                    if product_id:
                        try:
                            entry['product_id'] = Produit.objects.get(product_id=product_id)
                        except Produit.DoesNotExist:
                            self.stdout.write(self.style.ERROR(f'Produit with ID {product_id} does not exist'))
                            continue

                if model_name == 'OrderDetail':
                    order_id = entry.get('order_id')
                    if order_id:
                        try:
                            entry['order'] = Order.objects.get(order_id=order_id)
                        except Order.DoesNotExist:
                            self.stdout.write(self.style.ERROR(f'Order with ID {order_id} does not exist'))
                            continue

                    product_id = entry.get('product_id')
                    if product_id:
                        try:
                            entry['product_id'] = Produit.objects.get(product_id=product_id)
                        except Produit.DoesNotExist:
                            self.stdout.write(self.style.ERROR(f'Produit with ID {product_id} does not exist'))
                            continue
                        
                if model_name == 'Planning':
                    employe_id = entry.get('employes_assignes')
                    if employe_id:
                        try:
                            entry['employes_assignes'] = Employe.objects.get(employe_id=employe_id)
                        except Order.DoesNotExist:
                            self.stdout.write(self.style.ERROR(f'Order with ID {employe_id} does not exist'))
                            continue
                    product_id = entry.get('produits_prepares')
                    if product_id:
                        try:
                            entry['produits_prepares'] = Produit.objects.get(product_id=product_id)
                        except Produit.DoesNotExist:
                            self.stdout.write(self.style.ERROR(f'Produit with ID {product_id} does not exist'))
                            continue
                        
                if model_name == 'ProduitPreparation':
                    planning_id = entry.get('planning_id')
                    if planning_id:
                        try:
                            entry['planning'] = Order.objects.get(planning_id=planning_id)
                        except Order.DoesNotExist:
                            self.stdout.write(self.style.ERROR(f'Order with ID {planning_id} does not exist'))
                            continue

                    product_id = entry.get('product_id')
                    if product_id:
                        try:
                            entry['produit'] = Produit.objects.get(product_id=product_id)
                        except Produit.DoesNotExist:
                            self.stdout.write(self.style.ERROR(f'Produit with ID {product_id} does not exist'))
                            continue
                        
                if model_name == 'Fournisseur':
                    produit_fournis_id = entry.get('produits_fournis')
                    if produit_fournis_id:
                        try:
                            entry['produits_fournis'] = Produit.objects.get(product_id=produit_fournis_id)
                        except Produit.DoesNotExist:
                            self.stdout.write(self.style.ERROR(f'Produit with ID {produit_fournis_id} does not exist'))
                            continue

                if model_name == 'Production':
                    planning_id = entry.get('planning_id')
                    if planning_id:
                        try:
                            entry['planning_id'] = Planning.objects.get(planning_id=planning_id)
                        except Planning.DoesNotExist:
                            self.stdout.write(self.style.ERROR(f'Planning with ID {planning_id} does not exist'))
                            continue

                    product_id = entry.get('product_id')
                    if product_id:
                        try:
                            entry['product_id'] = Produit.objects.get(product_id=product_id)
                        except Produit.DoesNotExist:
                            self.stdout.write(self.style.ERROR(f'Produit with ID {product_id} does not exist'))
                            continue


                if model_name == 'SousTraitant':
                    product_id = entry.get('produits_traites')
                    if product_id:
                        try:
                            entry['produits_traites'] = Produit.objects.get(product_id=product_id)
                        except Produit.DoesNotExist:
                            self.stdout.write(self.style.ERROR(f'Produit with ID {product_id} does not exist'))
                            continue
                
                if model_name == 'OrderStockProduct':                            
                        # Ici, on charge les relations entre entrepôts, produits, et stocks
                        product_id = entry.get('product_id')
                        if product_id:
                            try:
                                entry['product_id'] = Produit.objects.get(product_id=product_id).product_id
                            except Produit.DoesNotExist:
                                self.stdout.write(self.style.ERROR(f'Produit with ID {product_id} does not exist'))
                                continue

                        warehouse_id = entry.get('warehouse_id')
                        if warehouse_id:
                            try:
                                entry['warehouse_id'] = Warehouse.objects.get(warehouse_id=warehouse_id).warehouse_id
                            except Warehouse.DoesNotExist:
                                self.stdout.write(self.style.ERROR(f'Warehouse with ID {warehouse_id} does not exist'))
                                continue
                            
                if model_name == 'OrderHistoriqueVentes':
                    client_email = entry.get('client_email')
                    if client_email:
                        try:
                            # Récupérer le client par son email
                            entry['client_email'] = Client.objects.get(email=client_email)
                        except Client.DoesNotExist:
                            self.stdout.write(self.style.ERROR(f'Client with email {client_email} does not exist'))
                            continue
                
                
                if model_name == 'ProduitOrderHistorique':
                    historiqueventes_id = entry.get('historiqueventes_id')
                    if historiqueventes_id:
                        try:
                            # Récupérer le client par son email
                            entry['historiqueventes_id'] = OrderHistoriqueVentes.objects.get(id=historiqueventes_id)
                        except OrderHistoriqueVentes.DoesNotExist:
                            self.stdout.write(self.style.ERROR(f'Client with email {historiqueventes_id} does not exist'))
                            continue
                        
                    produits_id = entry.get('produits_id')
                    if produits_id:
                        try:
                            # Récupérer le client par son email
                            entry['produits_id'] = Produit.objects.get(product_id=produits_id)
                        except Produit.DoesNotExist:
                            self.stdout.write(self.style.ERROR(f'Client with email {produits_id} does not exist'))
                            continue


                new_entries.append(model(**entry))

        if new_entries:
            model.objects.bulk_create(new_entries)
            self.stdout.write(self.style.SUCCESS(f'Successfully loaded {len(new_entries)} entries for {model_name}'))
        else:
            self.stdout.write(self.style.SUCCESS(f'No new entries for {model_name}'))
