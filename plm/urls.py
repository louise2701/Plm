"""
URL configuration for plm project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from order.views import unauthorized_view,home,login,confirm_order
urlpatterns = [
    path('admin/', admin.site.urls),
    path("order/", include("order.urls")),
    path('login/', login, name='login'),  # Page de connexion
    path('', home, name='home'),  # Page d'accueil (restreinte aux utilisateurs connectés)
]

 # Import de la vue

urlpatterns += [
    path('unauthorized/', unauthorized_view, name='unauthorized'),  # Nouvelle route
    path('confirm_order/', confirm_order, name='confirm_order'),
]