from django.urls import include, path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('help/', views.help_page, name='help'),
    path('terms/', views.terms, name='terms'),
    path('privacy/', views.privacy, name='privacy'),
    
    path('product/<int:pk>/', views.product_detail, name='product_detail'),
    path('product/add/', views.create_product, name='create_product'),
    path('product/update/<int:pk>/', views.update_product, name='update_product'),
    path('product/delete/<int:pk>/', views.delete_product, name='delete_product'),
    path('product/<int:pk>/review/', views.add_review, name='add_review'),
    path('product/<int:pk>/complaint/', views.add_complaint, name='add_complaint'),
    
    path('category/<slug:slug>/', views.category_products, name='category_products'),
    path('search/', views.search, name='search'),
    
    path('seller/create/', views.create_seller_profile, name='create_seller_profile'),
    path('seller/edit/', views.edit_seller_profile, name='edit_seller_profile'),
    path('seller/<int:seller_id>/', views.seller_profile, name='seller_profile'),
    path('my-products/', views.my_products, name='my_products'),
    
    path('favorites/', views.favorites, name='favorites'),
    path('toggle-favorite/<int:pk>/', views.toggle_favorite, name='toggle_favorite'),
    
    path('cart/', views.cart_view, name='cart_view'),
    path('cart/add/<int:pk>/', views.add_to_cart, name='add_to_cart'),
    path('cart/update/<int:pk>/', views.update_cart_quantity, name='update_cart_quantity'),
    path('cart/remove/<int:pk>/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/clear/', views.clear_cart, name='clear_cart'),
    
    path('checkout/', views.checkout, name='checkout'),
    path('order/success/<int:order_id>/', views.order_success, name='order_success'),
    path('my-orders/', views.my_orders, name='my_orders'),
    
    path('login/', views.user_login, name='user_login'),
    path('logout/', views.user_logout, name='user_logout'),

    path('chat/start/<int:product_id>/', views.start_chat, name='start_chat'),
    path('chat/<int:chat_id>/', views.chat_detail, name='chat_detail'),
    path('comment/<int:product_id>/', views.add_comment, name='add_comment'),
    path('like/<int:product_id>/', views.like_product, name='like_product'), 
    path('captcha/', include('captcha.urls')),

    path('register/', views.register, name='register'),
    path('verify-email/', views.verify_email, name='verify_email'),
    path('verify-phone/', views.verify_phone, name='verify_phone'),

    path('register/', views.register, name='register'),
    path('verify-code/', views.verify_code, name='verify_code'),
    path('resend-code/', views.resend_code, name='resend_code'),

    path('verify-email/', views.verify_email, name='verify_email'),

        path('register/', views.register_step1, name='register_step1'),
    path('verify-phone/', views.verify_phone, name='verify_phone'),
    path('verify-email/', views.verify_email, name='verify_email'),
    path('verify-captcha/', views.verify_captcha, name='verify_captcha'),
    path('resend-phone-code/', views.resend_phone_code, name='resend_phone_code'),
    path('resend-email-code/', views.resend_email_code, name='resend_email_code'),
]

