from . import views
from django.urls import path
from .views import ProfileUpdateView,ProfileView, DeviceCreateView, DeviceUpdateView
from django.urls import include, re_path as url

urlpatterns = [
    path('login/', views.loginUser, name='login'),
    url(r"^accounts/login/$", views.loginUser, name="login"),
    path('signup/', views.signup, name='signup'),
    path('logout/', views.logoutUser, name='logout'),
    path('favorites/', views.favorites, name='favorites'),
    path('', views.devicelist, name='home'),
    path('device/create', views.DeviceCreateView.as_view(), name='create_device'),
    #path('devicedetail/<slug:slug>/update/', views.DeviceDeleteView.as_view(), name='device-delete'),
    path('devicedetail/<slug:slug>/refresh/', views.devicerefresh, name='device_refresh'),
    path('devicedetail/<slug:slug>/reboot/', views.devicereboot, name='device_reboot'),
    path('devicedetail/<slug:slug>/', views.devicedetail, name='device_detail'),
    path('devicedetail/<slug:slug>/update/', DeviceUpdateView.as_view(), name='device-update'),
    path('fetch_device', views.fetch_device, name="fetch_device"),
    path('profile-update/', ProfileUpdateView.as_view(), name='profile-update'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('about/',views.about,name='about'),
    path('faq/',views.faq,name='faq'),
    path('search/',views.search,name='search'),
    path('devicetags/<slug:slug>/', views.devices_by_tag, name='devices_by_tag'),
]

from django.conf import settings
from django.conf.urls.static import static
if settings.DEBUG: 
        urlpatterns += static(settings.MEDIA_URL, 
                              document_root=settings.MEDIA_ROOT)
