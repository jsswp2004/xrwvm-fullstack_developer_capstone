from django.contrib import admin
from .models import CarMake, CarModel
# from .models import related models


# Register your models here.
# Registering models with their respective admins
admin.site.register(CarMake)
admin.site.register(CarModel)

# CarModelInline class

# CarModelAdmin class

# CarMakeAdmin class with CarModelInline

# Register models here
