# Generated by Django 2.0.9 on 2018-10-24 07:49

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('status', models.PositiveIntegerField(choices=[(1, 'Pending Analysis'), (2, 'Analysis Complete'), (3, 'Analysis Failed')], default=1)),
                ('is_positive', models.NullBooleanField()),
                ('deleted', models.BooleanField(default=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]