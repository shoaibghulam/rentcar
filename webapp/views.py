from multiprocessing import context
from django.shortcuts import render , HttpResponse , redirect
from django.views import View
import json
from .models import *
from django.db.models import Q
import random 
from django.contrib import messages
from django.core.mail import EmailMultiAlternatives
from django.db.models import Sum

from passlib.hash import django_pbkdf2_sha256 as handler
BASE="http://127.0.0.1:8000/"
def emailverify(subject,to,link,message):

    from_email="komaljan4@gmail.com"
        
        
    html_content = f'''
                <h1 style="text-align:center; font-family: 'Montserrat', sans-serif;">{message}</h1>
                    
                <div style='width:300px; margin:0 auto;'> <a href='{link}' style=" background-color:#0066ff; border: none;  color: white; padding: 15px 32px;  text-align: center; text-decoration: none; display: inline-block; font-size: 16px; margin: 4px 2px; cursor: pointer; font-family: PT Sans, sans-serif;" >click here</a>
            </div>
                '''

    msg = EmailMultiAlternatives(subject, html_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()

class HomeView(View):
    def get(self, request):
        context={
            'title':'The A Rent Car',
            'data':CarsModel.objects.filter(status="Completed")[0:3],
            'city':CityModels.objects.all().order_by('-cityName')
        }
        return render(request,'public/index.html',context)

class RegisterView(View):
    def get(self, request):
        context={
            'title':'Register Vendor',
            'city':CityModels.objects.all().order_by('-cityName'),
        }
        # print(Site.objects.get_current().domain)
        return render(request,'public/register.html',context)
    
    def post(self, request):
       
        email=request.POST['email']
        verifyToken= random.randint(1,5000)
        checkData=VendorModel.objects.filter(email=email)
        if not checkData:
            data=VendorModel(
                firstName=request.POST['firstName'],
                lastName=request.POST['lastName'],
                companyName=request.POST['companyName'],
                contactNo=request.POST['contactNo'],
                city=CityModels.objects.get(pk=request.POST['city']),
                email=email,
                password= handler.hash(request.POST['password']),
                token=verifyToken
            )
            print("my request is",request.POST)
            data.save()
            if data:
                msg="Verify Account"
                link=f"{BASE}verify/{data.pk}/{verifyToken}"
                print(data.email,link,msg)
                emailverify("Verify Account",email,link,msg)
                messages.success(request,"Please Verify Your Account")
            
                return redirect('/created')
        else:
            messages.success(request,"Email Address already exists")
            return redirect('/register')

            
class CreateView(View):
    def get(self, request):
        context={
            'title':'Verify Vendor'
        }
        return render(request , 'public/created.html',context)


class VerifyView(View):
    def get(self, request ,id,token):
        try:
            query=VendorModel.objects.get(pk=id,token=token)
            if query:
                query.token="none"
                query.status="enable"
                query.save()
                messages.success(request,"Your account has been verified")
                return redirect('/vendorlogin')
        except:
             messages.success(request,"Token is expire")
             return redirect('/vendorlogin')


class VendorLoginView(View):
    def get(self, request):
        context={
            'title':'Login Vendor'
        }
        return render(request,'public/vendorlogin.html',context)
    
    def post(self, request):
       
        try:
            email=request.POST['email']
            password=request.POST['password']
            query=VendorModel.objects.get(email=email , status="enable")
            if query and handler.verify(password,query.password):
                request.session['login'] =True
                request.session['id']=query.pk
                request.session['name']=f"{query.firstName} {query.lastName}"
                request.session['userimg']=f"{query.profile.url}"
                return redirect('/vendor')
            else:
                messages.success(request,"Please Enter Correct Email and Password")
                return redirect('vendorlogin')
        except:
            messages.success(request,"Please Enter Correct Email and Password")
            return redirect('vendorlogin')

class ForgetPasswordVendor(View):
    def get(self, request):
        context={
            'title':'Forget Vendor Password'
        }
        return render(request,'public/vendorforget.html',context)
    def post(self, request):
        try:
            verifyToken= random.randint(1,5000)
            email=request.POST['email']
            query=VendorModel.objects.get(email=email)
            query.token=verifyToken
            query.save()
            if query:
                
                msg="Forget Password"
                link=f"{BASE}resetvendor/{query.pk}/{verifyToken}"
                print(query.email,link,msg)
                emailverify("Verify Account",email,link,msg)
                messages.success(request,"Please Check your mail inbox")
            
                return redirect('/vendorlogin')
            else:
                messages.success(request,"Enter correct Email")
                return redirect('/vendorforget')
        except:
            messages.success(request,"Enter correct Email")
            return redirect('/vendorforget')

class ResetVendorPassword(View):
    def get(self, request,id,token):
        try:
            query=VendorModel.objects.get(pk=id)
            if token != int(query.token):
                messages.success(request,"Token Expire")
                return redirect('/vendorlogin')
            context = {
                'title':'Reset Vendor Password',
            }
            return render(request,'public/vendorreset.html',context)
        except:
            return redirect('/')
    
    def post(self, request,id,token):
        query=VendorModel.objects.get(pk=id)
        if token==query.token:
            query.password=handler.hash(request.POST['password'])
            query.token="none"
            query.save()
            messages.success(request,"Your password has been changed.")
            return redirect('/vendorlogin')
        else:
            messages.success(request,"Token Expire")
            return redirect('/vendorlogin')

    

# --------------- Vendor Dashboard
class VendorView(View):
    def get(self, request):
        if request.session.has_key('login'):
            context={
                "title":f"{request.session['name'] } Profile",
                'profile':VendorModel.objects.get(pk=request.session['id']),
            }
            return render(request,'vendor/vendor_profile.html',context)
        else:
            return redirect('/vendorlogin')
    
    def post(self, request):
        if request.session.has_key('login'):
            



            update=VendorModel.objects.get(pk=request.session['id'])
            update.firstName=request.POST['firstName']
            update.lastName=request.POST['lastName']
            update.email=request.POST['email']
            update.companyName=request.POST['companyName']
            update.contactNo=request.POST['contactNo']
            update.address=request.POST['address']
            update.description=request.POST['description']
            
          
            if request.FILES.get('profile'):
                update.profile=request.FILES['profile']
            update.save()
            return redirect('/vendor')


class MyLestingView(View):
    def get(self, request):
        if request.session.has_key('login'):
        #    wooow
           
            context={
                'title':'Car Listing',
                'data':CarsModel.objects.filter(vendorId=request.session['id']),
                   
            }
            return render(request, 'vendor/my_listings.html',context)

class MyLestingCompletedView(View):
    def get(self, request):
        if request.session.has_key('login'):
            context={
                'title':'Car Listing',
                'data':CarsModel.objects.filter(status="Completed")
               
            }
            return render(request, 'vendor/my_listings_completed.html',context)

class MyLestingInProgressView(View):
    
    def get(self, request):
         if request.session.has_key('login'):
            context={
                'title':'Car Listing',
                'data':CarsModel.objects.filter(status="In Progress")
              
            }
            return render(request, 'vendor/my_listings_in_progress.html',context)

class AddListingView(View):
    def get(self, request):
         if request.session.has_key('login'):
           context={
               'title':'Adding Cars',
               'data':AmenitiesModel.objects.all(),
               'city':CityModels.objects.all().order_by('-cityName'),
           }
           return render(request, 'vendor/add_listing.html',context)
    def post(self, request):
        
         if request.session.has_key('login'):
            amenities=request.POST.getlist('amenities')
            amenititesList=AmenitiesModel.objects.filter(id__in=amenities)

            query=CarsModel(
            carType=request.POST['carType'],
            noOfSeats=request.POST['noOfSeats'],
            gearBox=request.POST['gearBox'],
            fuel=request.POST['fuel'],
            
            photo1=request.FILES['photo1'],
            photo2=request.FILES['photo2'],
            photo3=request.FILES['photo3'],
            city=request.POST['city'],
            address=request.POST['address'],
            price=float(request.POST['price']),
            cleaningFee=float(request.POST['cleaningFee']),
            listingTitle=request.POST['listingTitle'],
            listingDescription=request.POST['listingDescription'],
            rules=request.POST['rules'],
            checkIn=request.POST['checkIn'],
            checkOut=request.POST['checkOut'],
            rentalPeriod=request.POST['rentalPeriod'],
            vendorId=VendorModel.objects.get(pk=request.session['id'])
            )
            query.save()
            addinit=CarsModel.objects.get(pk=query.pk)
            for mydata in amenititesList:
                addinit.amenities.add(mydata)
                addinit.save()
            # query.amenities.add(amenititesList)

            return redirect('/my_listings')


class EditListingView(View):
    def get(self, request,id):
         if request.session.has_key('login'):
           context={
               'title':'Adding Cars',
               'data':AmenitiesModel.objects.all(),
               'details':CarsModel.objects.get(pk=id),
               'city':CityModels.objects.all().order_by('-cityName'),
           }
           return render(request, 'vendor/edit_listing.html',context)
    def post(self, request ,id):
        
         if request.session.has_key('login'):
            query=CarsModel.objects.get(pk=1)
            amenities=request.POST.getlist('amenities')
            amenititesList=AmenitiesModel.objects.filter(id__in=amenities)

            print("the number of seats is",)
            query.carType=request.POST['carType']
            query.noOfSeats=request.POST['noOfSeats']
            query.gearBox=request.POST['gearBox']
            query.fuel=request.POST['fuel']
            if request.FILES.get('photo1'):
                query.photo1=request.FILES['photo1']
            
            if request.FILES.get('photo2'):
                query.photo2=request.FILES['photo2']


            if request.FILES.get('photo3'):
                query.photo3=request.FILES['photo3']
            query.city=request.POST['city']
            query.address=request.POST['address']
            query.price=float(request.POST['price'])
            query.cleaningFee=float(request.POST['cleaningFee'])
            query.listingTitle=request.POST['listingTitle']
            query.listingDescription=request.POST['listingDescription']
            query.rules=request.POST['rules']
            query.checkIn=request.POST['checkIn']
            query.checkOut=request.POST['checkOut']
            query.rentalPeriod=request.POST['rentalPeriod']
           
            query.save()
            addinit=CarsModel.objects.get(pk=query.pk)
  # remove all amenitites start
            removeinit=AmenitiesModel.objects.all()
            for rmdata in removeinit:

                addinit.amenities.remove(rmdata)
                addinit.save()
            
            # remove all amenitites end
           
          
            for mydata in amenititesList:

                addinit.amenities.add(mydata)
                addinit.save()
            # query.amenities.add(amenititesList)

            return redirect('/my_listings')


class DeleteListingView(View):
    def get(self, request, id):
        data=CarsModel.objects.get(pk=id)
        data.delete()
        return redirect('/my_listings')
class MySettingsView(View):
    def get(self, request):
        context={
            'title':'My Settings'
        }
        return render(request,'vendor/my_settings.html')
    
    def post(self, request):
        if request.POST['status']=="email":
            emailUpdate=VendorModel.objects.get(pk=request.session['id'])
            emailUpdate.email=request.POST['email']
            emailUpdate.save()
            messages.success(request,"Email Address has been updated")
            return redirect('my_settings')
        elif request.POST['status']=='password':
            passwordUpdate=VendorModel.objects.get(pk=request.session['id'])
            if passwordUpdate and handler.verify(request.POST['oldpassword'], passwordUpdate.password):
                passwordUpdate.password=handler.hash(request.POST['password'])
                passwordUpdate.save()
                messages.success(request,"Password has been updated")
                return redirect('my_settings')
            else:
                 messages.success(request,"Please Enter Correct Password")
                 return redirect('my_settings')
        else:
            return redirect('my_settings')


class UserRegisterView(View):
    def post(self, request):
        firstName=request.POST['firstName']
        lastName=request.POST['lastName']
        email=request.POST['email']
        contactNo=request.POST['contactNo']
        password=handler.hash(request.POST['password'])
        day=request.POST['day']
        month=request.POST['month']
        year=request.POST['year']
        dob=f"{day}-{month}-{year}"
        checkData=UserModel.objects.filter(email=email)
        if not checkData:
            verifyToken=random.randint(1,5000)
            addUser=UserModel(
                firstName=firstName,
                lastName=lastName,
                email=email,
                contactNo=contactNo,
                password=password,
                DOB=dob,
                token=verifyToken
            )
            addUser.save()
            if addUser:
                    msg="Verify Account"
                    link=f"{BASE}userverify/{addUser.pk}/{verifyToken}"
                
                    emailverify("Verify Account",email,link,msg)
                    messages.success(request,"Please Verify Your Account")
            messages.success(request,"Please Verify your Account")
            return redirect('/created')


class UserVerifyView(View):
    def get(self, request ,id,token):
        try:
            query=UserModel.objects.get(pk=id,token=token)
            if query:
                query.token="none"
                query.status="enable"
                query.save()
                messages.success(request,"Your account has been verified")
                return redirect('/')
        except:
             messages.success(request,"Token is expire")
             return redirect('/')



class UserLoginView(View):

    def post(self, request):
       
        try:
            email=request.POST['email']
            password=request.POST['password']
            query=UserModel.objects.get(email=email ,status="enable")
            if query and handler.verify(password,query.password):
                request.session['userlogin'] =True
                request.session['userid']=query.pk
                request.session['username']=f"{query.firstName} {query.lastName}"
                request.session['img']=f"{query.profile.url}"
                return redirect('/user_profile')
               
            else:
                messages.success(request,"Please Enter Correct Email and Password")
                return redirect('/')
        except:
            messages.success(request,"Please Enter Correct Email and Password")
            return redirect('/')



class CarDetials(View):
    def get(self, request,id):
        data=CarsModel.objects.get(pk=id)
        context={
            'title':data.listingTitle,
            'data':data,
            'totalprice':data.price+data.cleaningFee,
            'review':ReviewsModel.objects.filter(orderid__car=id)
        }
        return render(request,'public/property_page.html',context)
    def post(self, request,id):     

            # adding review end
        insertData=OrdersModel(
                firstName=request.POST.get('firstName'),
                lastName=request.POST.get('lastName'),
                contactNo=request.POST.get('contactNo'),
                email=request.POST.get('email'),
                Pickup=request.POST['Pickup'],
                Return=request.POST['Return'],
                checkIn=request.POST['checkIn'],
                checkOut=request.POST['checkOut'],
                bookBy=None if not request.session.has_key('userid') else UserModel.objects.get(pk=request.session['userid']),
                car=CarsModel.objects.get(pk=id),
                returnCar=request.POST.get('returnCar','NO'),
                totalPrice=request.POST['totalprice']
        )
        insertData.save()
        return redirect('/thank_you')

class UserProfileView(View):
    def get(self, request):
        if request.session.has_key('userlogin'):
            data=UserModel.objects.get(pk=request.session['userid'])
            dob=list(data.DOB.split("-"))
        
            context={
                'title':request.session['username']+ ' Profile',
                'profile':UserModel.objects.get(pk=request.session['userid']),
               
            }
        return render(request,'user/user_profile.html',context)
    
    def post(self, request):
        update=UserModel.objects.get(pk=request.session['userid'])
       
        update.firstName=request.POST['firstName']
        update.lastName=request.POST['lastName']
        update.email=request.POST['email']
     
        update.contactNo=request.POST['contactNo']
       
        
        
        if request.FILES.get('profile'):
            update.profile=request.FILES['profile']
        update.save()
        return redirect('/user_profile')


class UserTripsView(View):
    def get(self, request):
        context={
            'title':'My Trips',
            'data':OrdersModel.objects.filter(bookBy=request.session['userid'])
        }
        return render(request,'user/orders.html',context)

class UserTripsCompletedView(View):
    def get(self, request):
        context={
            'title':'My Trips',
            'data':OrdersModel.objects.filter(bookBy=request.session['userid'],status="Completed")
        }
        return render(request,'user/orders_completed.html',context)


class UserTripsProcessingView(View):
    def get(self, request):
        context={
            'title':'My Trips',
            'data':OrdersModel.objects.filter(bookBy=request.session['userid'],status="Processing")
        }
        return render(request,'user/orders_processing.html',context)



class OrderView(View):
    def get(self, request, id):
        if request.session.has_key('userlogin'):
            data=OrdersModel.objects.get(pk=id)
            context={
                'title':'Order Details',
                'data':data,
            }
            return render(request,'user/orders_view.html',context)
    
 





# ------------------------vendor view order

class VendorTripsView(View):
    def get(self, request):
        context={
            'title':'My Trips',
            'data':OrdersModel.objects.filter(car__vendorId=request.session['id']).order_by('-pk')
        }
        return render(request,'vendor/orders.html',context)

class VendorTripsCompletedView(View):
    def get(self, request):
        context={
            'title':'My Trips',
            'data':OrdersModel.objects.filter(car__vendorId=request.session['id'],status="Completed").order_by('-pk')
        }
        return render(request,'vendor/orders_completed.html',context)


class VendorTripsProcessingView(View):
    def get(self, request):
        context={
            'title':'My Trips',
            'data':OrdersModel.objects.filter(car__vendorId=request.session['id'],status="Processing").order_by('-pk')
        }
        return render(request,'vendor/orders_processing.html',context)



class VendorOrderView(View):
    def get(self, request, id):
        if request.session.has_key('login'):
            data=OrdersModel.objects.get(pk=id)
            context={
                'title':'Order Details',
                'data':data,
            }
            return render(request,'vendor/orders_view.html',context)
    
    def post(self, request,id):
        updatestatus=OrdersModel.objects.get(pk=id)
        updatestatus.status=request.POST['status']
        updatestatus.save()
        if  updatestatus.status=="Completed":
            subject="Rent A Car Review"
            to=updatestatus.email
            link=f"http://127.0.0.1:8000/add_review/{updatestatus.pk}"
            message="Hi, <br> Your Trip is Complated your review is very importent for our compnay"
            emailverify(subject,to,link,message)
         

        messages.success(request,"Order Status is Updated")
        return redirect('/new_orders')






class Reviews(View):
    def get(self, request):
        if request.session.has_key('login'):
            print("THE LIST IS",request.session['id'])
            context={
                'title':'Reviews',
                 'review':ReviewsModel.objects.filter(orderid__car__vendorId__id=request.session['id'])
            }
            print(request.session['id'])
            return render(request, 'vendor/reviews.html',context)
            









# -------------------New Edition start-----------------
class VendorDetails(View):
    def get(self, request,id):
        vendorData=VendorModel.objects.get(id=id)
        print("My data is",vendorData.profile)
        context={
            'title':'Vendor Details',
            'vendorData':vendorData,
            'cars':CarsModel.objects.filter(vendorId=id),
            'reviews':ReviewsModel.objects.filter(orderid__car__vendorId__id=id),
        }
        print(context)
        return render(request,'public/vendor_details.html',context)


class VendorNewOrdersView(View):
    def get(self, request):
        if request.session.has_key('login'):
            id=request.session['id']
            complated=OrdersModel.objects.filter(car__vendorId=id, status="Completed")
            cancel=OrdersModel.objects.filter(car__vendorId=id , status="Cancel")
            totalprice=OrdersModel.objects.filter(car__vendorId=id,status="Completed").aggregate(Sum('totalPrice'))
            
            context={
                'title':'New Trips Order',
                'data':OrdersModel.objects.filter(car__vendorId=request.session['id'] , status="Processing").order_by('-pk'),
                'complated':complated.count(),
                'cars':CarsModel.objects.filter(vendorId=id).count(),
                'cancel':cancel.count(),
                'totalprice':totalprice['totalPrice__sum']
            }
            return render(request,'vendor/neworders.html',context)
        else:
            return redirect('/')

class VendorPendingPaymentView(View):
    def get(self, request):
        context={
            'title':'My Trips',
            'data':OrdersModel.objects.filter(car__vendorId=request.session['id'] , status="Pending payment").order_by('-pk')
        }
        return render(request,'vendor/pending_payment.html',context)

# -------------------New Edition end-------------------



class UserLogOut(View):
    def get(self, request):
        if request.session.has_key('login'):
            del request.session['login'] 
            del request.session['id']
            del request.session['name']
            del request.session['userimg']

        if request.session.has_key('userlogin'):
            del request.session['userlogin']
            del request.session['userid']
            del request.session['username']
            del request.session['img']
        return redirect('/')



class AddReview(View):
    def get(self, request ,id):
        checkData=ReviewsModel.objects.filter(orderid=id)
        if not checkData:
            return render(request,'public/add_review.html')
        else:
            return redirect('/')
    
    def post(self, request,id):
        order=OrdersModel.objects.get(pk=id)
        checkData=ReviewsModel.objects.filter(orderid=id)
        if not checkData:
            query=ReviewsModel(
            firstName=order.firstName,
            lastName=order.lastName,
            orderid=order,
            stars=request.POST['stars'],
            description=request.POST['description'],
            status="Yes"
            )
            query.save()
        
        return redirect('/')


class ResultView(View):
    def get(self, request):
        cityname=request.GET.get('city')
       
        context={
            'title':'Search Result',
            'data':CarsModel.objects.filter(Q(city=cityname)).order_by('-pk'),
            'city':CityModels.objects.all().order_by('-cityName')
        }
        return render(request,'public/listing_page.html',context)




class AllCarsview(View):
    def get(self, request):
      
       
        context={
            'title':'Cars',
            'data':CarsModel.objects.all().order_by('-pk'),
            'city':CityModels.objects.all().order_by('-cityName')
        }
        return render(request,'public/listing_page.html',context)





        # new edition start here
class ThankYouUser(View):
    def get(self, request):
        context={
            'title':'Thank You',
        }
        return render(request,'public/thank_you.html',context)
        # new edition start end