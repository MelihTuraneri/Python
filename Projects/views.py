from django.shortcuts import render
from members.models import *
from django.db.models import Q, F
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.cache import cache



def profile(request, username):
    query = list(Staff.objects.filter(username=username).all()
                 .annotate(country = F('address__city__country__country'), city = F('address__city__city'),
                           district = F('address__district'), addresss = F('address__address'),
                           postal_code = F('address__postal_code'), phone = F('address__phone'))
                           .values("first_name", "last_name", "email", "picture", "country",
                                   "city", "district", "addresss", "postal_code", "phone"))[0]

    return render(request, "profile.html", {'model': query})



def home(request):
    if request.method == 'POST':
        cache.clear()

        search= request.POST["search"]

        query = list(Film.objects.filter(title__icontains=search).values("film_id", "title", "release_year", "rental_rate").all())

        query2 = list(Film.objects.all().values("film_id", "title", "description").order_by("rental_rate"))[:5]

        page_num = request.GET.get('page', 1)
        paginator = Paginator(query, 20)

        try:
            page_obj = paginator.page(page_num)
        except PageNotAnInteger:
            page_obj = paginator.page(1)
        except EmptyPage:
            page_obj = paginator.page(paginator.num_pages)

        return render(request, "home.html", {'models': page_obj, 'models2' : query2})

    else:
        page_num = request.GET.get('page', 1)

        if page_num == 1:
            query = list(Film.objects.all())
            cache.set('my_key', query, 1800)
            query2 = list(Film.objects.all().values("film_id", "title", "description").order_by("rental_rate"))[:5]
            cache.set('my_key2', query2, 1800)
        else:
            query = cache.get("my_key")
            query2 = cache.get("my_key2")

        # if cache.get("my_key") == None:
        #     cache.set('my_key', query, 300)
        # else:
        #     query = cache.get("my_key")
            
        paginator = Paginator(query, 20)
        page_obj = paginator.page(page_num)

        return render(request, "home.html", {'models': page_obj, 'models2' : query2})



def film(request, film_id):
    query = list(Film.objects.filter(film_id=film_id).all().annotate(film_language = F('language__name')).values("title", "description", "release_year", "length",
                                                                                                             "special_features", "fulltext", "film_language"))[0]
    
    return render(request, "filmsv2.html", {"model" : query})



def categories(request):
    query = Category.objects.all().order_by("category_id")

    return render(request, "cat.html", {"categories": query})



def films_by_categories(request, category_id):

    film_id_list = list(FilmCategory.objects.filter(category=category_id).values_list("film", flat=True).all())
        
    query = list(Film.objects.filter(film_id__in=film_id_list).values("title", "film_id").all())

    return render(request, "films.html", {"models" : query,"category" : category_id})



def films_details(request, film_id, category_id):
    query = list(Film.objects.filter(film_id=film_id).annotate(film_language = F('language__name')).values("title", "release_year", "length",
                                                                                                           "description", "fulltext", "film_language",
                                                                                                           "rental_rate", "rental_duration",
                                                                                                           "special_features").all())[0]

    query2 = Category.objects.filter(category_id=category_id).values("name")[0]

    actor_id = list(FilmActor.objects.filter(film=film_id).values_list("actor", flat=True).all())

    query3 = list(Actor.objects.filter(actor_id__in=actor_id).values("first_name", "last_name").all())

    return render(request, "films_details.html", {"model": query, "model2" : query2, "models3" : query3})



def customers(request):
    if request.method == 'POST':
        search = request.POST["search"]

        query = list(Customer.objects.filter(Q(first_name__icontains=search) | Q(last_name__icontains=search) | Q(email__icontains=search)).values("first_name", "last_name", "email", "customer_id").all())

        return render(request, "customers.html", {'models': query})
    else:
        query = list(Customer.objects.values("first_name", "last_name", "email", "customer_id").all())

        return render(request, "customers.html", {'models': query})
    


def customer(request, customer_id):
    if request.method == 'POST':
        film_title = request.POST["search"]
        min = request.POST["min"]
        max = request.POST["max"]
        select1 = request.POST['select1']
        select2 = request.POST['select2']

        order_rule = "rental__rental_date" if select1 == "1" else "payment_date" if select1 == "2" else "rental__return_date"
        order_rule = "-" + order_rule if select2 == "2" else order_rule

        query = (Customer.objects.filter(customer_id=customer_id).all().annotate(country = F('address__city__country__country'),
                                                                                city = F('address__city__city'),
                                                                                district = F('address__district'),
                                                                                addresss = F('address__address'),
                                                                                postal_code = F('address__postal_code'),
                                                                                phone = F('address__phone'))
                                                                                .values("first_name", "last_name", "country", "city", 
                                                                                        "district", "addresss", "postal_code", "phone")[0])

        if min == "" and max == "":
            query2 = Payment.objects.filter(Q(customer=customer_id) & Q(rental__inventory__film__title__icontains=film_title)).all()
        elif min != "" and max == "":
            query2 = Payment.objects.filter(Q(customer=customer_id) & Q(amount__gte=float(min)) & Q(rental__inventory__film__title__icontains=film_title)).all()
        elif min == "" and max != "":
            query2 = Payment.objects.filter(Q(customer=customer_id) & Q(amount__lte=float(max)) & Q(rental__inventory__film__title__icontains=film_title)).all()
        else:
            query2 = Payment.objects.filter(Q(customer=customer_id) & Q(amount__gte=float(min)) &  Q(amount__lte=float(max)) & Q(rental__inventory__film__title__icontains=film_title)).all()
        
        query2 = (query2.annotate(title = F('rental__inventory__film__title'),
                                  rental_date = F('rental__rental_date'),
                                  return_date = F('rental__return_date'))
                                  .values("title", "amount", "rental_date", "return_date", "payment_date")
                                  .order_by(order_rule))

        return render(request, "customer.html", {"model" : query,"models2" : query2})
    else:
        query = (Customer.objects.filter(customer_id=customer_id).all().annotate(country = F('address__city__country__country'),
                                                                                city = F('address__city__city'),
                                                                                district = F('address__district'),
                                                                                addresss = F('address__address'),
                                                                                postal_code = F('address__postal_code'),
                                                                                phone = F('address__phone'))
                                                                                .values("first_name", "last_name", "country", "city", 
                                                                                        "district", "addresss", "postal_code", "phone")[0])

            
        query2 = (Payment.objects.filter(customer=customer_id).all().annotate(title = F('rental__inventory__film__title'),
                                                                             rental_date = F('rental__rental_date'),
                                                                             return_date = F('rental__return_date'))
                                                                             .values("title", "amount", "rental_date", "return_date", "payment_date")
                                                                             .order_by("rental__rental_date"))
            
        return render(request, "customer.html", {"model" : query,"models2" : query2})

