# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import mezzanine.core.fields
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0004_auto_20151219_1737'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AskedQuestion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('_order', mezzanine.core.fields.OrderField(null=True, verbose_name='Order')),
                ('creation_time', models.DateTimeField(auto_now_add=True, verbose_name='Creation Time')),
                ('question', models.CharField(help_text='Ask New Question', max_length=1024, verbose_name='Question')),
                ('question_fa', models.CharField(help_text='Ask New Question', max_length=1024, null=True, verbose_name='Question')),
                ('question_en', models.CharField(help_text='Ask New Question', max_length=1024, null=True, verbose_name='Question')),
                ('answer', models.CharField(max_length=4096, null=True, verbose_name='Answer', blank=True)),
                ('answer_fa', models.CharField(max_length=4096, null=True, verbose_name='Answer', blank=True)),
                ('answer_en', models.CharField(max_length=4096, null=True, verbose_name='Answer', blank=True)),
                ('is_approved', models.BooleanField(default=True, verbose_name='Approved')),
            ],
            options={
                'ordering': ('_order',),
                'verbose_name': 'Asked Question',
                'verbose_name_plural': 'Asked Questions',
            },
        ),
        migrations.CreateModel(
            name='ContainerPage',
            fields=[
                ('page_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='pages.Page')),
            ],
            options={
                'ordering': ('_order',),
                'verbose_name': 'Container Page',
                'verbose_name_plural': 'Container Pages',
            },
            bases=('pages.page',),
        ),
        migrations.CreateModel(
            name='QAPage',
            fields=[
                ('page_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='pages.Page')),
                ('content', mezzanine.core.fields.RichTextField(verbose_name='Content')),
                ('content_fa', mezzanine.core.fields.RichTextField(null=True, verbose_name='Content')),
                ('content_en', mezzanine.core.fields.RichTextField(null=True, verbose_name='Content')),
                ('responder_mail', models.EmailField(max_length=2014, null=True, verbose_name='Responder Mail', blank=True)),
            ],
            options={
                'ordering': ('_order',),
                'verbose_name': 'QA Page',
                'verbose_name_plural': 'QA Pages',
            },
            bases=('pages.page', models.Model),
        ),
        migrations.AddField(
            model_name='askedquestion',
            name='page',
            field=models.ForeignKey(verbose_name='Containing Page', to='custom_pages.QAPage'),
        ),
        migrations.AddField(
            model_name='askedquestion',
            name='questioner',
            field=models.ForeignKey(verbose_name='Questioner', to=settings.AUTH_USER_MODEL),
        ),
    ]
