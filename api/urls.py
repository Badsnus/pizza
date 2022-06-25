from django.urls import path

from .views import show_pizzas_list, add_pizzas, add_order, index

urlpatterns = [
    path('show_pizzas_list', show_pizzas_list, name='show_pizzas_list'),
    path('add_pizzas', add_pizzas, name='add_pizzas'),
    path('add_order', add_order, name='add_order'),
    path('', index, name='index')
]
