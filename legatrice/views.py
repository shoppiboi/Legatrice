from django.shortcuts import render
from django.http import HttpResponse
from .forms import GeeksForm
import requests
import re
from time import sleep

basic_mana_cards = [
    "Forest", 
    "Island",
    "Swamp",
    "Mountain",
    "Plains"
]

def extract_card_names(cockatrice_file, ignore_side=False):
    
    f = open(cockatrice_file, 'r')
    
    card_names = []

    for line in f:

        #   if the side zone has been ignored, iteration of the file ends here
        if 'zone name="side"' in line and ignore_side:
            return card_names
        
        if '" name=' in line:
            _split = line.split()[2:]
            _split = ' '.join(_split)
            result = re.search('name="(.*)"/>', _split)
            card_names.append(result.group(1))

    return card_names

def retrieve_legalities(card_name, format_name="standard"):

    name = card_name.lower()
    name = name.replace(" ", "+")

    #   if the card is one of the basic mana cards, return Legal
    #   explanation for this has been provided at Lines 5-12
    if card_name in basic_mana_cards:
        return "legal"
    
    response = requests.get("https://api.scryfall.com/cards/named?fuzzy=duelist's+heritage")
    
    if response.status_code == 200:
        card_data = response.json()
        return card_data['legalities'][format_name]

def handle_uploaded_file(file):  
    with open('legatrice/upload/'+file.name, 'wb+') as destination:  
        for chunk in file.chunks():
            destination.write(chunk)

def homePageView(request):
    context = {}
    if request.POST:
        form = GeeksForm(request.POST, request.FILES)
        if form.is_valid():
            handle_uploaded_file(request.FILES["geeks_field"])
    else:
        form = GeeksForm()
    context['form'] = form

    card_names = extract_card_names('legatrice/upload/'+request.FILES['geeks_field'].name, 'r')

    card_legality_pairs = {}

    for name in card_names:
        card_legality_pairs[name] = retrieve_legalities(name, 'commander')
        sleep(0.05) 

    print(card_legality_pairs)

    context['legalities'] = card_legality_pairs

    return render(request, "home.html", context)

    # return HttpResponse(response.content)