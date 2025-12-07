from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('items/', views.items_list, name='items_list'),
    path('items/add/', views.add_item, name='add_item'),
    path('items/<int:item_id>/', views.item_detail, name='item_detail'),
    path('lost/', views.lost_items, name='lost_items'),
    path('found/', views.found_items, name='found_items'),
    path('found/unclaimed/', views.unclaimed_found, name='unclaimed_found'),
    path('reports/submit/', views.submit_report, name='submit_report'),
    path('claims/submit/', views.submit_claim, name='submit_claim'),
    path('students/', views.students_crud, name='students'),
    path('students/add/', views.add_student, name='add_student'),
    path('students/<int:student_id>/reports/', views.student_reports, name='student_reports'),
    # auth
    path('accounts/register/', views.register, name='register'),
    path('accounts/login/', views.login_view, name='login'),
    path('accounts/logout/', views.logout_view, name='logout'),
    path('profile/', views.profile, name='profile'),
]
