from django.shortcuts import render, redirect, get_object_or_404
from django.shortcuts import get_object_or_404, redirect
from telegram import User
from .models import Product, Like
from django.core.paginator import Paginator
from django.db.models import Q, Count, Avg
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from django.forms import modelformset_factory
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse
from .models import Category
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from .models import EmailVerification, PhoneVerification
from .forms import UserRegistrationForm, EmailVerificationForm, PhoneVerificationForm
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from .models import EmailVerification
from .forms import UserRegistrationForm
import random
import random
import requests
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from .forms import UserRegistrationForm
from .models import PhoneVerification, EmailVerification
import random
import requests

def send_verification_email(recipient_email, code):
    """Tasdiqlash kodini email orqali yuborish"""
    subject = "Tasdiqlash kodi"
    message = f"Sizning tasdiqlash kodingiz: {code}"
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [recipient_email]
    
    send_mail(subject, message, from_email, recipient_list)


# 1-QADAM: Ro'yxatdan o'tish (barcha ma'lumotlar)
def register_step1(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            # Userni vaqtincha saqlash (aktiv emas)
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            
            # Ma'lumotlarni sessiyaga saqlash
            request.session['reg_user_id'] = user.id
            request.session['reg_phone'] = form.cleaned_data.get('phone')
            request.session['reg_email'] = form.cleaned_data.get('email')
            
            # TELEFONGA KOD YUBORISH
            phone = form.cleaned_data.get('phone')
            phone_code = ''.join([str(random.randint(0,9)) for _ in range(6)])
            
            PhoneVerification.objects.create(
                user=user,
                phone=phone,
                code=phone_code
            )
            
            # SMS yuborish (test uchun konsolga chiqaramiz)
            print(f"\n📱 TELEFONGA KOD: {phone} -> {phone_code}\n")
            
            # Haqiqiy SMS uchun:
            # send_sms(phone, f"Tasdiqlash kodingiz: {phone_code}")
            
            messages.success(request, "1/3: Telefon raqamga kod yuborildi!")
            return redirect('verify_phone')
    else:
        form = UserRegistrationForm()
    
    return render(request, 'register_step1.html', {'form': form})


# 2-QADAM: Telefon tasdiqlash
def verify_phone(request):
    user_id = request.session.get('reg_user_id')
    if not user_id:
        messages.error(request, "Avval ro'yxatdan o'ting!")
        return redirect('register_step1')
    
    try:
        user = User.objects.get(id=user_id)
        verification = PhoneVerification.objects.get(user=user)
    except:
        messages.error(request, "Xatolik yuz berdi!")
        return redirect('register_step1')
    
    if request.method == 'POST':
        entered_code = request.POST.get('code')
        
        if entered_code == verification.code:
            # Telefon tasdiqlandi
            verification.is_verified = True
            verification.save()
            
            messages.success(request, "✅ Telefon tasdiqlandi! Endi emailni tasdiqlang.")
            return redirect('verify_email')
        else:
            messages.error(request, "❌ Kod noto'g'ri! Qayta urinib ko'ring.")
    
    # Telefonni qisman yashirish
    phone = request.session.get('reg_phone')
    hidden_phone = phone[:4] + '****' + phone[-4:] if len(phone) > 8 else phone
    
    return render(request, 'verify_phone.html', {'phone': hidden_phone})


# 3-QADAM: Email tasdiqlash
def verify_email(request):
    user_id = request.session.get('reg_user_id')
    if not user_id:
        return redirect('register_step1')
    
    try:
        user = User.objects.get(id=user_id)
        # Email verification yaratish (agar yo'q bo'lsa)
        email_verification, created = EmailVerification.objects.get_or_create(
            user=user,
            defaults={
                'email': user.email,
                'code': ''.join([str(random.randint(0,9)) for _ in range(6)])
            }
        )
    except:
        messages.error(request, "Xatolik yuz berdi!")
        return redirect('register_step1')
    
    # Agar birinchi marta kelgan bo'lsa, emailga kod yuborish
    if request.method == 'GET' and not request.GET.get('resend'):
        # Kod yaratish va emailga yuborish
        code = email_verification.generate_code()
        
        # Email yuborish
        send_mail(
            'Email tasdiqlash kodi',
            f'Sizning tasdiqlash kodingiz: {code}',
            settings.EMAIL_HOST_USER,
            [user.email],
            fail_silently=False,
        )
        print(f"\n📧 EMAILGA KOD: {user.email} -> {code}\n")
    
    # Kodni qayta yuborish
    if request.GET.get('resend') == 'email':
        code = email_verification.generate_code()
        send_mail(
            'Yangi tasdiqlash kodi',
            f'Sizning yangi tasdiqlash kodingiz: {code}',
            settings.EMAIL_HOST_USER,
            [user.email],
            fail_silently=False,
        )
        messages.success(request, "Emailga yangi kod yuborildi!")
        return redirect('verify_email')
    
    if request.method == 'POST':
        entered_code = request.POST.get('code')
        
        if entered_code == email_verification.code:
            # Email tasdiqlandi
            email_verification.is_verified = True
            email_verification.save()
            
            messages.success(request, "✅ Email tasdiqlandi! Endi captcha ni tasdiqlang.")
            return redirect('verify_captcha')
        else:
            messages.error(request, "❌ Kod noto'g'ri! Qayta urinib ko'ring.")
    
    # Emailni qisman yashirish
    email = user.email
    hidden_email = email[:3] + '****' + email[email.find('@'):]
    
    return render(request, 'verify_email.html', {'email': hidden_email})


# 4-QADAM: Captcha
from captcha.fields import CaptchaField
from django import forms

class CaptchaForm(forms.Form):
    captcha = CaptchaField(label="Kodni kiriting")

def verify_captcha(request):
    user_id = request.session.get('reg_user_id')
    if not user_id:
        return redirect('register_step1')
    
    try:
        user = User.objects.get(id=user_id)
        phone_verified = PhoneVerification.objects.get(user=user, is_verified=True)
        email_verified = EmailVerification.objects.get(user=user, is_verified=True)
    except:
        messages.error(request, "Avval telefon va emailni tasdiqlang!")
        return redirect('register_step1')
    
    if request.method == 'POST':
        form = CaptchaForm(request.POST)
        if form.is_valid():
            # HAMMASI TASDIQLANDI!
            user.is_active = True
            user.save()
            
            # Avtomatik login
            login(request, user)
            
            # Sessiyani tozalash
            if 'reg_user_id' in request.session:
                del request.session['reg_user_id']
            if 'reg_phone' in request.session:
                del request.session['reg_phone']
            if 'reg_email' in request.session:
                del request.session['reg_email']
            
            messages.success(request, "✅✅✅ MUVAFFAQIYATLI RO'YXATDAN O'TINGIZ!")
            return redirect('create_seller_profile')
    else:
        form = CaptchaForm()
    
    return render(request, 'verify_captcha.html', {'form': form})


# Kodni qayta yuborish
def resend_phone_code(request):
    user_id = request.session.get('reg_user_id')
    if not user_id:
        return redirect('register_step1')
    
    try:
        user = User.objects.get(id=user_id)
        verification = PhoneVerification.objects.get(user=user)
        code = verification.generate_code()
        
        print(f"\n📱 YANGI TELEFON KODI: {verification.phone} -> {code}\n")
        messages.success(request, "Yangi SMS kod yuborildi!")
    except:
        messages.error(request, "Xatolik yuz berdi!")
    
    return redirect('verify_phone')


def resend_email_code(request):
    user_id = request.session.get('reg_user_id')
    if not user_id:
        return redirect('register_step1')
    
    try:
        user = User.objects.get(id=user_id)
        verification = EmailVerification.objects.get(user=user)
        code = verification.generate_code()
        
        send_mail(
            'Yangi tasdiqlash kodi',
            f'Sizning yangi tasdiqlash kodingiz: {code}',
            settings.EMAIL_HOST_USER,
            [user.email],
            fail_silently=False,
        )
        messages.success(request, "Yangi email kod yuborildi!")
    except:
        messages.error(request, "Xatolik yuz berdi!")
    
    return redirect('verify_email')


# SMS yuborish (ESKIZ.UZ)
def send_sms(phone, message):
    try:
        url = "https://notify.eskiz.uz/api/message/sms/send"
        payload = {
            'mobile_phone': phone,
            'message': message,
            'from': '4546'
        }
        headers = {
            'Authorization': 'Bearer YOUR_TOKEN'
        }
        response = requests.post(url, data=payload, headers=headers)
        return response.json()
    except:
        return None

def verify_email(request):
    user_id = request.session.get('verify_user_id')
    if not user_id:
        messages.error(request, "Avval ro'yxatdan o'ting!")
        return redirect('register')
    
    try:
        user = User.objects.get(id=user_id)
        verification = EmailVerification.objects.get(user=user)
    except:
        messages.error(request, "Xatolik yuz berdi!")
        return redirect('register')
    
    if request.method == 'POST':
        entered_code = request.POST.get('code')
        
        if entered_code == verification.code:
            # 1 2 3 - TO'G'RI
            user.is_active = True
            user.save()
            verification.delete()  # Kodni o'chirish
            
            # Avtomatik login
            login(request, user)
            
            # Sessiyani tozalash
            del request.session['verify_user_id']
            
            messages.success(request, "✅ Email tasdiqlandi! Endi sotuvchi profilini yarating.")
            return redirect('create_seller_profile')
        else:
            # 4 - NOTO'G'RI
            messages.error(request, "❌ 4 - Kod noto'g'ri! Qayta urinib ko'ring.")
    
    return render(request, 'verify_email.html', {'email': user.email})

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            # Userni yaratish, lekin active emas
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            
            # 6 xonali kod yaratish
            code = ''.join([str(random.randint(0,9)) for _ in range(6)])
            
            # Kodni saqlash
            EmailVerification.objects.create(
                user=user,
                code=code
            )
            
            # Emailga kod yuborish
            send_mail(
                'Tasdiqlash kodi',
                f'Sizning tasdiqlash kodingiz: {code}',
                settings.EMAIL_HOST_USER,
                [user.email],
                fail_silently=False,
            )
            
            # Sessiyaga user id ni saqlash
            request.session['verify_user_id'] = user.id
            
            messages.success(request, "Emailingizga tasdiqlash kodi yuborildi!")
            return redirect('verify_email')  # ⚡ Kod kiritish sahifasiga
    else:
        form = UserRegistrationForm()

        
    
    return render(request, 'register.html', {'form': form})
from .models import Product, Category, Seller, ProductImage, Favorite, Cart, CartItem, Order, OrderItem, Review, Chat, Message, Comment
from .forms import (
    ProductForm, SellerForm, UserRegistrationForm, ProductImageForm,
    ReviewForm, ComplaintForm, OrderForm, UserLoginForm, ProductFilterForm
)


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            # Userni vaqtincha saqlash
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            
            # Email tasdiqlash kodi yaratish
            email_verification, created = EmailVerification.objects.get_or_create(user=user)
            code = email_verification.generate_code()
            
            # Emailga kod yuborish
            send_mail(
                'Tasdiqlash kodi',
                f'Sizning tasdiqlash kodingiz: {code}',
                settings.EMAIL_HOST_USER,
                [user.email],
                fail_silently=False,
            )
            
            # Sessiyaga user ID ni saqlash
            request.session['verification_user_id'] = user.id
            
            messages.success(request, "Emailingizga kod yuborildi!")
            return redirect('verify_code')
    else:
        form = UserRegistrationForm()
    
    return render(request, 'register.html', {'form': form})


def verify_code(request):
    user_id = request.session.get('verification_user_id')
    if not user_id:
        messages.error(request, "Avval ro'yxatdan o'ting!")
        return redirect('register')
    
    try:
        user = User.objects.get(id=user_id)
        email_verification = EmailVerification.objects.get(user=user)
    except (User.DoesNotExist, EmailVerification.DoesNotExist):
        messages.error(request, "Xatolik yuz berdi!")
        return redirect('register')
    
    if request.method == 'POST':
        # Tugmalardan kelgan kodni olish
        code = request.POST.get('code', '')
        
        if code == email_verification.code:
            # To'g'ri kod
            email_verification.is_verified = True
            email_verification.save()
            
            # User ni aktivlashtirish
            user.is_active = True
            user.save()
            
            # Avtomatik login
            login(request, user)
            
            # Sessiyani tozalash
            del request.session['verification_user_id']
            
            messages.success(request, "Email tasdiqlandi! Xush kelibsiz!")
            return redirect('create_seller_profile')
        else:
            # Noto'g'ri kod - 4 NOTOG'RI
            messages.error(request, "4 - Kod noto'g'ri! Qayta urinib ko'ring.")
    
    return render(request, 'verify_code.html', {
        'email': user.email,
    })


def resend_code(request):
    """Kodni qayta yuborish"""
    user_id = request.session.get('verification_user_id')
    if not user_id:
        return redirect('register')
    
    try:
        user = User.objects.get(id=user_id)
        email_verification = EmailVerification.objects.get(user=user)
        code = email_verification.generate_code()
        
        # Emailga kod yuborish
        send_mail(
            'Yangi tasdiqlash kodi',
            f'Sizning yangi tasdiqlash kodingiz: {code}',
            settings.EMAIL_HOST_USER,
            [user.email],
            fail_silently=False,
        )
        
        messages.success(request, "Yangi kod yuborildi!")
    except:
        messages.error(request, "Xatolik yuz berdi!")
    
    return redirect('verify_code')

def send_sms(phone, message):
    # Twilio, Eskiz yoki boshqa SMS provider
    url = "https://notify.eskiz.uz/api/message/sms/send"
    payload = {
        'mobile_phone': phone,
        'message': message,
        'from': '4546'
    }
    headers = {
        'Authorization': 'Bearer YOUR_TOKEN'
    }
    try:
        response = requests.post(url, data=payload, headers=headers)
        return response.json()
    except:
        return None

# 1-QADAM: Registratsiya
def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            # Userni vaqtincha saqlash (aktiv emas)
            user = form.save(commit=False)
            user.is_active = False  # Tasdiqlanmaguncha aktiv emas
            user.save()
            
            # Email tasdiqlash kodi yaratish
            email_verification, created = EmailVerification.objects.get_or_create(user=user)
            email_code = email_verification.generate_code()
            
            # Telefon tasdiqlash kodi yaratish
            phone = form.cleaned_data.get('phone')
            phone_verification, created = PhoneVerification.objects.get_or_create(user=user)
            phone_verification.phone = phone
            phone_verification.generate_code()
            phone_verification.save()
            
            # Emailga kod yuborish
            send_mail(
                'Email tasdiqlash kodi',
                f'Sizning tasdiqlash kodingiz: {email_code}\n\nBu kodni hech kimga bermang!',
                settings.EMAIL_HOST_USER,
                [user.email],
                fail_silently=False,
            )
            
            # Telefonga SMS yuborish (SMS provider kerak)
            # send_sms(phone, f"Tasdiqlash kodingiz: {phone_verification.code}")
            
            # Sessiyaga user ID ni saqlash
            request.session['verification_user_id'] = user.id
            
            messages.success(request, "Ro'yxatdan o'tdingiz! Email va telefoningizni tasdiqlang.")
            return redirect('verify_email')
    else:
        form = UserRegistrationForm()
    
    return render(request, 'register.html', {'form': form})


# 2-QADAM: Email tasdiqlash
def verify_email(request):
    user_id = request.session.get('verification_user_id')
    if not user_id:
        messages.error(request, "Avval ro'yxatdan o'ting!")
        return redirect('register')
    
    try:
        user = User.objects.get(id=user_id)
        email_verification = EmailVerification.objects.get(user=user)
    except (User.DoesNotExist, EmailVerification.DoesNotExist):
        messages.error(request, "Xatolik yuz berdi!")
        return redirect('register')
    
    if request.method == 'POST':
        form = EmailVerificationForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data.get('code')
            if code == email_verification.code:
                email_verification.is_verified = True
                email_verification.save()
                messages.success(request, "Email tasdiqlandi! Endi telefon raqamingizni tasdiqlang.")
                return redirect('verify_phone')
            else:
                messages.error(request, "Kod noto'g'ri!")
    else:
        form = EmailVerificationForm()
    
    # Kodni qayta yuborish
    if request.GET.get('resend') == 'email':
        email_verification.generate_code()
        send_mail(
            'Email tasdiqlash kodi (qayta)',
            f'Sizning yangi tasdiqlash kodingiz: {email_verification.code}',
            settings.EMAIL_HOST_USER,
            [user.email],
            fail_silently=False,
        )
        messages.success(request, "Kod qayta yuborildi!")
        return redirect('verify_email')
    
    # Emailni qisman yashirish (****@gmail.com)
    hidden_email = user.email[:3] + '****' + user.email[user.email.find('@'):]
    
    return render(request, 'verify_email.html', {
        'form': form,
        'email': hidden_email,
        'user_id': user_id
    })


# 3-QADAM: Telefon tasdiqlash
def verify_phone(request):
    user_id = request.session.get('verification_user_id')
    if not user_id:
        messages.error(request, "Avval ro'yxatdan o'ting!")
        return redirect('register')
    
    try:
        user = User.objects.get(id=user_id)
        phone_verification = PhoneVerification.objects.get(user=user)
    except (User.DoesNotExist, PhoneVerification.DoesNotExist):
        messages.error(request, "Xatolik yuz berdi!")
        return redirect('register')
    
    if request.method == 'POST':
        form = PhoneVerificationForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data.get('code')
            if code == phone_verification.code:
                phone_verification.is_verified = True
                phone_verification.save()
                
                # User ni aktivlashtirish
                user.is_active = True
                user.save()
                
                # Sessiyani tozalash
                del request.session['verification_user_id']
                
                # Avtomatik login
                login(request, user)
                
                messages.success(request, "Tabriklaymiz! Ro'yxatdan o'tish muvaffaqiyatli yakunlandi!")
                return redirect('create_seller_profile')
            else:
                messages.error(request, "Kod noto'g'ri!")
    else:
        form = PhoneVerificationForm()
    
    # Kodni qayta yuborish
    if request.GET.get('resend') == 'phone':
        phone_verification.generate_code()
        # SMS yuborish
        # send_sms(phone_verification.phone, f"Tasdiqlash kodingiz: {phone_verification.code}")
        messages.success(request, "Kod qayta yuborildi!")
        return redirect('verify_phone')
    
    # Telefonni qisman yashirish (+998 ** *** 45 67)
    phone = phone_verification.phone
    hidden_phone = phone[:4] + ' ** *** ' + phone[-4:] if len(phone) > 8 else phone
    
    return render(request, 'verify_phone.html', {
        'form': form,
        'phone': hidden_phone,
        'user_id': user_id
    })
@login_required  
def like_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    Like.objects.get_or_create(user=request.user, product=product)
    return redirect('product_detail', pk=product.id)


def search(request):
    query = request.GET.get('q')

    products = Product.objects.filter(
        title__icontains=query
    )

    return render(request,'search.html',{
        'products':products
    })


# -------------------- BOSH SAHIFA --------------------
def home(request):
    query = request.GET.get('q', '')
    category_id = request.GET.get('category', '')
    condition = request.GET.get('condition', '')
    min_price = request.GET.get('min_price', '')
    max_price = request.GET.get('max_price', '')
    sort = request.GET.get('sort', 'newest')

    products = Product.objects.filter(status='active').select_related('seller', 'category')

    if query:
        products = products.filter(Q(title__icontains=query) | Q(description__icontains=query))
    if category_id and category_id.isdigit():
        products = products.filter(category_id=category_id)
    if condition:
        products = products.filter(condition=condition)
    if min_price and min_price.replace('.', '', 1).isdigit():
        products = products.filter(price__gte=min_price)
    if max_price and max_price.replace('.', '', 1).isdigit():
        products = products.filter(price__lte=max_price)

    if sort == 'price_asc':
        products = products.order_by('price')
    elif sort == 'price_desc':
        products = products.order_by('-price')
    elif sort == 'popular':
        products = products.order_by('-views_count')
    else:
        products = products.order_by('-created_at')

    categories = Category.objects.annotate(
        product_count=Count('products', filter=Q(products__status='active'))
    ).filter(product_count__gt=0)

    popular_products = Product.objects.filter(status='active').order_by('-views_count')[:10]
    total_products = products.count()

    paginator = Paginator(products, 12)
    page = request.GET.get('page')
    products_page = paginator.get_page(page)

    favorites = []
    if request.user.is_authenticated:
        favorites = list(Favorite.objects.filter(user=request.user).values_list('product_id', flat=True))

    cart_count = 0
    if request.user.is_authenticated:
        cart, _ = Cart.objects.get_or_create(user=request.user)
        cart_count = cart.items.count()
    else:
        session_id = request.session.session_key
        if session_id:
            cart, _ = Cart.objects.get_or_create(session_id=session_id)
            cart_count = cart.items.count()

    context = {
        'products': products_page,
        'categories': categories,
        'popular_products': popular_products,
        'total_products': total_products,
        'favorites': favorites,
        'cart_count': cart_count,
    }
    return render(request, 'index.html', context)

# -------------------- MAHSULOT DETALLARI --------------------
def product_detail(request, pk):
    product = get_object_or_404(Product.objects.select_related('seller', 'category'), pk=pk, status='active')
    product.views_count += 1
    product.save(update_fields=['views_count'])

    seller_products = Product.objects.filter(seller=product.seller, status='active').exclude(pk=product.pk)[:4]
    similar_products = Product.objects.filter(category=product.category, status='active').exclude(pk=product.pk)[:4]
    reviews = Review.objects.filter(product=product).select_related('user')
    avg_rating = reviews.aggregate(Avg('rating'))['rating__avg'] or 0

    is_favorite = False
    if request.user.is_authenticated:
        is_favorite = Favorite.objects.filter(user=request.user, product=product).exists()

    context = {
        'product': product,
        'seller_products': seller_products,
        'similar_products': similar_products,
        'is_favorite': is_favorite,
        'reviews': reviews,
        'avg_rating': round(avg_rating, 1),
        'review_form': ReviewForm(),
        'complaint_form': ComplaintForm(),
    }
    return render(request, 'product_detail.html', context)

# -------------------- SHARH QO'SHISH --------------------
@login_required
def add_review(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.product = product
            review.save()
            messages.success(request, "Sharhingiz qabul qilindi!")
    return redirect('product_detail', pk=pk)

# -------------------- SHIKOYAT QO'SHISH --------------------
def add_complaint(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ComplaintForm(request.POST)
        if form.is_valid():
            complaint = form.save(commit=False)
            complaint.product = product
            complaint.save()
            messages.success(request, "Shikoyatingiz qabul qilindi!")
    return redirect('product_detail', pk=pk)

# -------------------- SOTUVCHI PROFILI --------------------
def seller_profile(request, seller_id):
    seller = get_object_or_404(Seller, pk=seller_id)
    products = Product.objects.filter(seller=seller, status='active').order_by('-created_at')
    paginator = Paginator(products, 12)
    page = request.GET.get('page')
    products_page = paginator.get_page(page)
    return render(request, 'seller_profile.html', {'seller': seller, 'products': products_page})

# -------------------- YANGI E'LON QO'SHISH --------------------
@login_required
def create_product(request):
    try:
        seller = Seller.objects.get(user=request.user)
    except Seller.DoesNotExist:
        messages.warning(request, "Avval sotuvchi profilini to'ldiring!")
        return redirect('create_seller_profile')

    ImageFormSet = modelformset_factory(ProductImage, form=ProductImageForm, extra=5, max_num=5, can_delete=True)

    if request.method == 'POST':
        form = ProductForm(request.POST)
        formset = ImageFormSet(request.POST, request.FILES, queryset=ProductImage.objects.none())
        if form.is_valid() and formset.is_valid():
            product = form.save(commit=False)
            product.seller = seller
            product.status = 'active'
            product.save()

            images_saved = False
            for f in formset:
                if f.cleaned_data and not f.cleaned_data.get('DELETE', False):
                    image = f.cleaned_data.get('image')
                    if image:
                        is_main = f.cleaned_data.get('is_main', False)
                        if not images_saved and not is_main:
                            is_main = True
                        ProductImage.objects.create(product=product, image=image, is_main=is_main)
                        images_saved = True
            messages.success(request, "E'lon muvaffaqiyatli qo'shildi!")
            return redirect('product_detail', pk=product.pk)
    else:
        form = ProductForm()
        formset = ImageFormSet(queryset=ProductImage.objects.none())

    return render(request, 'create_product.html', {'form': form, 'formset': formset})

# -------------------- E'LONNI TAHRIRLASH --------------------
@login_required
def update_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if product.seller.user != request.user:
        messages.error(request, "Siz faqat o'z e'lonlaringizni tahrirlay olasiz!")
        return redirect('home')

    ImageFormSet = modelformset_factory(ProductImage, form=ProductImageForm, extra=3, max_num=5, can_delete=True)

    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        formset = ImageFormSet(request.POST, request.FILES, queryset=product.images.all())
        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            messages.success(request, "E'lon yangilandi!")
            return redirect('product_detail', pk=product.pk)
    else:
        form = ProductForm(instance=product)
        formset = ImageFormSet(queryset=product.images.all())

    return render(request, 'update_product.html', {'form': form, 'formset': formset, 'product': product})


send_mail(
    "Tasdiqlash kodi",
    "Sizning kodingiz: 12345",
    "site@gmail.com",
    ["recipient@gmail.com"],
)

# -------------------- E'LONNI O'CHIRISH --------------------
@login_required
def delete_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if product.seller.user != request.user:
        messages.error(request, "Siz faqat o'z e'lonlaringizni o'chira olasiz!")
        return redirect('home')
    if request.method == 'POST':
        product.status = 'archived'
        product.save()
        messages.success(request, "E'lon o'chirildi!")
        return redirect('my_products')
    return render(request, 'delete_product.html', {'product': product})

# -------------------- SOTUVCHI PROFILI YARATISH --------------------
@login_required
def create_seller_profile(request):
    try:
        seller = Seller.objects.get(user=request.user)
        return redirect('edit_seller_profile')
    except Seller.DoesNotExist:
        pass

    if request.method == 'POST':
        form = SellerForm(request.POST, request.FILES)
        if form.is_valid():
            seller = form.save(commit=False)
            seller.user = request.user
            seller.save()
            messages.success(request, "Sotuvchi profili yaratildi!")
            return redirect('home')
    else:
        form = SellerForm()
    return render(request, 'create_seller_profile.html', {'form': form})

# -------------------- SOTUVCHI PROFILINI TAHRIRLASH --------------------
@login_required
def edit_seller_profile(request):
    seller = get_object_or_404(Seller, user=request.user)
    if request.method == 'POST':
        form = SellerForm(request.POST, request.FILES, instance=seller)
        if form.is_valid():
            form.save()
            messages.success(request, "Profil yangilandi!")
            return redirect('seller_profile', seller_id=seller.id)
    else:
        form = SellerForm(instance=seller)
    return render(request, 'edit_seller_profile.html', {'form': form, 'seller': seller})

# -------------------- MENING E'LONLARIM --------------------
@login_required
def my_products(request):
    seller = get_object_or_404(Seller, user=request.user)
    products = Product.objects.filter(seller=seller).order_by('-created_at')
    status = request.GET.get('status', '')
    if status:
        products = products.filter(status=status)
    paginator = Paginator(products, 12)
    page = request.GET.get('page')
    products_page = paginator.get_page(page)
    return render(request, 'my_products.html', {'products': products_page, 'current_status': status})

# -------------------- SAQLANGANLAR --------------------
@login_required
def toggle_favorite(request, pk):
    product = get_object_or_404(Product, pk=pk)
    favorite, created = Favorite.objects.get_or_create(user=request.user, product=product)
    if not created:
        favorite.delete()
        status = 'removed'
        msg = "Saqlanganlardan olib tashlandi!"
    else:
        status = 'added'
        msg = "Saqlanganlarga qo'shildi!"
    messages.success(request, msg)
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'status': status,
            'favorite_count': Favorite.objects.filter(user=request.user).count()
        })
    return redirect(request.META.get('HTTP_REFERER', 'home'))

@login_required
def favorites(request):
    favorites = Favorite.objects.filter(user=request.user).select_related('product').order_by('-created_at')
    products = [fav.product for fav in favorites if fav.product.status == 'active']
    paginator = Paginator(products, 12)
    page = request.GET.get('page')
    products_page = paginator.get_page(page)
    return render(request, 'favorites.html', {'products': products_page})

# -------------------- AUTENTIFIKATSIYA --------------------
def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Muvaffaqiyatli ro'yxatdan o'tdingiz!")
            return redirect('create_seller_profile')
    else:
        form = UserRegistrationForm()
    return render(request, 'register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                messages.success(request, f"Xush kelibsiz, {user.username}!")
                try:
                    Seller.objects.get(user=user)
                except Seller.DoesNotExist:
                    messages.info(request, "Sotuvchi profilini to'ldiring!")
                return redirect('home')
        else:
            messages.error(request, "Login yoki parol noto'g'ri!")
    else:
        form = UserLoginForm()
    return render(request, 'login.html', {'form': form})

def user_logout(request):
    logout(request)
    messages.success(request, "Hisobingizdan chiqildi!")
    return redirect('home')

# -------------------- SAVATCHA --------------------
def get_or_create_cart(request):
    if request.user.is_authenticated:
        cart, _ = Cart.objects.get_or_create(user=request.user)
    else:
        if not request.session.session_key:
            request.session.create()
        session_id = request.session.session_key
        cart, _ = Cart.objects.get_or_create(session_id=session_id, user=None)
    return cart

def cart_view(request):
    cart = get_or_create_cart(request)
    cart_items = cart.items.select_related('product').all()
    total = sum(item.subtotal for item in cart_items)
    return render(request, 'cart.html', {
        'cart_items': cart_items,
        'total': total,
        'cart_count': cart_items.count(),
    })

def add_to_cart(request, pk):
    product = get_object_or_404(Product, pk=pk, status='active')
    cart = get_or_create_cart(request)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product, defaults={'quantity': 1})
    if not created:
        cart_item.quantity += 1
        cart_item.save()
        messages.success(request, f"{product.title} soni oshirildi!")
    else:
        messages.success(request, f"{product.title} savatchaga qo'shildi!")
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'status': 'success', 'cart_count': cart.items.count()})
    return redirect(request.META.get('HTTP_REFERER', 'home'))

