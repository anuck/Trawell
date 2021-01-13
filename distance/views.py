from django.shortcuts import render, get_object_or_404
from .models import Distance
from .forms import MeasurementModelForm
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
from .utils import get_geo,get_center_coordinates, get_zoom, get_ip_address
import folium

# Create your views here.


def calculate_distance_view(request):
    #initial values
    distance_output = None
    destination = None
    error = None
    obj = get_object_or_404(Distance, id=1)
    form = MeasurementModelForm(request.POST or None)
    geoLocator = Nominatim(user_agent='distance')
    
    ip = '142.117.139.119'
    ip_ = get_ip_address(request)
    print(ip_)
    country, city, lat, lon = get_geo(ip)  
    #print('location country', country)
    #print('location city', city)
    print('location latitude', lat)
    print('location longitute', lon)

    location = geoLocator.geocode(city)
    print('location', location)

    # location co-ordinates
    l_lat = lat
    l_lon = lon 
    pointA = (l_lat,l_lon)

    #intial folium map
    m = folium.Map(width = 800, height = 500, location=get_center_coordinates(l_lat,l_lon), zoom_start=8 )
    
    #location marker
    folium.Marker([l_lat,l_lon], tooltip = 'click here for more', popup =city['city'],
                    icon= folium.Icon(color='purple')).add_to(m)

    if form.is_valid():
        instance = form.save(commit=False)
        destination_ = form.cleaned_data.get('destination')

        try:
            destination = geoLocator.geocode(destination_)
        
            #print(destination)
             
            # destination co-ordinates
            d_lat = destination.latitude
            d_lon = destination.longitude

            pointB = (d_lat,d_lon )

            #distance calculation
            distance_output = round(geodesic(pointA, pointB).km,2)
            
            #map modification
            m = folium.Map(width = 800, height = 500, location=get_center_coordinates(l_lat,l_lon,d_lat,d_lon), zoom_start=get_zoom(distance_output))
        
            #location marker
            folium.Marker([l_lat,l_lon], tooltip = 'click here for more', popup =city['city'],
                        icon= folium.Icon(color='purple')).add_to(m)
            
            #draw the line between the location and destination
            line = folium.PolyLine(locations=[pointA, pointB],weight=5, color='blue')
            m.add_child(line)
            
            #destination marker
            folium.Marker([d_lat,d_lon], tooltip = 'click here for more', popup =destination,
                        icon= folium.Icon(color='red',icon='cloud')).add_to(m)
            instance.location = location
            instance.distance = distance_output
            instance.save()
        except:
            error = "Location not found"
            print(error)

    m = m._repr_html_()
    context = {
        'error':error,
        'distance' : distance_output,
        'form' : form,
        'map' : m,
        'destination' : destination
    }

    return render(request, 'distance/main.html', context)