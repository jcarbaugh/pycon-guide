from django.contrib import admin
from .models import Presentation, PyCon, Interest, Calendar


@admin.register(PyCon)
class PyConAdmin(admin.ModelAdmin):
    list_display = ('year', 'location')


@admin.register(Presentation)
class PresentationAdmin(admin.ModelAdmin):
    list_display = ('year', 'title', 'start_time', 'duration_minutes')
    list_display_links = ('title',)
    list_filter = ('pycon', 'duration_minutes', 'category', 'audience')
    readonly_fields = ('duration_minutes',)
    search_fields = ('title',)

    def get_queryset(self, request):
        return Presentation.objects.select_related('pycon')

    def year(self, obj):
        return obj.pycon.year


@admin.register(Interest)
class InterestAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'presentation')

    def get_queryset(self, request):
        return Interest.objects.select_related('user', 'presentation')


@admin.register(Calendar)
class CalendarAdmin(admin.ModelAdmin):
    list_display = ('slug', 'user')

    def get_queryset(self, request):
        return Calendar.objects.select_related('user')
