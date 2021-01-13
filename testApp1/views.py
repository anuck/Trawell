from django.shortcuts import render
from .models import *
from django.contrib.auth.decorators import login_required
from .filters import DestinationsFilter
import requests
from urllib.parse import urlencode

from django.core.mail import EmailMessage
from django.conf import settings


@login_required
def home(request):
    destination = Destinations.objects.all().order_by("-hits")
    myFilter = DestinationsFilter(request.GET, queryset = destination)
    destination  = myFilter.qs
    context = {
        'destinations' : destination,
        'myFilter' : myFilter
    }
    return render(request,'testApp1/home.html', context)

@login_required
def portfolio(request):
    if request.method == 'GET':
        destination_id = request.GET.get('destination_id')
        values = Destinations.objects.get(id=destination_id)
        hitcount = values.hits
        hitcount = hitcount + 1
        values.hits = hitcount
        values.save()
        
    context = {
        "values":values,
    }
   
    return render(request,'testApp1/portfolio.html', context)


@login_required
def checkout(request):
       
    destination_id = request.GET.get('destination_id')
    values = Destinations.objects.get(id=destination_id)
    price=values.cost
    discount = 0
    discountAmount = 0
    errorMessage = None
        
    if request.method == 'POST':
        couponCode = request.POST.get('Coupon')
        try:
            promoCode = Coupons.objects.get(code=couponCode)
        except:
            print("Coupon does not exist")
            errorMessage = "Coupon does not exist"
        else:
            discount=promoCode.discountPercentage
            print(discount)
            discountAmount=(price*discount)/100
            price=price-discountAmount

    tax=(price * 0.15)
    total=price+tax
    print(total)
    request.session['values_id']= values.id
    request.session['values_name'] = values.name
    request.session['values_country'] = values.country
    request.session['values_package'] = values.package
    request.session['values_basePrice'] = values.cost
    request.session['price'] = price
    request.session['discount'] = discount
    request.session['discountAmount'] = discountAmount
    request.session['tax'] = tax
    request.session['total'] = total
    
    context = {
        "error":errorMessage,
        "values":values,
        "price":price,
        "discount":discount,
        "discountAmount":discountAmount,
        "tax":tax,
        "total":total
         }
    
    return render(request,'testApp1/checkout.html', context)

@login_required
def sendItineraryEmail(request):
    dest_id = request.session['values_id']
    name = request.session['values_name'] 
    country = request.session['values_country'] 
    package =request.session['values_package'] 
    cost=request.session['values_basePrice'] 
    price = request.session['price'] 
    discount = request.session['discount'] 
    discountAmount = request.session['discountAmount']
    tax = request.session['tax']
    total = request.session['total'] 

    print(request.user.username)
    order = Orders(user = request.user.username, destination_id = dest_id, destination_name=name)
    order.save()
   
    if request.method == 'POST':
        email = request.POST.get('email')
        message="Order Placed Successfully\n\n"
        message+="Itinerary : "+name+"-"+country+"\n"
        message+="The Package selected :"+ package+"\n\n"
        message+="Base Price :$"+str(cost)+"\n"
        message+="Discount Percentage : "+str(discount)+"%"+"\n"
        message+="Discount Applied:$"+str(discountAmount)+"\n"
        message+="Total amount before taxes :$"+str(price)+"\n"
        message+="Tax Amount(15%):$"+str(tax)+"\n" 
        message+="Total amount after taxes :$"+str(total)+"\n"

        email_subject = "TraWell Itinerary confirmation"

        email_body = message
        email = EmailMessage(
                email_subject,
                email_body,
                settings.EMAIL_HOST_USER,
                [email],
                )
        email.fail_silently = False
        email.send()

    

    context={
    }
    return render(request,'testApp1/confirm.html', context)
    


@login_required
def nearbylocations(request):
    api_Key = "AIzaSyCWRZPar2BHNZNKEHG4o1kxAJSDZG-BlTc"
    if request.method == 'POST':
        location = request.POST.get('location')
        radius = request.POST.get('radius')
        keywords = request.POST.get('keywords')

        endpoint_geocode = f"https://maps.googleapis.com/maps/api/geocode/json"
        params_geocode = {"address":location,"key":api_Key}
        url_params_geocode  = urlencode(params_geocode)
        url_geocode = f"{endpoint_geocode}?{url_params_geocode}"
        r = requests.get(url_geocode)
        if r.status_code not in range(200,299):
            return{}
        latlng = {}
        try:
            latlng = r.json()['results'][0]['geometry']['location']
        except:
            pass
        lat,lng = latlng.get("lat"),latlng.get("lng")

        places_endpoint = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"

        params_nearby = {
        "key" : api_Key,
        "location" : f"{lat},{lng}",
        "radius" : radius,
        "keyword" : keywords
        }

        params_nearby_encoded = urlencode(params_nearby)
        places_url = f"{places_endpoint}?{params_nearby_encoded}"
        r2 = requests.get(places_url)
        results = r2.json()["results"]
        context = {"results" : results}
        for result in results:
            print(result['name'])
        return render(request,'testApp1/nearby.html', context)
    else:
        context = {}
        return render(request,'testApp1/nearby.html', context)

@login_required
def deals(request):
    context = {}
    return render(request,'testApp1/deals.html', context)
