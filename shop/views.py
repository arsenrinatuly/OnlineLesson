from django.shortcuts import render, redirect

from .models import Product, Icecream
# Create your views here.
from .forms import ProductForm, IceCreamForm
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator
from django.forms import modelformset_factory

def product_list(request):
    products = Product.objects.all()

    paginator = Paginator(products, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)


    return render(request, 'products_list.html', {'products': page_obj.object_list, 'page_obj' : page_obj})


def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            product = form.save(commit=False)  

            print('Название:', form.cleaned_data['title']),
            print('Категории', form.cleaned_data['categories']),
            print('Измененные поля', form.changed_data)
            product.save()
            form.save_m2m()
            return redirect('/') 
    else:
        form = ProductForm()

    return render(request, 'product_form2.html', {'form': form})

def edit_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect('/')
    else:
        form = ProductForm(instance=product)
    return render(request, 'product_form.html',{'form': form})

def products_formset_view(request):
    ProductFormSet = modelformset_factory(Product, ProductForm, extra=1, can_delete=True)

    if request.method == 'POST':
        formset = ProductFormSet(request.POST)
        if formset.is_valid():
            formset.save()
            return redirect('products_formset')  
    else:
        formset = ProductFormSet()
    return render(request, 'products_formset_view.html', {'formset': formset})


def icecream_form(request):
    if request.method == 'POST':
        form = IceCreamForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('icecream')
    else:
        form = IceCreamForm()
    return render(request, 'icecream_form.html', {'form': form})