import re
from collections import Counter
from .models import Products
from difflib import get_close_matches

def words(text): return re.findall(r'\w+', text.lower())
wordings = []

for product in Products.objects.order_by('?'):
	wordings += product.name.replace('\n','').replace('.00','').replace('\t','').replace('(','').replace(')','').split()

#print(wordings)

def correction(word):
    #print(wordings[:10])
    return get_close_matches(word, wordings)[0]