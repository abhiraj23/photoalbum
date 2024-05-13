from django.contrib import admin

from .models import Photo, Category



class PhotoModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'image', 'description', 'category']
    
 
class CategoryModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'name']   


admin.site.register(Photo, PhotoModelAdmin)
admin.site.register(Category, CategoryModelAdmin)