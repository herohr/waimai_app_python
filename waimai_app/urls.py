"""waimai_app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from waimai_app import UserClient, image, verify_code, VendorClient

urlpatterns = [
    path('admin/', admin.site.urls),

    path('users', UserClient.user.userAPI.router(methods=["POST", ])),
    path('users/login', UserClient.user.login),
    path('users/info', UserClient.user.user_info_API.router(methods=["GET", "POST", "PUT"])),

    path('vendors/info', VendorClient.vendor_info_API.router(["GET", "POST", "PUT"])),
    path("vendors/login", VendorClient.login),
    path("vendors", VendorClient.vendorAPI.router(["POST"])),

    path("verify_code", verify_code.verify_code_API.router(methods=["GET", "POST"])),
    path("verify_message", verify_code.message_API.router(methods=["PUT"])),
    path("images", image.image_store_API.router(methods=["GET", "POST", "PUT"])),
    path("images/callback", image.image_callback_API.router(methods=["POST"]))
]
