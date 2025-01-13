from django.urls import path, re_path
from .views import (
    home, home_wlt,
    Create_wlt, Update_wlt,  Delete_wlt,
    calendar_view,
    add_income, Update_income,
    add_income_type, Update_income_type, Delete_income_type,
    Add_spending)

urlpatterns = [
    path('create_wlt/', Create_wlt.as_view(), name = 'create_wlt'),
    path('home_wlt/update_wlt/<int:pk>/', Update_wlt.as_view(), name = 'update_wlt'),
    path('home_wlt/delete_wlt/<int:pk>/', Delete_wlt.as_view(), name = 'delete_wlt'),

    path('home_wlt/<int:w_pk>/add_income_type/', add_income_type, name='add_income_type'),

    path('home_wlt/<int:w_pk>/update_income_type/<int:pk>/', Update_income_type.as_view(), name='update_income_type'),
    path('delete_income_type/', Delete_income_type.as_view(), name='delete_income_type'),

    path('home_wlt/add_income/<int:w_pk>/', add_income, name = 'add_income'),
    path('home_wlt/update_income/<int:pk>/', Update_income.as_view(), name='update_income'),


    path('home_wlt/add_spending/<int:pk>/', Add_spending.as_view(), name = 'add_spending'),

    path('home_wlt/calendar/<int:pk>', calendar_view, name='calendar'),
    path('home_wlt/<int:w_pk>', home_wlt, name = 'home_wlt'),

    path('', home, name = 'home'),
    ]

# urlpatterns = [
#     path('create_wlt/', Create_wlt.as_view(), name='create_wlt'),
#     path('home_wlt/update_wlt/<int:pk>/', Update_wlt.as_view(), name='update_wlt'),
#     path('home_wlt/delete_wlt/<int:pk>/', Delete_wlt.as_view(), name='delete_wlt'),
#
#     path('home_wlt/add_income/add_income_type/<int:pk>/', add_income_type, name='add_income_type'),
#     path('home_wlt/update_income_type/<int:pk>/', Update_income_type.as_view(), name='update_income_type'),
#     path('home_wlt/add_income/<int:pk>/', add_income, name='add_income'),
#     path('home_wlt/add_spending/<int:pk>/', Add_spending.as_view(), name='add_spending'),
#     path('home_wlt/update_income/<int:pk>/', Update_income.as_view(), name='update_income'),
#     path('home_wlt/calendar/<int:pk>', calendar_view, name='calendar'),
#     path('home_wlt/<int:pk>', home_wlt, name='home_wlt'),
#     path('delete_income_type/', Delete_income_type.as_view(), name='delete_income_type'),
#     path('', home, name='home'),
# ]