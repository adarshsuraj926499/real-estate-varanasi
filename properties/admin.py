from django.contrib import admin
from django.utils.html import format_html
from django.utils.text import Truncator
from .models import Enquiry, Property, PropertyMedia

class PropertyMediaInline(admin.TabularInline):
    model = PropertyMedia
    extra = 1
    fields = ("file", "media_type", "caption", "is_cover", "order")

@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ("title", "kind", "price", "location", "is_published", "is_featured", "created_at")
    list_filter = ("kind", "is_published", "is_featured")
    search_fields = ("title", "location", "description")
    list_editable = ("is_published", "is_featured")
    prepopulated_fields = {"slug": ("title",)}
    inlines = (PropertyMediaInline,)
    save_on_top = True

@admin.register(Enquiry)
class EnquiryAdmin(admin.ModelAdmin):
    list_display = ("name", "phone", "email", "property_summary", "message_preview", "status", "created_at")
    list_filter = ("status", "created_at", "property__kind")
    search_fields = ("name", "phone", "email", "property__title")
    list_editable = ("status",)
    readonly_fields = ("created_at",)
    list_per_page = 20
    date_hierarchy = "created_at"
    fieldsets = (("Customer", {"fields": ("property", "name", "phone", "email", "message")}),
                 ("Follow-up", {"fields": ("status", "admin_notes", "created_at")}))

    class Media:
        css = {"all": ("css/admin.css",)}

    @admin.display(description="Property / enquiry", ordering="property__title")
    def property_summary(self, obj):
        return obj.property.title if obj.property else "General enquiry"

    @admin.display(description="Message")
    def message_preview(self, obj):
        return Truncator(obj.message or "—").chars(72)

admin.site.site_header = "GhatNiva Properties Admin"
admin.site.site_title = "GhatNiva Admin"
admin.site.index_title = "Property and enquiry management"
