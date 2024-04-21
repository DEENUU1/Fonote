from django.contrib import admin

from .models.contact import Contact


class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'is_read')
    list_filter = ('is_read',)
    list_editable = ('is_read',)


admin.site.register(Contact, ContactAdmin)
