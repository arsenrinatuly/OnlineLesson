from django.shortcuts import render, redirect

from .models import Product, Icecream, Course, Lesson, Author, Book
# Create your views here.
from .forms import ProductForm, IceCreamForm, CourseForm, LessonForm
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator
from django.forms import modelformset_factory, inlineformset_factory
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required, user_passes_test, permission_required
from django.http import HttpResponseForbidden
from django.core.exceptions import PermissionDenied
from django.db import transaction






def books_list(request):
    bk = Book.objects.select_related('author').defer('description', 'author__bio')
    bk2 = Book.objects.select_related('author').only('title', 'author__name')
    return render(request, 'book_list.html', {'bk': bk, 'bk2': bk2})




@login_required
@permission_required('auth.change_user', raise_exception=True)
def half_admin(request):
    return render(request, 'half_admin.html')

def home_view(request):
    if request.user.is_authenticated:
        print("Пользователь вошел"),
        print('name:', request.user.username),
        print('id', request.user.id),
    else:
        print('Незивестный зашел на сайт')
    return render(request, 'home.html')

@login_required
def user_info(request):
    user = request.user
    groups = user.groups.all()
    permissions = user.get_all_permissions()
    return render(request, 'user_info.html', {'user': user, 'groups': groups, 'permissions': permissions})


@user_passes_test(lambda user: user.is_staff, login_url='login')
def for_staff(request):
    return render(request, 'forstaff.html')



def add_course(request):
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('add_course')
    else:
        form = CourseForm()
    return render(request, 'courseform.html', {'form': form})

def course_modelformset(request):
    CourseModelFormset = modelformset_factory(Course, CourseForm, can_delete=True, extra=1)
    queryset = Course.objects.all()[:10]
    if request.method == 'POST':
        formset = CourseModelFormset(request.POST)
        if formset.is_valid():
            formset.save()
            return redirect('/')
    else:
        formset = CourseModelFormset(queryset=queryset)
    
    return render(request, 'courseformset.html', {'formset': formset})



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
            try:
                with transaction.atomic():
                    product = form.save(commit=False)  
                    print('Название:', form.cleaned_data['title'])
                    print('Категории', form.cleaned_data['categories'])
                    print('Измененные поля', form.changed_data)

                    raise Exception("Тест отката")

                    product.save()
                    form.save_m2m()
                    return redirect('/') 
            except Exception as e:
                print('Ошибка произошла в транзакции:', e)

    else:
        form = ProductForm()

    return render(request, 'product_form2.html', {'form': form})


def add_dz26(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            print("Все норм")
            return redirect('/')
    else:
        form = ProductForm()
    return render(request, 'product_add_dz26.html', {'form': form})


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
    ProductFormSet = modelformset_factory(Product, ProductForm, extra=3, can_delete=True)

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


def course_with_lessons_view(request):
    LessonFormSet = inlineformset_factory(
        Course, Lesson, form=LessonForm, extra=1, max_num=5, can_delete=True
    )
    if request.method == 'POST':
        course_form = CourseForm(request.POST)
        formset = LessonFormSet(request.POST)
        if course_form.is_valid() and formset.is_valid():
            course = course_form.save()
            formset.instance = course
            formset.save()
            return redirect('/')
    else:
        course_form = CourseForm
        formset = LessonFormSet

    return render(request, 'course_with_lessons.html',{'form': course_form, 'formset' : formset})

