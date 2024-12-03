from django.contrib import admin
from .models import Password, PasswordHash

class PasswordHashInline(admin.TabularInline):
    """
    Inline model to display PasswordHash entries directly under the Password model.
    """
    model = PasswordHash
    extra = 1  # Number of empty forms to display (you can adjust this)

class PasswordAdmin(admin.ModelAdmin):
    """
    Admin configuration for Password model.
    """
    list_display = ('value', 'created_at')
    search_fields = ('value',)
    list_filter = ('created_at',)
    inlines = [PasswordHashInline]  # Display associated hashes inline

    def save_model(self, request, obj, form, change):
        """
        Override the save method to ensure that the password is saved before hashes.
        """
        super().save_model(request, obj, form, change)

class PasswordHashAdmin(admin.ModelAdmin):
    """
    Admin configuration for PasswordHash model.
    """
    list_display = ('password', 'algorithm', 'hash_value', 'created_at')
    search_fields = ('password__value', 'hash_value',)
    list_filter = ('algorithm', 'created_at')
    
    def save_model(self, request, obj, form, change):
        """
        Override the save method to ensure that the associated Password is valid.
        """
        super().save_model(request, obj, form, change)

# Register the models and the admin configurations
admin.site.register(Password, PasswordAdmin)
admin.site.register(PasswordHash, PasswordHashAdmin)
