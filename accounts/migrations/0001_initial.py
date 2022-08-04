# Generated by Django 3.2.13 on 2022-07-27 02:55

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='InstallerUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('email', models.EmailField(max_length=255, unique=True)),
                ('first_name', models.CharField(blank=True, max_length=150)),
                ('last_name', models.CharField(blank=True, max_length=150)),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('phone', models.CharField(max_length=255, null=True)),
                ('street', models.CharField(max_length=120, null=True)),
                ('city', models.CharField(max_length=120, null=True)),
                ('postcode', models.IntegerField(null=True)),
                ('state', models.CharField(max_length=120, null=True)),
                ('country', models.CharField(max_length=120, null=True)),
                ('is_installer', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name': 'InstallerUser',
                'verbose_name_plural': 'InstallerUsers',
            },
        ),
        migrations.CreateModel(
            name='InstallerToken',
            fields=[
                ('key', models.CharField(max_length=40, primary_key=True, serialize=False, verbose_name='Key')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='installertokens', to='accounts.installeruser', verbose_name='InstallerUserToken')),
            ],
            options={
                'verbose_name': 'InstallerToken',
                'verbose_name_plural': 'InstallerTokens',
            },
        ),
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('email', models.EmailField(max_length=255, unique=True)),
                ('first_name', models.CharField(blank=True, max_length=150)),
                ('last_name', models.CharField(default='lastname', max_length=150)),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.')),
                ('is_superuser', models.BooleanField(default=False)),
                ('is_customer', models.BooleanField(default=True)),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('customer_crm_id', models.CharField(blank=True, max_length=255, null=True, unique=True)),
                ('phone', models.CharField(blank=True, max_length=255)),
                ('street', models.CharField(blank=True, max_length=120)),
                ('city', models.CharField(blank=True, max_length=120)),
                ('postcode', models.CharField(blank=True, max_length=120)),
                ('state', models.CharField(blank=True, max_length=120)),
                ('country', models.CharField(blank=True, max_length=120)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'CustomUser',
                'verbose_name_plural': 'CustomUsers',
            },
        ),
    ]
