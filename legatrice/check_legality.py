import re
import time
import requests

#   due to the number of print editions these five cards have;
#   the performance of the program is significantly hindered,
#   where upto 8 seconds are spent retrieving the data for each
#   respective card.
# 
#   Hence, they've been given an exception where instead of reaching
#   into the API, they will instantly return Legal, as these cards are
#   ~traditionally~ always Legal. 
basic_mana_cards = [
    "Forest", 
    "Island",
    "Swamp",
    "Mountain",
    "Plains"
]

#   gets all card names from the .COD file.
#   this script has been made for files generated by Cockatrice specifically-
#   so format remains constant and follows the extraction rules set out below.
def extract_card_names(cockatrice_file, ignore_side=False):
    card_names = []

    for line in cockatrice_file:

        #   if the side zone has been ignored, iteration of the file ends here
        if 'zone name="side"' in line and ignore_side:
            return card_names
        
        if '" name=' in line:
            _split = line.split()[2:]
            _split = ' '.join(_split)
            result = re.search('name="(.*)"/>', _split)
            card_names.append(result.group(1))

    return card_names

def retrieve_legalities(card_name, format_name="Standard"):

    #   if the card is one of the basic mana cards, return Legal
    #   explanation for this has been provided at Lines 5-12
    if card_name in basic_mana_cards:
        return "legal"

    #   get the first instance of the card (this is due to 
    #   the library returning all the print editions of the card)
    #   as the legality remains constant regardless of print edition
    response = requests.get("https://api.scryfall.com/cards/named?fuzzy=" + card_name)
    
    if response.status_code == 200:
        card_data = response.json()
        return card_data['legalities'][format_name]
    return "not_legal"

def main(lines, format_choice, ignore_sideboard):
    card_names = extract_card_names(lines, ignore_sideboard)

    card_legality_pairs = {}

    for name in card_names:
        card_legality_pairs[name] = retrieve_legalities(name, format_choice)
        time.sleep(0.02)

    return card_legality_pairs