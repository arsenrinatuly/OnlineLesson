from django.shortcuts import render, redirect

from .models import Product, Icecream, Course, Lesson, Author, Book, Photo, UploadFile
# Create your views here.
from .forms import ProductForm, IceCreamForm, CourseForm, LessonForm, ProductSearchForm, VoteForm, ImageForm, PhotoForm, UploadFileform
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator
from django.forms import modelformset_factory, inlineformset_factory
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required, user_passes_test, permission_required
from django.http import HttpResponseForbidden, FileResponse, Http404
from django.core.files.storage import FileSystemStorage
from django.core.exceptions import PermissionDenied
from django.db import transaction, IntegrityError
from django.conf import settings
from django.contrib import messages


import os
import time


def list_filess(request):
    files = UploadFile.objects.all()
    return render(request, "list_filess.html", {"files" : files})


def upload_file(request):
    if request.method == 'POST':
        form = UploadFileform(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('upload_file')
    else:
        form = UploadFileform()

    return render(request, 'upload_file.html', {'form': form})


def upload_low_level(request):
    context = {}
    if request.method == 'POST' and request.FILES.get("file"):
        myfile = request.FILES["file"]
        fs = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, "manual"))
        filename = fs.save(myfile.name, myfile)
        context["file_url"] = fs.url(filename)
    return render(request, "upload_manual.html", context)






def photo_list(request):
    photos = Photo.objects.all()
    return render(request, 'photo_list.html', {"photos" : photos})

def upload_photo(request):
    if request.method == 'POST':
        form = PhotoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("photo_list")
    else:
        form = PhotoForm
    return render(request, "upload_photo.html", {"form" : form})


def delete_photo(request, pk):
    photo = get_object_or_404(Photo, pk=pk)  
    if request.method == "POST":
        photo.delete()
        return redirect("photo_list")
    return redirect("photo_list")



def vote_view(request):
    result = None
    if request.method == 'POST':
        form = VoteForm(request.POST)
        if form.is_valid():
            choice = form.cleaned_data['choice']
            result = "Вы выбрали: Да" if choice == "yes" else "Вы выбрали: Нет"
    else:
        form = VoteForm()

    return render(request, 'vote.html', {'form' : form , 'result' : result})



def list_files(request):
    upload_dir = os.path.join(settings.BASE_DIR, "files")
    os.makedirs(upload_dir, exist_ok=True)

    files = []
    for entry in os.scandir(upload_dir):
        if entry.is_file() and not entry.name.endswith(".txt"):
            desc_file = entry.path + ".txt"
            description = ""
            if os.path.exists(desc_file):
                with open(desc_file, "r" , encoding="utf-8") as f:
                    description = f.read()
            
            files.append({
                "name" : entry.name,
                "url": f"/files/{entry.name}/",
                "description": description
            })
    return render(request, "list_files.html", {"files": files})




def upload_image(request):
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            img = request.FILES["img"]
            description = form.cleaned_data["description"]
            upload_dir = os.path.join(settings.BASE_DIR, "files")
            os.makedirs(upload_dir, exist_ok=True)
            ext = os.path.splitext(img.name)[1]
            filename = f"{int(time.time())}{ext}"
            filepath = os.path.join(upload_dir, filename)
            with open(filepath, "wb+") as destination:
                for chunk in img.chunks():
                    destination.write(chunk)

            desc_path = filepath + ".txt"
            with open(desc_path, "w", encoding="utf-8") as f:
                f.write(description)

            return redirect("list_files")
        
    else:
        form = ImageForm
    
    return render(request, "upload.html", {"form" : form})


def serve_file(request, filename):
    upload_dir = os.path.join(settings.BASE_DIR, "files")
    filepath = os.path.join(upload_dir, filename)
    if not os.path.exists(filepath):
        raise Http404("Файл не найден")
    return FileResponse(open(filepath, "rb"), as_attachment=False)



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
            messages.success(request, "Курс успешно добавлен, поздравляю!")
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




def productsearchform(request):
    products = []
    if request.method == 'POST':
        form = ProductSearchForm(request.POST)
        if form.is_valid():
            query = form.cleaned_data['query']
            if query:
                products = Product.objects.filter(title__icontains=query)
    else:
        form = ProductSearchForm()

    context = {'form' : form, 'products': products}
    return render(request, 'product_search.html', context)



def test_transaction(request):
    try:
        with transaction.atomic():
            product = Product.objects.create(title='Тестовый товар', price=10000)

            Product.objects.create(title='Дорогой товар', price=60000)

            raise IntegrityError("Отказ транзакции для примера")
    
    except IntegrityError as e:
        return HttpResponse(f"Транзакция отменена: {e}")
    
    return HttpResponse("Транзакция прошла успешно")