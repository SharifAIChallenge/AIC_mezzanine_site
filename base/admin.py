# -*- coding: utf-8 -*-
from base.models import Team, Submit, TeamInvitation, Member
from django.contrib import admin
from django.conf import settings

admin_models = [Submit]
if settings.DEBUG:
    admin_models += [TeamInvitation]

list(map(admin.site.register, admin_models))


class MemberAdmin(admin.ModelAdmin):
    list_display = ('username', 'first_name', 'last_name', 'team', 'is_active')
    fields = (
        ('first_name', 'last_name', 'avatar'),
        ('username', 'email', 'phone_number'),
        ('password',),
        ('country', 'education_place'),
        ('team',),
        ('is_active', 'is_staff', 'is_superuser'),
        ('date_joined', 'last_login'),
    )

admin.site.unregister(Member)
admin.site.register(Member, MemberAdmin)


class MembersInline(admin.TabularInline):
    model = Member
    extra = 1


class TeamAdmin(admin.ModelAdmin):
    list_display = ('name', 'competition', 'head')
    fields = (
        ('name', 'head'),
        ('competition',),
        ('timestamp',),
    )
    inlines = [MembersInline]


admin.site.register(Team, TeamAdmin)
