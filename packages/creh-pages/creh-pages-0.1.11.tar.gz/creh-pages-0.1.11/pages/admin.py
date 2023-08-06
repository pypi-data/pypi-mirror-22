from django.contrib import admin

from pages.models.page import Page, SEOTag, PageTag
from pages.utils.constants import PAGE_CUSTOM_ADMIN
from pages.models.slider import Slider, SliderContent, SliderItem, SliderContentType


class SEOTagAdmin(admin.ModelAdmin):
    model = SEOTag
    list_display = ('title', 'description', 'url', 'keywords')


class PageTagInline(admin.TabularInline):
    model = PageTag
    extra = 3


class PageAdmin(admin.ModelAdmin):
    list_display = ['title', 'external_url', 'is_active', 'created']
    exclude = ['created', 'updated']
    search_fields = ('title', )
    inlines = (PageTagInline, )


class SliderAdmin(admin.ModelAdmin):
    list_display = ['title', 'is_active', 'created']
    list_filter = ['page', 'is_active']
    exclude = ['created', 'updated']
    search_fields = ('title', )


class SliderItemAdmin(admin.ModelAdmin):
    list_display = ['slider', 'active_from', 'active_to', 'is_active', 'created']
    exclude = ['created', 'updated']
    list_filter = ['slider', 'is_active']


class SliderContentTypeAdmin(admin.ModelAdmin):
    list_display = ['name']


class SliderContentAdmin(admin.ModelAdmin):
    list_display = ['order', 'type_content']


if not PAGE_CUSTOM_ADMIN:
    admin.site.register(Page, PageAdmin)

admin.site.register(Slider, SliderAdmin)
admin.site.register(SliderItem, SliderItemAdmin)
admin.site.register(SliderContent, SliderContentAdmin)
admin.site.register(SliderContentType, SliderContentTypeAdmin)
admin.site.register(SEOTag, SEOTagAdmin)
