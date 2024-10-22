# Generated by Django 4.2.2 on 2024-07-06 14:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_room_product'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='campus',
            field=models.ForeignKey(blank=True, default=1, on_delete=django.db.models.deletion.CASCADE, to='core.campus'),
        ),
        migrations.AlterField(
            model_name='product',
            name='datePosted',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='status',
            field=models.BooleanField(blank=True, default=True),
        ),
    ]
