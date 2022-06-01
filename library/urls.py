from django.contrib import admin
from django.urls import path
from libraryapp import views
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index),
    path('index/', views.index),
    path('login/', views.login),
    path('logout/', views.logout),
    path('usermain/', views.usermain),
    path('adminmain/', views.adminmain),
    path('adminmain/<int:bookid>/', views.adminmain),
    path('adminadd/', views.adminadd),
    path('adminfix/<int:bookid>/', views.adminfix),
    path('adminfix/<int:bookid>/<str:uptype>/', views.adminfix),
    path('book/<int:bookid>/', views.book),
    path('userbook/<int:bookid>/', views.userbook),
    path('userbook/<int:bookid>/<str:btype>/', views.userbook),
    path('adminbook/<int:bookid>/', views.adminbook),
    path('adminall/', views.adminall),
    url(r'^index/', views.index),
    path('index/<str:book_name>/', views.index),
    url(r'^usermain/', views.index),
    path('usermain/<str:book_name>/', views.index),
    url(r'^adminmain/', views.index),
    path('adminmain/<str:book_name>/', views.index),
    path('userstudy/', views.userstudy),
]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)