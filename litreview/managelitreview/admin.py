from django.contrib import admin

from .models import Ticket, Review


class TicketAdmin(admin.ModelAdmin):
    list_display = ("title", "user", "time_created")


class ReviewAdmin(admin.ModelAdmin):
    list_display = ("ticket", "user", "rating")


admin.site.register(Ticket, TicketAdmin)
admin.site.register(Review, ReviewAdmin)

