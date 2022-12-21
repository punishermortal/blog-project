
from django.contrib import admin
from django.urls import path
from blogapp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.home),
    path('about/',views.about,name='about'), #this name=about is needed for link about page in nav bar
    path('contact/',views.contact,name='contact'),
    path('dashboard/',views.dashboard,name='dashboard'),
    path('login/',views.user_login,name='login'),
    path('signup/',views.user_signup,name='signup'),
    path('logout/',views.user_logout,name='logout'),
    path('addpost/',views.add_Post,name='addpost'),

    #for update post need dynamic url q ki jis post ke liye update krna wo specific post cahiye hoga
    path('updatepost/<int:id>',views.update_Post,name='updatepost'),
    path('deletepost/<int:id>',views.delet_Post,name='deletepost'),
    
]
