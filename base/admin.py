# -*- coding: utf-8 -*-
from base.models import Team, Submit, TeamInvitation, Member, JoinRequest, Email, Message, GameRequest
from django.contrib import admin
from import_export import resources, fields
from import_export.admin import ImportExportModelAdmin

admin_models = [TeamInvitation, JoinRequest, Email, Message]

list(map(admin.site.register, admin_models))


class SubmitAdmin(admin.ModelAdmin):
    fieldsets = ((None, {"fields": ("status", "code", "compile_log_file", "team")}),)
    list_display = ("get_team_name", "code", "status", "compile_log_file")
    list_display_links = ()
    list_editable = ()
    list_filter = ()
    search_fields = ()

    def get_team_name(self, submit):
        return submit.team.name


admin.site.register(Submit, SubmitAdmin)


class MemberResource(resources.ModelResource):
    country = fields.Field()

    class Meta:
        model = Member
        fields = (
            'id',
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
            'id',
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
    search_fields = ('username', 'email', 'first_name', 'last_name', 'education_place')
    list_filter = ('is_active',)
    list_display = ('username', 'first_name', 'last_name', 'email', 'country', 'education_place', 'team', 'is_active')
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
    fields = ('username', 'first_name', 'last_name', 'email', 'country')
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
    member1_email = fields.Field()
    member1_country = fields.Field()
    member1_education_place = fields.Field()
    member2 = fields.Field()
    member2_email = fields.Field()
    member2_country = fields.Field()
    member2_education_place = fields.Field()
    head = fields.Field()
    has_successful_submit = fields.Field()

    class Meta:
        model = Team
        fields = (
            'id',
            'name',
            'timestamp',
            'head__email',
            'head__country',
            'head__education_place',
            'final',
            'will_come',
        )
        export_order = (
            'id',
            'name',
            'timestamp',
            'final',
            'head',
            'head__email',
            'head__country',
            'head__education_place',
            'member1',
            'member1_email',
            'member1_country',
            'member1_education_place',
            'member2',
            'member2_email',
            'member2_country',
            'member2_education_place',
            'will_come',
            'has_successful_submit',
        )

    def dehydrate_head(self, team):
        return team.head.get_full_name()

    def dehydrate_member1(self, team):
        members = team.get_members()
        if len(members) > 0:
            return members[0].get_full_name()
        return None

    def dehydrate_member1_email(self, team):
        members = team.get_members()
        if len(members) > 0:
            return members[0].email
        return None

    def dehydrate_member1_country(self, team):
        members = team.get_members()
        if len(members) > 0:
            return members[0].country
        return None

    def dehydrate_member1_education_place(self, team):
        members = team.get_members()
        if len(members) > 0:
            return members[0].education_place
        return None

    def dehydrate_member2(self, team):
        members = team.get_members()
        if len(members) > 1:
            return members[1].get_full_name()
        return None

    def dehydrate_member2_email(self, team):
        members = team.get_members()
        if len(members) > 0:
            return members[0].email
        return None

    def dehydrate_member2_country(self, team):
        members = team.get_members()
        if len(members) > 0:
            return members[0].country
        return None

    def dehydrate_member2_education_place(self, team):
        members = team.get_members()
        if len(members) > 0:
            return members[0].education_place
        return None

    def dehydrate_has_successful_submit(self, team):
        return team.submit_set.filter(status=2).exists()


class TeamAdmin(ImportExportModelAdmin):
    resource_class = TeamResource
    search_fields = ('name',)
    list_filter = ('final', 'show', 'will_come', 'head__country')
    list_display = ('name', 'competition', 'head', 'countries', 'show', 'final', 'will_come')
    fields = (
        ('name', 'head', 'show'),
        ('competition', 'final'),
        ('will_come',),
    )
    inlines = [MembersInline]

    def countries(self, obj):
        members = obj.member_set.all()
        return ",".join(list(set([str(member.country.name) for member in members])))


admin.site.register(Team, TeamAdmin)


@admin.register(GameRequest)
class GameRequestAdmin(admin.ModelAdmin):
    list_display = ('requester', 'requestee', 'accepted', 'accept_time')
