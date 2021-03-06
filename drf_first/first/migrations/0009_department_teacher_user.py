# Generated by Django 2.0.6 on 2020-10-29 12:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('first', '0008_auto_20201029_2043'),
    ]

    operations = [
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('de_name', models.CharField(max_length=20)),
                ('people_num', models.IntegerField()),
            ],
            options={
                'verbose_name': '部门',
                'verbose_name_plural': '部门',
                'db_table': 'department_drf',
            },
        ),
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('gender', models.SmallIntegerField(choices=[(2, 'other'), (1, 'famale'), (0, 'male')], default=0)),
                ('age', models.IntegerField(null=True)),
                ('department', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='first.Department')),
            ],
            options={
                'verbose_name': '教师',
                'verbose_name_plural': '教师',
                'db_table': 'teacher_brf',
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=20)),
                ('password', models.CharField(max_length=20)),
                ('gender', models.SmallIntegerField(choices=[(0, 'male'), (1, 'famale'), (2, 'other')], default=0)),
            ],
            options={
                'db_table': 'user_brf',
            },
        ),
    ]
