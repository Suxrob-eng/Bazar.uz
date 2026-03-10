from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Product, Seller, ProductImage, Review, Complaint, Category
from django.db.models import Count, Q
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from captcha.fields import CaptchaField

class UserRegistrationForm(UserCreationForm):
    first_name = forms.CharField(
        max_length=30, 
        required=True, 
        widget=forms.TextInput(attrs={
            'class': 'form-control', 
            'placeholder': 'Ism'
        })
    )
    last_name = forms.CharField(
        max_length=30, 
        required=True, 
        widget=forms.TextInput(attrs={
            'class': 'form-control', 
            'placeholder': 'Familiya'
        })
    )
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control', 
            'placeholder': 'Username'
        })
    )
    phone = forms.CharField(
        max_length=20,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '+998 90 123 45 67'
        })
    )
    email = forms.EmailField(
        required=True, 
        widget=forms.EmailInput(attrs={
            'class': 'form-control', 
            'placeholder': 'Email'
        })
    )
    
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'phone', 'email', 'password1', 'password2']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control', 
            'placeholder': 'Parol'
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control', 
            'placeholder': 'Parolni takrorlang'
        })

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(
        required=True, 
        widget=forms.EmailInput(attrs={
            'class': 'form-control', 
            'placeholder': 'Email'
        })
    )
    first_name = forms.CharField(
        max_length=30, 
        required=True, 
        widget=forms.TextInput(attrs={
            'class': 'form-control', 
            'placeholder': 'Ism'
        })
    )
    last_name = forms.CharField(
        max_length=30, 
        required=True, 
        widget=forms.TextInput(attrs={
            'class': 'form-control', 
            'placeholder': 'Familiya'
        })
    )
    phone = forms.CharField(
        max_length=20,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '+998 90 123 45 67'
        })
    )
    captcha = CaptchaField(label="Kodni kiriting")
    
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'phone', 'password1', 'password2', 'captcha']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Username'})
        self.fields['password1'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Parol'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Parolni takrorlang'})


class EmailVerificationForm(forms.Form):
    code = forms.CharField(
        max_length=6,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '6 xonali kod',
            'style': 'text-align: center; font-size: 24px; letter-spacing: 5px;'
        })
    )


class PhoneVerificationForm(forms.Form):
    code = forms.CharField(
        max_length=6,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '6 xonali kod',
            'style': 'text-align: center; font-size: 24px; letter-spacing: 5px;'
        })
    )


class RegisterForm(forms.Form):
    username = forms.CharField()
    # captcha = ReCaptchaField()

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}))
    first_name = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ism'}))
    last_name = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Familiya'}))
    captcha = CaptchaField(label='Captcha')

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'captcha']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

class UserLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Parol'}))

class SellerForm(forms.ModelForm):
    class Meta:
        model = Seller
        fields = ['full_name', 'phone', 'additional_phone', 'city', 'region', 'avatar']
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'F.I.O.'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+998 90 123 45 67'}),
            'additional_phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+998 90 123 45 67 (ixtiyoriy)'}),
            'city': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Shahar/Tuman'}),
            'region': forms.Select(attrs={'class': 'form-select'}, choices=[
                ('', 'Viloyatni tanlang'), ('toshkent', 'Toshkent'), ('samarqand', 'Samarqand'),
                ('buxoro', 'Buxoro'), ('fergana', 'Farg\'ona'), ('andijan', 'Andijon'),
                ('namangan', 'Namangan'), ('khorezm', 'Xorazm'), ('kashkadarya', 'Qashqadaryo'),
                ('surkhandarya', 'Surxondaryo'), ('jizzakh', 'Jizzax'), ('sirdarya', 'Sirdaryo'),
                ('navoiy', 'Navoiy'), ('karakalpakstan', 'Qoraqalpog\'iston'),
            ]),
            'avatar': forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
        }

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['category', 'title', 'description', 'price', 'is_bargain', 'condition', 'location']
        widgets = {
            'category': forms.Select(attrs={'class': 'form-select', 'placeholder': 'Kategoriyani tanlang', 'choices': Category.objects.all()}),  
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Misol: iPhone 15'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Mahsulot haqida...'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '999.99'}),
            'is_bargain': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'condition': forms.Select(attrs={'class': 'form-select'}, choices=[
                ('new', 'Yangi'),
                ('like_new', 'Yangi deyarli'),
                ('used', 'Ishlatilgan')
            ]),
            'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Misol: Chilonzor, Toshkent'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].queryset = Category.objects.all()
        self.fields['category'].empty_label = "Kategoriyani tanlang"

    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price and price < 0:
            raise forms.ValidationError("Narx manfiy bo'lishi mumkin emas")
        return price

class ProductImageForm(forms.ModelForm):
    class Meta:
        model = ProductImage
        fields = ['image', 'is_main']
        widgets = {
            'image': forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
            'is_main': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.Select(attrs={'class': 'form-select'}, choices=[(i, f'{i} ★') for i in range(1, 6)]),
            'comment': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Fikringiz...'}),
        }

class ComplaintForm(forms.ModelForm):
    class Meta:
        model = Complaint
        fields = ['name', 'phone', 'reason', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'F.I.O.'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+998 90 123 45 67'}),
            'reason': forms.Select(attrs={'class': 'form-select'}, choices=[
                ('spam', 'Spam'), ('fraud', 'Firibgarlik'), ('fake', 'Soxta mahsulot'),
                ('offensive', 'Haqorat'), ('other', 'Boshqa')
            ]),
            'message': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Shikoyat matni...'}),
        }

class OrderForm(forms.Form):
    full_name = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'F.I.O.'}))
    phone = forms.CharField(max_length=20, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+998 90 123 45 67'}))
    email = forms.EmailField(required=False, widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email (ixtiyoriy)'}))
    city = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Shahar'}))
    address = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'To\'liq manzil'}))
    comment = forms.CharField(required=False, widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Buyurtmaga izoh (ixtiyoriy)'}))

class ProductFilterForm(forms.Form):
    q = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Qidirish...'}))
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        required=False,
        empty_label="Barcha kategoriyalar",
        widget=forms.Select(attrs={'class': 'form-select'})
    )  
    condition = forms.ChoiceField(
        choices=[('', 'Barchasi'), ('new', 'Yangi'), ('like_new', 'Yangi deyarli'), ('used', 'Ishlatilgan')],
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    min_price = forms.DecimalField(
        required=False,
        min_value=0,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Min narx'})
    )
    max_price = forms.DecimalField(
        required=False,
        min_value=0,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Max narx'})
    )
    sort = forms.ChoiceField(
        choices=[
            ('newest', 'Eng yangi'),
            ('price_asc', 'Narxi oshishi'),
            ('price_desc', 'Narxi kamayishi'),
            ('popular', 'Eng ommabop'),
        ],
        required=False,
        initial='newest',
        widget=forms.Select(attrs={'class': 'form-select'})
    )