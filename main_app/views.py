from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Beanie, Accessory, Photo
from .forms import MaintenanceForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

import boto3
import uuid

S3_BASE_URL = 'https://s3.us-east-1.amazonaws.com/'
BUCKET = 'katkollect'

# Create your views here.

def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

@login_required
def beanies_index(request):
    beanies = Beanie.objects.filter(user=request.user)
    return render(request, 'beanies/index.html', {'beanies': beanies})

@login_required
def beanies_detail(request, beanie_id):
    beanie = Beanie.objects.get(id=beanie_id)
    maintenance_form = MaintenanceForm()
    
    missing_accessories = Accessory.objects.exclude(id__in = beanie.accessories.all().values_list('id'))

    return render(request, 'beanies/detail.html', {
        'beanie': beanie,
        'maintenance_form': maintenance_form,
        'accessories': missing_accessories
    })


@login_required
def add_maintenance(request, beanie_id):
    # 1) collect form input values
    form = MaintenanceForm(request.POST)
    # 2) validate input values
    if form.is_valid():
    # 3) save a copy of a maintenance instance in memory
        new_look_over = form.save(commit=False)
    # 4) attach a reference to the beanie baby that needs care
        new_look_over.beanie_id = beanie_id
    # 5) save the new look-over/maintenance  to the database
        new_look_over.save()
    # 6) redirect the user back to the beanie baby detail page
    return redirect('detail', beanie_id=beanie_id)

@login_required
def assoc_accessory(request, beanie_id, accessory_id):
    Beanie.objects.get(id=beanie_id).accessories.add(accessory_id)
    return redirect('detail', beanie_id=beanie_id)

@login_required
def dissoc_accessory(request, beanie_id, accessory_id):
    Beanie.objects.get(id=beanie_id).accessories.remove(accessory_id)
    return redirect('detail', beanie_id=beanie_id)

@login_required
def add_photo(request, beanie_id):
    # attempt to collect the photo information from the form submission
    photo_file = request.FILES.get('photo-file')
    '''
    <input type="file" name="photo-file" 
    
    '''
    # use an if statement to see if the photo information is present or not
    # if photo is present
    if photo_file:
        # initialize a reference to the S3 service from boto3
        s3 = boto3.client('s3')
        # create a unique name for the photo asset
        key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
        '''
        EXAMPLE CHANGE:
        beanie_boo.jpg => whra7o.png
        '''
        # attempt to upload the photo asset to AWS S3 
        try:
            s3.upload_fileobj(photo_file, BUCKET, key)
            url = f'{S3_BASE_URL}{BUCKET}/{key}'
            photo = Photo(url=url, beanie_id=beanie_id)
            # save a secure URL for the AWS-hosted photo asset to the database
            photo.save()
        # if upload is NOT successful
        # print errors to the console
        except Exception as error:
            print('*********************')
            print('An error occurred while uploading to S3')
            print(error)
            print('*********************')
        # return response as a redirect to the client - redirects to the detail page
    return redirect('gallery', beanie_id=beanie_id)

@login_required
def photo_delete(request, beanie_id, photo_id):
    Photo.objects.get(id=photo_id).delete()
    return redirect('gallery', beanie_id=beanie_id)

@login_required
def accessories_index(request):
    accessories = Accessory.objects.all()
    return render(request, 'accessories/index.html', {'accessories': accessories})

@login_required
def accessories_detail(request, accessory_id):
    accessory = Accessory.objects.get(id=accessory_id)
    return render(request, 'accessories/detail.html', {'accessory': accessory})

@login_required
def beanie_gallery(request, beanie_id):
    beanie = Beanie.objects.get(id=beanie_id)
    return render(request, 'beanies/gallery.html', {
        'beanie': beanie,
    })

def signup(request):
    # we'll need this for our context dictionary, in case there are no errors
    error_message = ''
    # check for a POST request (as opposed to a GET request)
    if request.method == 'POST':
        # capture form inputs
        form = UserCreationForm(request.POST)
        # validate form inputs (make sure everything we need is there)
        if form.is_valid():
            # save the new user to the database
            user = form.save()
            # log the new user in
            login(request, user)
            # redirect to the Beanie Babies index page
            return redirect('index')
        # if form is NOT valid
        else:
            error_message = 'invalid sign up - please try again'
            # redirect to signup page (/accounts/signup) and display error message
    # If GET request
        # render a signup page with a blank user creation form
    form = UserCreationForm()  
    context = {
        'form': form,
        'error': error_message
    }    
    return render(request, 'registration/signup.html', context)


class BeanieCreate(LoginRequiredMixin, CreateView):
    model = Beanie
    fields = ('name', 'animal', 'description', 'date_acquired')
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class BeanieUpdate(LoginRequiredMixin, UpdateView):
    model = Beanie
    fields = ('name', 'animal', 'description', 'date_acquired')

class BeanieDelete(LoginRequiredMixin, DeleteView):
    model = Beanie
    success_url = '/beanies/'

class AccessoryCreate(LoginRequiredMixin, CreateView):
    model = Accessory
    fields = '__all__'

class AccessoryUpdate(LoginRequiredMixin, UpdateView):
    model = Accessory
    fields = ('name', 'color')

class AccessoryDelete(LoginRequiredMixin, DeleteView):
    model = Accessory
    success_url = '/accessories'


