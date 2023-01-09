import time
from django.shortcuts import render, redirect
from django.views import generic
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.models import User
from .models import Device, Snap, FavouriteDevice, Profile
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse, JsonResponse
from django.views.generic import RedirectView
from django.http import HttpResponse
from django.views.generic import RedirectView,TemplateView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from django.shortcuts import render,get_object_or_404
import json
from django.forms import model_to_dict
from .forms import SignupForm, UserForm,ProfileForm
from django.db.models import Q
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.db import IntegrityError
from taggit.models import Tag
from django.views.generic import UpdateView, CreateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
import datetime
import logging
from .mqtt import ClientInfoObject, agentIface, ClientDict
from django.http import JsonResponse

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def default(o):
    if isinstance(o, (datetime.date, datetime.datetime)):
        return o.isoformat()
    return str(o)

def loginUser(request):
    if not request.user.is_authenticated:
        if request.method == "POST":
            user = authenticate(username=request.POST.get("username"), password=request.POST.get("password"))
            if user is not None:
                login(request, user)
                messages.success(request, "Logged In Successfully")
                return redirect('home')
            else:
                messages.error(request, "Invalid credentials")
        return render(request, "login.html")
    return redirect("home")


def devicelist(request):
    
    device_list= Paginator(Device.objects.all().order_by('-created_on'),2)
    page= request.GET.get('page')

    try:
         devices = device_list.page(page)
    except PageNotAnInteger:
         devices = device_list.page(1)
    except EmptyPage:
         devices = device_list.page(device_list.num_pages)

    return render(request,'index.html', {"device_list": devices})

def fetch_device(request):
    device_list= Paginator(Device.objects.all().order_by('-created_on'),2)
    page=request.POST.get("page")

    try:
        devices = device_list.page(page)
    except PageNotAnInteger:
        devices = device_list.page(1)
    except EmptyPage:
        devices = device_list.page(device_list.num_pages)

    device_dic = {
        "number": devices.number,
        "has_next": devices.has_next(),
        "has_previous": devices.has_previous(),
        "devices": []
    }

    for i in device_list.page(page):
        device_dic["devices"].append(i.__dict__)
    
    for i in device_dic["devices"]:
        i["author"]=User.objects.get(id = i.get("author_id")).username

   
    return JsonResponse({"device_list": json.dumps(device_dic, default = default)})

def devicedetail(request, slug):
        
    device = Device.objects.get(slug=slug)
    device.save()

    if request.user.is_authenticated:
        Favourites,_ = FavouriteDevice.objects.get_or_create(user=request.user)
    device_in_favorites = None

    if request.user.is_authenticated:
        if device in Favourites.devices.all():
            device_in_favorites = True
        else:
            device_in_favorites = False

    FavouritesUsers=FavouriteDevice.objects.filter(Q(devices=device.id) | Q(devices=device.id))
    
    try:
        ClientDict[str(device.serialno)].status = 0
    except KeyError:
        agentIface.subscribeTopic(agentIface.MQTT_SUBSCRIBE_TOPIC_BASE + format(device.serialno),device.serialno)
        ClientDict[str(device.serialno)].status = 0

    agentIface.publishData(agentIface.MQTT_PUBLISH_TOPIC_BASE + format(device.serialno),"heartbeat",2)
    time.sleep(2)
   
    try:
        device.status = ClientDict[str(device.serialno)].status
    except KeyError:
        print('key value not found')
        
    if device.status:
        agentIface.publishData(agentIface.MQTT_PUBLISH_TOPIC_BASE + format(device.serialno),"getuserinfo",2)
        time.sleep(2)
        device.deviceusers = ClientDict[str(device.serialno)].deviceusers
        device.save()   

        agentIface.publishData(agentIface.MQTT_PUBLISH_TOPIC_BASE + format(device.serialno),"getsysteminfo",2)
        time.sleep(2)
        device.deviceinfo = ClientDict[str(device.serialno)].deviceinfo
        device.save()   


        agentIface.publishData(agentIface.MQTT_PUBLISH_TOPIC_BASE + format(device.serialno),"getsnapinfo",2)
        time.sleep(2)
        device.devicesnaps = ClientDict[str(device.serialno)].devicesnaps
        device.save()   


        device.deviceuptime = ClientDict[str(device.serialno)].deviceuptime
        device.save()   
    print("Fatih1:" + device.deviceinfo)
    print("Fatih2:" + device.devicesnaps)
    return render(request, 'devicedetail.html', {'device': device, 'serialno': device.serialno, 'status': device.status, 'deviceuptime': device.deviceuptime, 'devicesnaps': device.devicesnaps,  'deviceusers': device.deviceusers, 'deviceinfo': device.deviceinfo, 'device_in_favorites': device_in_favorites,"FavouritesUsers":FavouritesUsers})

