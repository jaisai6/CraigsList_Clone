from django.shortcuts import render
from bs4 import BeautifulSoup
import requests
from requests.compat import quote_plus
from . import models

BASE_CRAIGSLIST_URL = "https://losangeles.craigslist.org/search/?query={}"

# Create your views here.
def home(request):
    return render(request,'my_app/base.html')

def new_search(request):
    search = request.POST.get('search')
    models.Search.objects.create(search = search)
    final_url = BASE_CRAIGSLIST_URL.format(quote_plus(search))
    response = requests.get(final_url)
    data = response.text
    soup = BeautifulSoup(data, features='html.parser')

    post_listings = soup.find_all('li',{'class': 'result-row'})

    final_postings = []

    for post in post_listings:
        post_title = post.find(class_ = 'result-title').text
        post_url = post.find(class_ = 'result-title').get('href')

        if post.find(class_ = 'result-price'):
            post_price = post.find(class_ = 'result-price').text
        else:
            post_price = "N/A"
        

        if( post.find(class_ = 'result-image').get('data-ids') ):
            image_id = post.find(class_ = 'result-image').get('data-ids').split(',')[0].split(':')[1]
            print(image_id)
            post_image = "https://images.craigslist.org/{}_300x300.jpg".format(image_id)

        else:
            post_image = "https://craigslist.org/images/peace.jpg"
        
        final_postings.append( (post_title,post_url,post_price,post_image) )

    stuff_for_frontend = {
        'search': search,
        'final_postings': final_postings,
    }

    return render(request,'my_app/new_search.html',stuff_for_frontend)
