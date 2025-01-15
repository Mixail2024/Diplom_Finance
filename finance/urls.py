from django.urls import path, re_path
from .views import (
    home, home_wlt,
    Create_wlt, Update_wlt,  Delete_wlt,
    calendar_view,
    add_income, update_income,
    add_income_type, Update_income_type,
    add_spending, update_spending,
    add_spending_type, Update_spending_type,
    delete_filtered_dt
)

urlpatterns = [
    path('create_wlt/', Create_wlt.as_view(), name = 'create_wlt'),
    path('home_wlt/<int:pk>/update_wlt/', Update_wlt.as_view(), name = 'update_wlt'),
    path('home_wlt/<int:pk>/delete_wlt/', Delete_wlt.as_view(), name = 'delete_wlt'),

#____________________________________________________________________________________________________INCOME

    path('home_wlt/<int:w_pk>/add_income/', add_income, name = 'add_income'),
    path('home_wlt/<int:w_pk>/update_income/<int:income_pk>/', update_income, name='update_income'),

    path('home_wlt/<int:w_pk>/add_income_type/', add_income_type, name='add_income_type'),
    path('home_wlt/<int:w_pk>/update_income_type/<int:pk>/', Update_income_type.as_view(), name='update_income_type'),


#____________________________________________________________________________________________________SPENDING

    path('home_wlt/<int:w_pk>/add_spending/', add_spending, name = 'add_spending'),
    path('home_wlt/<int:w_pk>/update_spending/<int:spending_pk>/', update_spending, name='update_spending'),

    path('home_wlt/<int:w_pk>/add_spending_type/', add_spending_type, name='add_spending_type'),
    path('home_wlt/<int:w_pk>/update_spending_type/<int:pk>/', Update_spending_type.as_view(), name='update_spending_type'),




#______________________________________________________________________________________________

    path('home_wlt/<int:w_pk>/delete filtered dt/', delete_filtered_dt, name = 'delete_filtered_dt'),
    path('home_wlt/<int:pk>/calendar/', calendar_view, name='calendar'),
    path('home_wlt/<int:w_pk>/', home_wlt, name = 'home_wlt'),

    path('', home, name = 'home'),
    ]
