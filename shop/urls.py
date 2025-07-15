from django.urls import path
from .views import (add_product, 
                    edit_product,
                    product_list, 
                    products_formset_view, 
                    icecream_form, add_dz26, add_course, course_modelformset, course_with_lessons_view, home_view)

urlpatterns = [
    # path('', home_view, name='home'),
    path('list/', product_list, name='product_list'),
    path('add/', add_product, name='add_product'),
    path('edit/<int:pk>/', edit_product, name='edit_product'),
    path('products/formset/', products_formset_view, name='products_formset'),
    path('icecream/', icecream_form, name='icecream'),
    path('add26/', add_dz26, name='add_dz26'),
    path('addcourse/', add_course, name='add_course'),
    path('coursemodel/', course_modelformset, name="course_modelformset"),
    path('coursewithlesson/', course_with_lessons_view, name='coursewithlesson'),
]
