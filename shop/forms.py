from django import forms    
from .models import Product, Icecream

class ProductForm(forms.ModelForm):
    password1 = forms.CharField(widget=forms.PasswordInput(), label="пароль")
    password2 = forms.CharField(widget=forms.PasswordInput(), label="повторите пароль")


    def clean_title(self):
        title = self.cleaned_data.get('title')
        if not title.strip():
            raise forms.ValidationError("Название не может содержать только пробелы")
        if len(title) < 5:
            raise forms.ValidationError("Название должно содержать не менее 5 символов")
        return title
    
    def clean(self):
        cleaned_data = super().clean()
        price = cleaned_data.get('price')
        description = cleaned_data.get('description')

            
        p1 = cleaned_data.get('password1')
        p2 = cleaned_data.get('password2')
        if p1 and p2 and p1!=p2:
            raise forms.ValidationError('Пароли не совпадают')


        if price > 10000 and not description:
            raise forms.ValidationError("Для продукта с ценой выше 10 тысяч, обязательно нужно добавить описание!")
        return cleaned_data



    class Meta:
        model = Product
        #fields = ['title', 'description'] первое дз
        fields = ['title', 'description', 'price', 'available', 'categories']
        labels = {
            'title' : 'Название товара',
            'description' : 'Описание',
            'price' : 'цена',
            'available': 'наличие',
            'categories' : 'категория',
        }

        help_texts = {
            'title' : 'Введите краткое название товара',
            'description' : 'Введите описание для вашего товара',
            'price': 'Введите цену для вашего товара',
            'available' : 'Укажите в наличии ли товара',
            'categories': 'Укажите в какой категории ваш товар',
        }

        widgets = {
            'title' : forms.TextInput(attrs={'placeholder' : 'Введите название'}),
            'description': forms.Textarea(attrs={'rows': 5, 'placeholder': 'Подробное описание'}),
            'price': forms.NumberInput(attrs={'placeholder': 'Введите цену товара'}),
            'available': forms.CheckboxInput(),
            'categories': forms.SelectMultiple(attrs={'size' : 6}),
        }

class IceCreamForm(forms.ModelForm):
    class Meta:
        model = Icecream
        fields = ['name', 'price', 'available']