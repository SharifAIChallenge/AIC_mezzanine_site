from django.core.urlresolvers import reverse
from django.utils.safestring import mark_safe


# http://stackoverflow.com/questions/9919780/how-do-i-add-a-link-from-the-django-admin-page-of-one-object-to-the-admin-page-o
def add_link_field(target_model=None, field='', link_text=unicode):
    def add_link(cls):
        reverse_name = target_model or cls.model.__name__.lower()

        def link(self, instance):
            app_name = instance._meta.app_label
            reverse_path = "admin:%s_%s_change" % (app_name, reverse_name)
            link_obj = getattr(instance, field, None)
            if link_obj:
                url = reverse(reverse_path, args=(link_obj.id,))
                return mark_safe("<a href='%s'>%s</a>" % (url, link_text(link_obj)))
            return "(None)"

        field_name = field + '_link'
        link.allow_tags = True
        link.short_description = field_name
        link.func_name = field_name
        setattr(cls, field_name, link)

        list_display = list(getattr(cls, 'list_display', []))
        try:
            indx = list_display.index(field)
            list_display[indx] = field_name
        except ValueError:
            pass
        cls.list_display = list_display

        return cls

    return add_link
