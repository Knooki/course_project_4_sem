from django.shortcuts import render, redirect
from .models import LANGUAGES, Product, Course
from django.views.generic import DetailView



def index(request):
    return render(request, 'catalog/all_products.html')


def add_something(request):
    return render(request, 'catalog/add_something.html')


def all_products(request):
    products = Product.objects.all()
    return render(request, 'catalog/all_products.html', {'items': products})


def all_courses(request):
    courses = Course.objects.all()
    return render(request, 'catalog/all_products.html', {'items': courses})


class ProductDetailView(DetailView):
    model = Product
    template_name = "catalog/product.html"


class CourseDetailView(DetailView):
    model = Course
    template_name = "catalog/product.html"


def purchase_product(request, slug):
    if not request.user.is_authenticated:
        return redirect('/authentication/login'+'?message='+'Для покупки продуктов войдите')
    if Product.objects.get(slug=slug):
        product = Product.objects.get(slug=slug)
        context = {'item': product}
    elif Course.objects.get(slug=slug):
        course = Course.objects.get(slug=slug)
        context = {'item': course}
    return render(request, 'catalog/purchase_product.html', context)