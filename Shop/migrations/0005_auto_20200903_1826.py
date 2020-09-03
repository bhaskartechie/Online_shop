# Generated by Django 3.1 on 2020-09-03 12:56

from django.db import migrations
import django_resized.forms


class Migration(migrations.Migration):

    dependencies = [
        ('Shop', '0004_auto_20200903_1824'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='image',
            field=django_resized.forms.ResizedImageField(blank=True, crop=None, force_format='JPEG', keep_meta=True, quality=75, size=[10, 20], upload_to='products/%Y/%m/%d'),
        ),
    ]
