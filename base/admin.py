# -*- coding: utf-8 -*-
from base.models import Team, Submit, TeamInvitation, Member, JoinRequest
from django.contrib import admin
from import_export import resources, fields
from import_export.admin import ImportExportModelAdmin

admin_models = [Submit, TeamInvitation, JoinRequest]

list(map(admin.site.register, admin_models))


class MemberResource(resources.ModelResource):
    country = fields.Field()

    class Meta:
        model = Member
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            'phone_number',
            'education_place',
            'date_joined',
            'team__name',
        )
        export_order = (
            'username',
            'first_name',
            'last_name',
            'email',
            'phone_number',
            'country',
            'education_place',
            'date_joined',
            'team__name',
        )

    def dehydrate_country(self, member):
        return member.country.name


class MemberAdmin(ImportExportModelAdmin):
    resource_class = MemberResource
    list_display = ('username', 'first_name', 'last_name', 'country', 'education_place', 'team', 'is_active')
    fields = (
        ('first_name', 'last_name'),
        ('username', 'email', 'phone_number'),
        ('password',),
        ('country', 'education_place'),
        ('team',),
        ('is_active', 'is_staff', 'is_superuser'),
        ('date_joined', 'last_login'),
    )


admin.site.unregister(Member)
admin.site.register(Member, MemberAdmin)


class MembersInline(admin.StackedInline):
    model = Member
    fields = ('username', 'email')
    readonly_fields = fields
    extra = 0

    def get_max_num(self, request, obj=None, **kwargs):
        team = obj
        if team is None:
            return 1000
        else:
            return team.competition.max_members


class TeamResource(resources.ModelResource):
    member1 = fields.Field()
    member2 = fields.Field()
    head = fields.Field()

    class Meta:
        model = Team
        fields = (
            'name',
            'timestamp',
        )
        export_order = (
            'name',
            'timestamp',
            'head',
            'member1',
            'member2',
        )

    def dehydrate_head(self, team):
        return team.head.get_full_name()

    def dehydrate_member1(self, team):
        members = team.get_members()
        if len(members) > 0:
            return members[0].get_full_name()
        return None

    def dehydrate_member2(self, team):
        members = team.get_members()
        if len(members) > 1:
            return members[1].get_full_name()
        return None


class TeamAdmin(ImportExportModelAdmin):
    resource_class = TeamResource
    list_display = ('name', 'competition', 'head', 'show')
    fields = (
        ('name', 'head', 'show'),
        ('competition',),
    )
    inlines = [MembersInline]


admin.site.register(Team, TeamAdmin)
