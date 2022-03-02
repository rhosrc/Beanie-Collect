from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Beanie, Accessory, Photo
from .forms import MaintenanceForm

import boto3
import uuid

S3_BASE_URL = 'https://s3.us-east-1.amazonaws.com/'
BUCKET = 'katkollect'

# Create your views here.

def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def beanies_index(request):
    beanies = Beanie.objects.all()
    return render(request, 'beanies/index.html', {'beanies': beanies})

def beanies_detail(request, beanie_id):
    beanie = Beanie.objects.get(id=beanie_id)
    maintenance_form = MaintenanceForm()
    
    missing_accessories = Accessory.objects.exclude(id__in = beanie.accessories.all().values_list('id'))

    return render(request, 'beanies/detail.html', {
        'beanie': beanie,
        'maintenance_form': maintenance_form,
        'accessories': missing_accessories
    })

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

def assoc_accessory(request, beanie_id, accessory_id):
    Beanie.objects.get(id=beanie_id).accessories.add(accessory_id)
    return redirect('detail', beanie_id=beanie_id)

def dissoc_accessory(request, beanie_id, accessory_id):
    Beanie.objects.get(id=beanie_id).accessories.remove(accessory_id)
    return redirect('detail', beanie_id=beanie_id)

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
    return redirect('detail', beanie_id=beanie_id)


def accessories_index(request):
    accessories = Accessory.objects.all()
    return render(request, 'accessories/index.html', {'accessories': accessories})

def accessories_detail(request, accessory_id):
    accessory = Accessory.objects.get(id=accessory_id)
    return render(request, 'accessories/detail.html', {'accessory': accessory})


class BeanieCreate(CreateView):
    model = Beanie
    fields = ('name', 'animal', 'description', 'date_acquired')

class BeanieUpdate(UpdateView):
    model = Beanie
    fields = ('name', 'animal', 'description', 'date_acquired')

class BeanieDelete(DeleteView):
    model = Beanie
    success_url = '/beanies/'

class AccessoryCreate(CreateView):
    model = Accessory
    fields = '__all__'

class AccessoryUpdate(UpdateView):
    model = Accessory
    fields = ('name', 'color')

class AccessoryDelete(DeleteView):
    model = Accessory
    success_url = '/accessories'

