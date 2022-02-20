from django.contrib import admin
from .models import *
# Register your models here.

class OrderAdmin(admin.ModelAdmin):
    
    list_display=(
        'OrderId',
        'firstName',
        'lastName',
        'contactNo',
        'Pickup',
        'Return',
        'checkIn',
        'checkOut',
        'BookDateandtime',
        'bookBy',
        'car',
        'returnCar',
        'totalPrice',
        'status'
    )

class CarsAdmin(admin.ModelAdmin):
    
    list_display=(
        'carId',
        'status',
        'carType',
        'noOfSeats',
        'gearBox',
        'fuel',
        'price',
        'listingTitle',
        'vendorId',
    )

class ReviewAdmin(admin.ModelAdmin):
    
    list_display=(
        'reviewId',
        'firstName',
        'lastName',
        'orderid',
        'stars',
        'description',
        'date'
    )

class CityAdmin(admin.ModelAdmin):
    
    list_display=(
        'cityId',
        'cityName',
       
    )


admin.site.register(VendorModel)
admin.site.register(CarsModel,CarsAdmin)
admin.site.register(AmenitiesModel)
admin.site.register(UserModel)
admin.site.register(OrdersModel,OrderAdmin)
admin.site.register(ReviewsModel,ReviewAdmin)
admin.site.register(CityModels,CityAdmin)