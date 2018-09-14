from django.urls import path
from . import views

urlpatterns = [
    path('', views.last_operations, name='budget_dashboard'),
    path('add_operation/', views.add_operation, name='budget_add_operation'),
    path('budgets/', views.view_budgets, name='budget_view_budgets'),
    path('add_budget/', views.add_budget, name='budget_add_budget'),
    path('categories/', views.view_categories, name='budget_view_categories'),
    # path('add_category/', views.add_category, name='budget_add_category'),
    path('overview/', views.overview, name='budget_overview'),
]
