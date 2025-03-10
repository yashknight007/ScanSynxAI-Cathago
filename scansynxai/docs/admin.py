from django.contrib import admin
from .models import CreditRequest, UserProfile

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'credits')
    search_fields = ('user__username',)
    list_filter = ('credits',)

admin.site.register(UserProfile, ProfileAdmin)

class CreditRequestAdmin(admin.ModelAdmin):
    list_display = ("user", "requested_credits", "status", "created_at", "approved_at")
    list_filter = ("status", "created_at")
    actions = ["approve_requests", "deny_requests"]

    def approve_requests(self, request, queryset):
        for credit_request in queryset:
            credit_request.approve()
        self.message_user(request, "Selected requests have been approved.")

    def deny_requests(self, request, queryset):
        for credit_request in queryset:
            credit_request.deny()
        self.message_user(request, "Selected requests have been denied.")

    approve_requests.short_description = "Approve selected credit requests"
    deny_requests.short_description = "Deny selected credit requests"

admin.site.register(CreditRequest, CreditRequestAdmin)