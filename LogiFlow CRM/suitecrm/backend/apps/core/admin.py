from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import Tenant, User


@admin.register(Tenant)
class TenantAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'plan', 'created_at']
    list_filter = ['plan']
    search_fields = ['name', 'slug', 'cnpj']
    readonly_fields = ['created_at', 'updated_at']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ['username', 'email', 'tenant', 'role', 'is_active']
    list_filter = ['is_active', 'role', 'tenant']
    search_fields = ['username', 'email', 'first_name', 'last_name']
    
    fieldsets = BaseUserAdmin.fieldsets + (
        ('LogiFlow', {'fields': ('tenant', 'role', 'telefone')}),
    )
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('LogiFlow', {'fields': ('tenant', 'role')}),
    )
