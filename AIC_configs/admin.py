from copy import deepcopy

from django.contrib import admin

from mezzanine.forms.admin import FormAdmin
from mezzanine.forms.models import Form
from mezzanine.galleries.admin import GalleryAdmin
from mezzanine.galleries.models import Gallery
from mezzanine.pages.admin import PageAdmin
from mezzanine.pages.models import RichTextPage


page_fieldsets = deepcopy(PageAdmin.fieldsets)
page_fieldsets[0][1]["fields"].insert(+2, "featured_image")
PageAdmin.fieldsets = page_fieldsets

admin.site.unregister(Form)
admin.site.register(Form, FormAdmin)
# admin.site.unregister(Gallery)
# admin.site.register(Gallery, GalleryAdmin)
admin.site.unregister(RichTextPage)
admin.site.register(RichTextPage, PageAdmin)