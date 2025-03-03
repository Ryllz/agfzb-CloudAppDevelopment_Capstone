from django.contrib import admin
from .models import CarModel, CarMake

# CarModelInline class
class CarModelInline(admin.StackedInline):
    model = CarModel
    extra = 5

# CarModelAdmin class
class CarModelAdmin(admin.ModelAdmin):
        fields = ['manufacturer', 'name', 'dealer_id','car_type','year']

# CarMakeAdmin class with CarModelInline
class CarMakeAdmin(admin.ModelAdmin):
        fields = ['name', 'desc']
        inlines = [CarModelInline]

# Register models here
admin.site.register(CarModel, CarModelAdmin)
admin.site.register(CarMake, CarMakeAdmin)