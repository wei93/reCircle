# app/urls.py

from django.conf.urls import url

from app import views

urlpatterns = [
	url(r'^profile/$', views.profile, name='profile'),
	url(r'^ProductDetail/download_my_pdf/$', views.download_pdf, name='download'),
	url(r'^ProductDetail/$', views.productdetail, name='productdetail'),
]
