from django.urls import path

from .views import (
    ProductDetailView,
    CourseDetailView,
    all_products,
    all_courses,
    purchase_product,
)

from .help_with_choice import *

app_name = 'catalog'

urlpatterns = [
    path('products/', all_products, name='all_products'),
    path('courses/', all_courses, name='all_courses'),
    path('products/<slug>/', ProductDetailView.as_view(), name='product'), 
    path('courses/<slug>/', CourseDetailView.as_view(), name='course'), 
    path('purchase-product/<slug>/', purchase_product ,name='purchase-product'),
    path('help-with-choice/', help_with_choice, name='help-with-choie'),
]