# Generated by Django 3.1 on 2021-03-05 16:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app1', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='user_profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(max_length=200)),
                ('phone_no', models.BigIntegerField()),
                ('dept_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app1.department')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.RemoveField(
            model_name='credential',
            name='permission_id',
        ),
        migrations.RemoveField(
            model_name='faculty',
            name='dept_id',
        ),
        migrations.RemoveField(
            model_name='student',
            name='dept_id',
        ),
        migrations.RemoveField(
            model_name='attendance',
            name='faculty_id',
        ),
        migrations.RemoveField(
            model_name='attendance',
            name='student_id',
        ),
        migrations.AddField(
            model_name='attendance',
            name='user_id',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='auth.user'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='course',
            name='course_string',
            field=models.CharField(default=0, max_length=200),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='course_enrolled',
            name='student_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='session',
            name='faculty_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.DeleteModel(
            name='admin',
        ),
        migrations.DeleteModel(
            name='credential',
        ),
        migrations.DeleteModel(
            name='faculty',
        ),
        migrations.DeleteModel(
            name='permission',
        ),
        migrations.DeleteModel(
            name='student',
        ),
    ]