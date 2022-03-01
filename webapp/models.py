from django.db import models
USER_STATUS = [
    ('enable', 'enable'),
    ('disable', 'disable'),
    
]
CAR_STATUS = [
    ('In Progress', 'In Progress'),
    ('Completed', 'Completed'),
    
]

BOOK_STATUS = [
    ('Processing', 'Processing'),
    ('Pending payment', 'Pending payment'),
    ('Completed', 'Completed'),
    ('Cancel', 'Cancel'),
    
]
# Create your models here.

class CityModels(models.Model):
    cityId=models.AutoField(primary_key=True)
    cityName=models.CharField(max_length=255)
    def __str__(self):
        return self.cityName


class VendorModel(models.Model):
    id=models.AutoField(primary_key=True)
    firstName=models.CharField(max_length=250)
    lastName=models.CharField(max_length=250)
    companyName=models.CharField(max_length=250)
    contactNo=models.CharField(max_length=250)
    address=models.CharField(max_length=250,blank=True)
    city=models.ForeignKey(CityModels, on_delete=models.CASCADE , null=True , blank=True)
    email=models.CharField(max_length=250)
    password=models.TextField(max_length=3000)
    description=models.TextField(max_length=3000,default="", blank=True)
    profile=models.ImageField(upload_to="profile/", default="profile/default_avatar.jpg")
    status=models.CharField(max_length=50, default="disable")
    token=models.CharField(max_length=200)
    def __str__(self):
        return self.email

class AmenitiesModel(models.Model):
    id=models.AutoField(primary_key=True)
    title=models.CharField(max_length=250)
    def __str__(self):
        return self.title

class CarsModel(models.Model):
    carId=models.AutoField(primary_key=True)
    carType=models.CharField(max_length=100)
    noOfSeats=models.IntegerField()
    gearBox=models.CharField(max_length=250)
    fuel=models.CharField(max_length=250)
    amenities=models.ManyToManyField(AmenitiesModel , null=True)
    photo1=models.ImageField(upload_to="cars/")
    photo2=models.ImageField(upload_to="cars/")
    photo3=models.ImageField(upload_to="cars/")
    city=models.CharField(max_length=250, default="null")
    address=models.TextField(max_length=1000, default="null")
    price=models.FloatField()
    cleaningFee=models.FloatField()
    listingTitle=models.CharField(max_length=250)
    listingDescription=models.TextField(max_length=3000)
    rules=models.TextField(max_length=3000)
    checkIn=models.CharField(max_length=250)
    checkOut=models.CharField(max_length=250)
    rentalPeriod=models.CharField(max_length=250)
    vendorId=models.ForeignKey(VendorModel, on_delete=models.CASCADE)
    status=models.TextField(max_length=200,choices=CAR_STATUS,default="In Progress")
    # trydata=models.TextField(max_length=200, default="null")
    def __str__(self):
        return self.listingTitle



class UserModel(models.Model):
    id=models.AutoField(primary_key=True)
    firstName=models.CharField(max_length=255)
    lastName=models.CharField(max_length=255)
    email=models.CharField(max_length=255)
    contactNo=models.CharField(max_length=255)
    password=models.TextField(max_length=2255)
    DOB=models.CharField(max_length=255)
    token=models.CharField(max_length=255 , default="")
    profile=models.ImageField(upload_to="profile/", default="profile/default_avatar.jpg")
    status=models.CharField(max_length=50, default="disable")
    def __str__(self):
        return self.email 

class OrdersModel(models.Model):
    OrderId=models.AutoField(primary_key=True)
    firstName=models.CharField(max_length=550,default="")
    lastName=models.CharField(max_length=550,default="")
    contactNo=models.CharField(max_length=550,default="")
    email=models.CharField(max_length=550,default="")
    Pickup=models.TextField(max_length=550,default="")
    Return=models.TextField(max_length=550,default="")
    checkIn=models.CharField(max_length=250,default="")
    checkOut=models.CharField(max_length=250,default="")
    BookDateandtime=models.DateTimeField(auto_now_add=True)
    car=models.ForeignKey(CarsModel , on_delete=models.CASCADE ,default="")
    returnCar=models.CharField(max_length=10,default="No")
    totalPrice=models.FloatField()
    bookBy=models.ForeignKey(UserModel , on_delete=models.CASCADE , blank=True, null=True)
    status=models.CharField(max_length=100, choices=BOOK_STATUS, default="Processing")
    def __str__(self):
        return str(self.OrderId)


class ReviewsModel(models.Model):
    reviewId=models.AutoField(primary_key=True)
    firstName=models.CharField(max_length=550,default="")
    lastName=models.CharField(max_length=550,default="")
    orderid=models.ForeignKey(OrdersModel , on_delete=models.CASCADE, blank=True , default="")
    stars=models.IntegerField(default=0)
    description=models.TextField(max_length=1500)
    date=models.DateField(auto_now_add=True)
    status=models.CharField(max_length=100,default="No")
    def __str__(self):
        return str(self.reviewId)