def devicerefresh(request, slug): 
    device = Device.objects.get(slug=slug)
    device.save()

    if request.user.is_authenticated:
        Favourites,_ = FavouriteDevice.objects.get_or_create(user=request.user)
    device_in_favorites = None

    if request.user.is_authenticated:
        if device in Favourites.devices.all():
            device_in_favorites = True
        else:
            device_in_favorites = False

    FavouritesUsers=FavouriteDevice.objects.filter(Q(devices=device.id) | Q(devices=device.id))
    
    try:
        ClientDict[str(device.serialno)].status = 0
    except KeyError:
        agentIface.subscribeTopic(agentIface.MQTT_SUBSCRIBE_TOPIC_BASE + format(device.serialno),device.serialno)
        ClientDict[str(device.serialno)].status = 0

    agentIface.publishData(agentIface.MQTT_PUBLISH_TOPIC_BASE + format(device.serialno),"heartbeat",2)
    time.sleep(2)
   
    try:
        device.status = ClientDict[str(device.serialno)].status
    except KeyError:
        print('key value not found')
        
    if device.status:
        agentIface.publishData(agentIface.MQTT_PUBLISH_TOPIC_BASE + format(device.serialno),"getuserinfo",2)
        time.sleep(2)
        device.deviceusers = ClientDict[str(device.serialno)].deviceusers
        device.save()   

        agentIface.publishData(agentIface.MQTT_PUBLISH_TOPIC_BASE + format(device.serialno),"getsysteminfo",2)
        time.sleep(2)
        device.deviceinfo = ClientDict[str(device.serialno)].deviceinfo
        device.save()   

        agentIface.publishData(agentIface.MQTT_PUBLISH_TOPIC_BASE + format(device.serialno),"getsnapinfo",2)
        time.sleep(2)
        device.devicesnaps = ClientDict[str(device.serialno)].devicesnaps
        device.save()   

        device.deviceuptime = ClientDict[str(device.serialno)].deviceuptime
        device.save()   

    return render(request, 'devicedetail.html', {'device': device, 'serialno': device.serialno, 'status': device.status, 'deviceuptime': device.deviceuptime, 'devicesnaps': device.devicesnaps,  'deviceusers': device.deviceusers, 'deviceinfo': device.deviceinfo, 'device_in_favorites': device_in_favorites,"FavouritesUsers":FavouritesUsers})

def devicereboot(request, slug):
    device = Device.objects.get(slug=slug)
    #request_data = json.loads(request.body)
    #rc, mid = mqtt_client.publish(request_data['topic'], request_data['msg'])
    #rc.wait_for_publish()
    #return JsonResponse({'code': rc})
    #FavouritesUsers=FavouriteDevice.objects.filter(Q(devices=device.id) | Q(devices=device.id))
    device = Device.objects.get(slug=slug)
    device.save()

    if request.user.is_authenticated:
        Favourites,_ = FavouriteDevice.objects.get_or_create(user=request.user)
    device_in_favorites = None

    if request.user.is_authenticated:
        if device in Favourites.devices.all():
            device_in_favorites = True
        else:
            device_in_favorites = False
    
    if request.user.is_authenticated:
        agentIface.publishData(agentIface.MQTT_TOPIC_BASE + "/" + format(device.id),"Reboot",0)

    FavouritesUsers=FavouriteDevice.objects.filter(Q(devices=device.id) | Q(devices=device.id))
    return render(request, 'devicedetail.html', {'device': device, 'device_in_favorites': device_in_favorites,"FavouritesUsers":FavouritesUsers})

