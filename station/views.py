from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.shortcuts import render
from django.urls import reverse
from django.views import View
import folium
import geocoder
from .forms import StationForm
from .models import Station
from geopy.geocoders import Nominatim
from django.templatetags.static import static
from django.utils.text import slugify
from django.urls import reverse
from django.shortcuts import redirect, render
from .models import Product, Commande, Category
from django.core.paginator import Paginator
from django.core.files.storage import default_storage
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from django.conf import settings

from folium.features import CustomIcon

# Create your views here.
@login_required(login_url="/signin")
def home(request):
    return render(request, 'home.html')


def landingpage(request):
    return render(request, 'landingpage.html')


def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password1 = request.POST['password1']
        user = authenticate(username=username, password=password1)
        if user is not None:
            login(request, user)
            username = user.username
            return redirect('home')
        else:
            messages.error(request, "error")
            return redirect('signin')

    return render(request, 'signin.html')


def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        if User.objects.filter(username=username):
            messages.error(request, "username already exist")
            return redirect('signup')

        if User.objects.filter(email=email):
            messages.error(request, "email already exist")
            return redirect('signup')

        if len(username) > 10:
            messages.error(request, "username is to long")
            return redirect('signup')

        if password1 != password2:
            messages.error(request, 'the password is not correct')
            return redirect('signup')

        if not username.isalnum():
            messages.error(request, 'the username should be an alnum')
            return redirect('signup')

        myuser = User.objects.create_user(username, email, password1)
        myuser.save()
        messages.success(request, "sucess")
        return redirect('signin')

        # return redirect('/signin')
    return render(request, 'signup.html')


def signout(request):
    logout(request)
    return redirect('/')


# creation d'un login station
def signinStation(request):
    if request.method == 'POST':
        username = request.POST['username']
        password1 = request.POST['password1']
        user = authenticate(username=username, password=password1)
        if user is not None:
            login(request, user)
            username = user.username
            return redirect('homeStation')
        else:
            messages.error(request, "error")
            return redirect('signinStation')

    return render(request, 'signinStation.html')


