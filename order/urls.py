from django.urls import path
from . import views
#from .views import home, produces, order_infos, confirm_order, order_confirmed, login, signin, account, order_history, logout,contact
from .views import home, produces,production, order_infos,planning,confirm_order, order_confirmed, login, signin,sous_traitants, account, order_history, logout, contact,fournisseurs, employees,stock_management,catalog_management,client_management,order_management,statistics_view,warehouse_management # Ajout de employees
urlpatterns = [
    path('home/', home, name='home'),

    path('produces/', produces, name='produces'),
   

    path('order_infos/', order_infos, name='order_infos'),

    path('confirm_order/', confirm_order, name='confirm_order'),
    path('order_confirmed/<int:order_id>/', order_confirmed, name='order_confirmed'),

    path('login/', login, name='login'),

    path('signin/', signin, name='signin'),

    path('account/', account, name='account'),
    path('account/order_history/<int:order_id>/', order_history, name='order_history'),

    path('logout/', logout, name='logout'),
    path('orders/', order_management, name='order_management'),
    path('contact/', contact, name='contact'),
    path('production/', production, name='production'),
    path('employees/', employees, name='employees'),
    path('planning/', planning, name='planning'),
    path('statistics_view/', statistics_view, name='statistics_view'),
    path('stock_management/', stock_management, name='stock_management'),
    path('client_management/', client_management, name='client_management'),
    path('catalog_management/', catalog_management, name='catalog_management'), 
    path('warehouse_management/', warehouse_management, name='warehouse_management'), 
    path('fournisseurs/', fournisseurs, name='fournisseurs'),
    path('sous_traitants/', sous_traitants, name='sous_traitants'),
   

]