def logoutUser(request):
    logout(request)
    messages.info(request, "Logged out of IOT Device Manager")
    return redirect("home")


def signup(request):
    if request.method == 'POST':
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        password_c = request.POST.get("password-c")
        if (password == password_c):
            try:
                user = User.objects.create_user(username, email, password);
                user.save()
                login(request, user)
                messages.success(request, "Logged In Successfully")
                return redirect("home")
            except IntegrityError:
                messages.info(request, "Try different Username")
                return render(request, "signup.html")
        messages.error(request, "Password doesn't match Confirm Password")
    if request.user.is_authenticated:
        return redirect('home')
    return render(request, "signup.html")


def favorites(request):
    user = request.user
    FavDevices,_ = FavouriteDevice.objects.get_or_create(user=user)
    userdevices=Device.objects.filter(Q(author=user) | Q(author=user))

    return render(request, 'favourites.html', { 'device_list': FavDevices.devices.all(), "favorites": True,"userdevices":userdevices})


def Favorites(request, slug):
    if not request.user.is_authenticated:
        return redirect('login')

    Favourites,_ = FavouriteDevice.objects.get_or_create(user=request.user)
    try:
        device = Device.objects.get(slug=slug)
    except Device.DoesNotExist:
        device = None

    if device not in Favourites.devices.all():
        Favourites.devices.add(device)
    else:
        Favourites.devices.remove(device)
    
    Favourites.save()
    
    return HttpResponse('Success')


def about(request):
    context={}
    return render(request,'about.html',context=context)

def faq(request):
    context={}
    return render(request,'faq.html',context=context)

def search(request):
    query = request.GET.get('query', None)
    alldevices=Device.objects.filter(Q(title__icontains=query) | Q(content__icontains=query))
    params={'device_list':alldevices,}
    return render(request,'search.html',params)


from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .forms import UserForm, ProfileForm
from django.contrib.auth.models import User
from .models import Device, Profile, Snap

from django.contrib import messages

class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'profile.html'

class ProfileUpdateView(LoginRequiredMixin, TemplateView):
    user_form = UserForm()
    profile_form = ProfileForm()
    template_name = 'profile-update.html'

    def post(self, request):

        post_data = request.POST or None
        file_data = request.FILES or None

        user_form = UserForm(post_data, instance=request.user)
        profile_form = ProfileForm(post_data, file_data, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.error(request, 'Your profile is updated successfully!')
            return HttpResponseRedirect(reverse_lazy('profile'))

        context = self.get_context_data(
                                        user_form=user_form,
                                        profile_form=profile_form
                                    )

        return self.render_to_response(context)     

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

class DeviceUpdateView(LoginRequiredMixin, UpdateView):
    model = Device
    fields = ['title', 'serialno', 'content', 'image', 'tags']

    template_name ='device_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class DeviceCreateView(LoginRequiredMixin,CreateView):
    model = Device
    fields = ['title', 'serialno', 'content', 'image', 'tags']
    template_name = 'device_form.html'
    redirect_field_name = "redirect"  # added
    redirect_authenticated_user = True  # added
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

#class DeviceDeleteView(LoginRequiredMixin,DeleteView):
#    model = Device
    #fields = ['title', 'content', 'image', 'tags']
#    template_name = 'device_confirm_delete.html'
#    redirect_field_name = "redirect"  # added
#    redirect_authenticated_user = True  # added
    #Device.objects.filter(slug=slug).delete()
    #<a class="btn btn-info btn-lg"  href="{% url "device-delete" device.slug %}">Delete</a>
    #def form_valid(self, form):
    #    form.instance.author = self.request.user
    #    return super().form_valid(form)

def devices_by_tag(request, slug):
    tags = Tag.objects.filter(slug=slug).values_list('name', flat=True)
    devices = Device.objects.filter(tags__name__in=tags)

    return render(request, 'devicesbytag.html', { 'devices': devices,'tags':tags.first})