def signupStation(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if User.objects.filter(username=username):
            messages.error(request, "username already exist")
            return redirect('signupStation')

        if User.objects.filter(email=email):
            messages.error(request, "email already exist")
            return redirect('signupStation')

        if len(username) > 10:
            messages.error(request, "username is to long")
            return redirect('signupStation')

        if password1 != password2:
            messages.error(request, 'the password is not correct')

        if not username.isalnum():
            messages.error(request, 'the username should be an alnum')
            return redirect('signupStation')

        myuser = User.objects.create_user(username, email, password1)
        myuser.is_staff = 1
        myuser.save()
        messages.success(request, "sucess")
        return redirect('signinStation')

        # return redirect('/signin')
    return render(request, 'signupStation.html')


@login_required(login_url="/signinStation")
def homeStation(request):
    stations = Station.objects.all()
    return render(request, 'homeStation.html', {"stations": stations})


class StationCreate(LoginRequiredMixin, View):
    def get(self, request):
        form = StationForm()
        return render(request, "station_form.html", {"form": form})

    def post(self, request):
        form = StationForm(data=request.POST)

        if form.is_valid():
            form.instance.user = request.user
            form.save()
            return redirect("index")

        return render(request, "station_form.html", {"form": form})



def index(request):
    if request.method == 'POST':
        form = StationForm(request.POST)
        if form.is_valid():
            station = form.save(commit=False)
            station.user = request.user
            station.save()
            return redirect('/')
    else:
        form = StationForm()

    stations = Station.objects.all()

    # Créer une carte avec des marqueurs pour les stations existantes
    m = folium.Map(location=[20, -10], zoom_start=6)
    for station in stations:
        
        
        
        
        # Generate the URL for the station's detail page
        station_url = reverse('station-detail', args=[station.slug])



        folium.Marker(
        location=[station.latitude, station.longitude],
        tooltip=station.nom,
        popup=f'<a href="{station_url}">{station.nom}</a>',
        icon=folium.Icon(icon_color='white', icon='gas-pump', prefix='fa', color='red')  # Utilisation d'une icône de feuille verte
    ).add_to(m)

    # Obtenir la localisation de l'utilisateur connecté
    location = geocoder.ip('me')
    user_lat = None
    user_lng = None

    if location is not None:
       user_lat = location.lat
       user_lng = location.lng

    if user_lat is not None and user_lng is not None:
       folium.Marker([user_lat, user_lng], tooltip='your location').add_to(m)
   

   
   
    m = m._repr_html_()

    context = {
        'form': form,
        'm': m
    }
    return render(request, 'index.html', context)
    


def get_default_location():
    location = geocoder.ip('me')
    if location is not None:
        return str(location)
    return ""


from django.shortcuts import render, get_object_or_404
from .models import Station



def station_detail(request, slug):
    station = get_object_or_404(Station, slug=slug)
    context = {
        'station': station
    }
    return render(request, 'station_detail.html',  context)






@login_required
def add_product(request):
    categories = Category.objects.all()

    if request.method == 'POST':
        # Retrieve other form data
        product_name = request.POST.get('product-name')
        description = request.POST.get('description')
        price = request.POST.get('price')
        product_category_id = int(request.POST.get('product-category'))

        # Get the uploaded image file
        product_image = request.FILES.get('product-image')

        # Get the category object based on the category ID
        product_category = Category.objects.get(id=product_category_id)

        # Create a new Product object
        product = Product(
            title=product_name,
            price=price,
            description=description,
            category=product_category,
            image=product_image,  # Assign the image directly
        )

        # Save the product object to the database
        product.save()

        return redirect('index')

    return render(request, 'addProduct.html', {'categories': categories})


# Create your views here.
def dex(request):

    product_object = Product.objects.all()

    item_name = request.GET.get('item-name')
    if item_name and item_name != '':
        product_object = product_object.filter(title__icontains=item_name)

    paginator = Paginator(product_object, 4)
    page = request.GET.get('page')
    product_object = paginator.get_page(page)
    return render(request, 'dex.html', {'product_object': product_object})

def detail(request, myid):
    product_object = Product.objects.get(id=myid)
    return render(request, 'detail.html', {'product': product_object}) 

def checkout(request):
    if request.method == "POST":
        items = request.POST.get('items')
        total = request.POST.get('total')
        nom = request.POST.get('nom')
        email = request.POST.get('email')
        address = request.POST.get('address')
        ville = request.POST.get('ville')
        pays = request.POST.get('pays')
        zipcode= request.POST.get('zipcode')
        com = Commande(items=items,total=total, nom=nom, email=email, address=address, ville=ville, pays=pays, zipcode=zipcode)
        com.save()
        return redirect('confirmation')


    return render(request, 'checkout.html') 

def confirmation(request):
    info = Commande.objects.all()[:1]
    for item in info:
        nom = item.nom
    return render(request, 'confirmation.html', {'name': nom})
      





def add_product(request):
    categories = Category.objects.all()

    if request.method == 'POST':
        # Retrieve form data
        product_name = request.POST.get('product-name')
        description = request.POST.get('description')
        price = request.POST.get('price')
        quantity = int(request.POST.get('quantity', 1))  # Default to 1 if quantity is not provided
        product_category_id = int(request.POST.get('product-category'))

        # Get the uploaded image file
        product_image = request.FILES.get('product-image')

        # Save the image file to the images directory
        image_path = default_storage.save('images/' + product_image.name, product_image)

        # Get the category object based on the category ID
        product_category = Category.objects.get(id=product_category_id)

        # Create a new Product object and save it to the database
        product = Product(
            title=product_name,
            price=price,
            description=description,
            category=product_category,
            image=image_path,
            user=request.user,  # Set the user foreign key
            quantity=quantity  # Set the quantity
        )
        product.save()

        return redirect('home')

    return render(request, 'addProduct.html', {'categories': categories})


def all_commands(request):
    commands = Commande.objects.all().order_by('-date_commande')
    return render(request, 'shop/all_commands.html', {'commands': commands})

def ajouter_panier(request, product_id):
    # Retrieve the product object
    product = Product.objects.get(pk=product_id)

    # Get the current user's shopping cart from the session
    panier = request.session.get('panier', {})

    # Check if the product already exists in the cart
    if product_id in panier:
        # Increment the quantity and update the total price
        panier[product_id]['quantity'] += 1
        panier[product_id]['total_price'] += product.price
    else:
        # Add the product to the cart
        panier[product_id] = {
            'title': product.title,
            'quantity': 1,
            'total_price': product.price
        }

    # Update the cart in the session
    request.session['panier'] = panier

    return redirect('product_list')