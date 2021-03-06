# Generated by Django 2.1.5 on 2019-04-23 21:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('category', models.CharField(choices=[('Software_Development', 'Software_Development'), ('Reference', 'Reference'), ('Entertainment', 'Entertainment'), ('Social', 'Social'), ('Unknown', 'Unknown')], max_length=200)),
                ('start_time', models.DateTimeField()),
                ('end_time', models.DateTimeField()),
                ('is_finished', models.BooleanField(default=False)),
                ('user', models.ForeignKey(default=None, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('process_name', models.CharField(max_length=200)),
                ('ip_addr', models.GenericIPAddressField()),
                ('update_time', models.DateTimeField()),
                ('create_time', models.DateTimeField()),
                ('type', models.CharField(max_length=50)),
                ('username', models.CharField(max_length=50)),
            ],
        ),
    ]