def update_cart_quantity(request, pk):
    if request.method == 'POST':
        action = request.POST.get('action')
        cart = get_or_create_cart(request)
        try:
            cart_item = CartItem.objects.get(cart=cart, product_id=pk)
            if action == 'increase':
                cart_item.quantity += 1
                cart_item.save()
            elif action == 'decrease':
                if cart_item.quantity > 1:
                    cart_item.quantity -= 1
                    cart_item.save()
                else:
                    cart_item.delete()
            messages.success(request, "Savatcha yangilandi!")
        except CartItem.DoesNotExist:
            pass
    return redirect('cart_view')

def remove_from_cart(request, pk):
    cart = get_or_create_cart(request)
    CartItem.objects.filter(cart=cart, product_id=pk).delete()
    messages.success(request, "Mahsulot savatchadan o'chirildi!")
    return redirect('cart_view')

def clear_cart(request):
    cart = get_or_create_cart(request)
    cart.items.all().delete()
    messages.success(request, "Savatcha tozalandi!")
    return redirect('cart_view')

# -------------------- BUYURTMA --------------------
@login_required
def checkout(request):
    cart = get_or_create_cart(request)
    cart_items = cart.items.select_related('product').all()
    if not cart_items:
        messages.warning(request, "Savatchangiz bo'sh!")
        return redirect('home')
    total = sum(item.subtotal for item in cart_items)

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = Order.objects.create(
                user=request.user,
                full_name=form.cleaned_data['full_name'],
                phone=form.cleaned_data['phone'],
                email=form.cleaned_data['email'],
                city=form.cleaned_data['city'],
                address=form.cleaned_data['address'],
                comment=form.cleaned_data['comment'],
                total_amount=total
            )
            for item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    product_title=item.product.title,
                    product_price=item.product.price,
                    quantity=item.quantity
                )
            cart.items.all().delete()
            messages.success(request, "Buyurtmangiz qabul qilindi!")
            return redirect('order_success', order_id=order.id)
    else:
        initial = {}
        if request.user.is_authenticated:
            try:
                seller = Seller.objects.get(user=request.user)
                initial = {'full_name': seller.full_name, 'phone': seller.phone}
            except Seller.DoesNotExist:
                initial = {'full_name': f"{request.user.first_name} {request.user.last_name}", 'email': request.user.email}
        form = OrderForm(initial=initial)

    return render(request, 'checkout.html', {'form': form, 'cart_items': cart_items, 'total': total, 'cart_count': cart_items.count()})

