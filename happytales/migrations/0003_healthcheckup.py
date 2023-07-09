# Generated by Django 3.2.4 on 2023-07-09 20:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('happytales', '0002_auto_20230710_0056'),
    ]

    operations = [
        migrations.CreateModel(
            name='HealthCheckup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('weight', models.DecimalField(decimal_places=2, max_digits=5)),
                ('temperature', models.DecimalField(decimal_places=2, max_digits=4)),
                ('notes', models.TextField()),
                ('pet', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='happytales.pet')),
            ],
        ),
    ]
