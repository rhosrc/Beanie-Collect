# Generated by Django 4.0.2 on 2022-02-26 23:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0003_maintenance'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='maintenance',
            options={'ordering': ('-date', 'look_over')},
        ),
        migrations.AddField(
            model_name='beanie',
            name='accessories',
            field=models.ManyToManyField(to='main_app.Accessory'),
        ),
    ]