def order_success(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    return render(request, 'order_success.html', {'order': order})

@login_required
def my_orders(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'my_orders.html', {'orders': orders})

# -------------------- KATEGORIYALAR --------------------
def category_products(request, slug):
    category = get_object_or_404(Category, slug=slug)
    products = Product.objects.filter(category=category, status='active').order_by('-created_at')
    paginator = Paginator(products, 12)
    page = request.GET.get('page')
    products_page = paginator.get_page(page)
    return render(request, 'category_products.html', {'category': category, 'products': products_page})

# -------------------- QIDIRUV --------------------
def search(request):
    form = ProductFilterForm(request.GET)
    products = Product.objects.filter(status='active')

    if form.is_valid():
        q = form.cleaned_data.get('q')
        category = form.cleaned_data.get('category')
        condition = form.cleaned_data.get('condition')
        min_price = form.cleaned_data.get('min_price')
        max_price = form.cleaned_data.get('max_price')
        sort = form.cleaned_data.get('sort')

        if q:
            products = products.filter(Q(title__icontains=q) | Q(description__icontains=q))
        if category:
            products = products.filter(category=category)
        if condition:
            products = products.filter(condition=condition)
        if min_price:
            products = products.filter(price__gte=min_price)
        if max_price:
            products = products.filter(price__lte=max_price)

        if sort == 'price_asc':
            products = products.order_by('price')
        elif sort == 'price_desc':
            products = products.order_by('-price')
        elif sort == 'popular':
            products = products.order_by('-views_count')
        else:
            products = products.order_by('-created_at')

    paginator = Paginator(products, 12)
    page = request.GET.get('page')
    products_page = paginator.get_page(page)

    context = {
        'form': form,
        'products': products_page,
        'total_count': products.count(),
    }
    return render(request, 'search.html', context)

@login_required
def start_chat(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if product.seller.user == request.user:
        return redirect('product_detail', pk=product.id)

    chat, created = Chat.objects.get_or_create(
        buyer=request.user,
        seller=product.seller.user,
        product=product
    )

    return redirect('chat_detail', chat_id=chat.id)

@login_required
def chat_detail(request, chat_id):
    chat = get_object_or_404(Chat, id=chat_id)

    if request.user not in [chat.buyer, chat.seller]:
        return redirect('home')

    if request.method == 'POST':
        text = request.POST.get('text')
        if text:
            Message.objects.create(
                chat=chat,
                sender=request.user,
                text=text
            )
        return HttpResponseRedirect(reverse('chat_detail', args=[chat.id]))

    messages_list = chat.messages.all().order_by('created_at')
    return render(request, 'chat.html', {'chat': chat, 'messages': messages_list})

@login_required
def add_comment(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.method == 'POST':
        text = request.POST.get('text')
        if text:
            Comment.objects.create(
                product=product,
                user=request.user,
                text=text
            )

    return redirect('product_detail', pk=product.id)


def add_categories(request):
    categories_data = [
        ('Elektronika', 'elektronika', 'mobile-alt'),
        ('Telefonlar', 'telefonlar', 'phone'),
        ('Kompyuterlar', 'kompyuterlar', 'laptop'),
        ('Planshetlar', 'planshetlar', 'tablet-alt'),
        ('Kiyim', 'kiyim', 'tshirt'),
        ('Erkaklar kiyimi', 'erkaklar-kiyimi', 'user-tie'),
        ('Ayollar kiyimi', 'ayollar-kiyimi', 'user'),
        ('Transport', 'transport', 'car'),
        ('Yengil avtomobillar', 'yengil-avtomobillar', 'car'),
        ('Uy-joy', 'uy-joy', 'home'),
        ('Kvartiralar', 'kvartiralar', 'building'),
        ('Hayvonlar', 'hayvonlar', 'dog'),
        ('Itlar', 'itlar', 'dog'),
        ('Mushuklar', 'mushuklar', 'cat'),
        ('Xizmatlar', 'xizmatlar', 'tools'),
        ('Uy-ro\'zg\'or', 'uy-rozgor', 'couch'),
        ('Sport', 'sport', 'futbol'),
        ('Kitoblar', 'kitoblar', 'book'),
        ('Bolalar dunyosi', 'bolalar-dunyosi', 'baby'),
        ('Salomatlik', 'salomatlik', 'heartbeat'),
        ('Bog\'', 'bog', 'seedling'),
        ('Ish o\'rinlari', 'ish-orinlari', 'briefcase'),
        ('Boshqa', 'boshqa', 'th-large'),
    ]
    
    count = 0
    for name, slug, icon in categories_data:
        cat, created = Category.objects.get_or_create(
            slug=slug,
            defaults={'name': name, 'icon': icon}
        )
        if created:
            count += 1
    
    return JsonResponse({'status': 'success', 'added': count})

def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')

def help_page(request):
    return render(request, 'help.html')

def terms(request):
    return render(request, 'terms.html')

def privacy(request):
    return render(request, 'privacy.html')