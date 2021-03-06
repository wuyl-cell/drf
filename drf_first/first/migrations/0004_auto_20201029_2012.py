# Generated by Django 2.0.6 on 2020-10-29 12:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('first', '0003_auto_20201028_2157'),
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
        migrations.RemoveField(
            model_name='teacher',
            name='department',
        ),
        migrations.AlterField(
            model_name='teacher',
            name='gender',
            field=models.SmallIntegerField(choices=[(1, 'famale'), (0, 'male'), (2, 'other')], default=0),
        ),
    ]
