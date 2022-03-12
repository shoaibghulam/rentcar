from django.urls import path
from  webapp.views import *
urlpatterns = [
    path('',HomeView.as_view(), name='home'),
    path('register',RegisterView.as_view(), name='register'),
    path('created',CreateView.as_view(), name='created'),
    path('verify/<int:id>/<int:token>',VerifyView.as_view(), name='verify'),
    path('vendorlogin',VendorLoginView.as_view(), name='vendorlogin'),
    path('vendorforget',ForgetPasswordVendor.as_view(), name='vendorforget'),
    path('resetvendor/<int:id>/<int:token>',ResetVendorPassword.as_view(), name='resetvendor'),
    path('vendor',VendorView.as_view(), name='vendor'),
    path('my_listings',MyLestingView.as_view(), name='my_listings'),
    path('my_listings_completed',MyLestingCompletedView.as_view(), name='my_listings_completed'),
    path('my_listings_in_progress',MyLestingInProgressView.as_view(), name='my_listings_in_progress'),
    path('add_listing',AddListingView.as_view(), name='add_listing'),
    path('my_settings',MySettingsView.as_view(), name='my_settings'),
    path('userregister',UserRegisterView.as_view(), name='userregister'),
     path('userverify/<int:id>/<int:token>',UserVerifyView.as_view(), name='verify'),
    path('userlogin',UserLoginView.as_view(), name='userlogin'),
    path('cars_details/<int:id>',CarDetials.as_view(), name='cars_details'),
    path('user_profile',UserProfileView.as_view(), name='cars_details'),
    path('my_trips',UserTripsView.as_view(), name='my_trips'),
    path('my_orders_completed',UserTripsCompletedView.as_view(), name='my_orders_completed'),
    path('my_orders_processing',UserTripsProcessingView.as_view(), name='my_orders_processing'),
    path('order_view/<int:id>',OrderView.as_view(), name='order_view'),
    
    path('trips',VendorTripsView.as_view(), name='trips'),
    path('orders_completed',VendorTripsProcessingView.as_view(), name='orders_processing'),
    path('view_order/<int:id>',VendorOrderView.as_view(), name='view_order'),
    path('reviews',Reviews.as_view(), name='reviews'),
    path('logout',UserLogOut.as_view(), name='logout'),

    # new edition start
    path('vendor_details/<int:id>',VendorDetails.as_view(), name='vendor_details'),
    path('new_orders',VendorNewOrdersView.as_view(), name='new_orders'),
    path('pending_payment',VendorPendingPaymentView.as_view(), name='pending_payment'),
    path('add_review/<int:id>',AddReview.as_view(), name='add_review'),
    path('result',ResultView.as_view(), name='result'),
    path('thank_you',ThankYouUser.as_view(), name='thank_you'),
    path('all_cars',AllCarsview.as_view(), name='all_cars'),
    path('edit_listing/<int:id>',EditListingView.as_view(), name='edit_listing'),
    path('delete_listing/<int:id>',DeleteListingView.as_view(), name='delete_listing'),
    # new edition end
  
]
