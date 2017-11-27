# import re
# from collections import Counter
# from .models import Products
# from difflib import get_close_matches
# def words(text): return re.findall(r'\w+', text.lower())
# wordings = []

# for product in Products.objects.all():
#     wordings.append(product.name.replace('\n','').replace('.00','').replace('\t',''))

# def correct(word):
#     print(wordings[:10])
#     return get_close_matches(word, wordings)[:1]