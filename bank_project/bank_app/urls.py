from . import views
from django.urls import path

app_name = 'bank_app'
urlpatterns = [

    path('', views.home, name='home'),
    path('register', views.register, name='register'),
    path('index_login', views.index_login, name='index_login'),
    path('logout', views.logout_view, name='logout'),
    path('details', views.details, name='details'),
    path('success', views.success, name='success'),
    path('get_branches/<int:dist_id>/', views.get_branches, name='get_branches'),
    # path('get_branches', views.get_branches, name='get_branches'),
]

