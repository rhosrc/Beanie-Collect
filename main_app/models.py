from django.db import models
from django.urls import reverse
from datetime import date

LOOK_OVERS = (
    ('B', 'Brushed'),
    ('W', 'Washed'),
    ('M', 'Mended')
)


# Create your models here.

class Accessory(models.Model):
    name = models.CharField(max_length=50)
    color = models.CharField(max_length=20)

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('accessorydetail', kwargs={'accessory_id': self.id})


class Beanie(models.Model):
    name = models.CharField(max_length=100)
    animal = models.CharField(max_length=100)
    description = models.TextField(max_length=250)
    date_acquired = models.DateField()
    accessories = models.ManyToManyField(Accessory)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('detail', kwargs={'beanie_id': self.id})
    
    def cared_for_today(self):
        return self.maintenance_set.filter(date=date.today()).count() >= len(LOOK_OVERS)


class Maintenance(models.Model):
    date = models.DateField('Maintenance Date')
    look_over = models.CharField('To-Do-Item', max_length=1, choices=LOOK_OVERS, default=LOOK_OVERS[0][0])
    beanie = models.ForeignKey(Beanie, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.get_look_over_display()} on {self.date}'
    
    class Meta:
        ordering = ('-date', 'look_over')

class Photo(models.Model):
    url = models.CharField(max_length=200)
    beanie = models.ForeignKey(Beanie, on_delete=models.CASCADE)

    def __str__(self):
        return f'Photo for beanie_id: {self.beanie_id} @{self.url}'