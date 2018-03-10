from difflib import SequenceMatcher

from django.db.models import Q

from analytics.utils import add_query
from analytics.utils import whichPage
from .models import Products

global all_product_cart

STOP_WORDS = ['price', 'prices', 'laptops', 'laptop', 'phones', 'phone', 'dresses']
all_products_c = Products.objects.all()
all_products = []

for product in all_products_c:
    all_products.append(product.name)

all_products = tuple(all_products)


def experimental_search(request, query):
    new_products = []
    print(query)
    for all_p in all_products:
        query_score = SequenceMatcher(a=query, b=all_p).ratio()
        if query_score > 0.30:
            new_products.append(all_p)
            print(query_score)
    print(new_products)


# Search Plugin
def search_bite(request, query):
    experimental_search(request, query)
    all_products = Products.objects.order_by('?')
    whichPage(request, 'search', request.build_absolute_uri())
    if 'iphone' in str(query.lower()) or 'ipad' in str(query.lower()):
        # # print(query)
        # print(list(query))
        query = query.lower()
        quey = query.split()

        for stop_w in STOP_WORDS:
            if stop_w in quey:
                quey.remove(stop_w)

        if len(quey) >= 3:
            if 'plus' in quey and len(quey) <= 3:
                q = ' '.join(quey)
                all_products = all_products.filter(
                    Q(name__icontains=q) |
                    Q(name__iexact=q)
                ).distinct()
            else:
                for q in quey:
                    all_products = all_products.filter(
                        Q(name__icontains=q)

                    ).distinct()

            add_query(query,
                      'search page',
                      all_products[:10],
                      nbool=True,
                      correct=query,
                      request=request)
        else:
            # query = correction(query)

            # print(query)
            query = query.strip()
            query = query.split()
            for stop_w in STOP_WORDS:
                if stop_w in query:
                    query.remove(stop_w)

            query = ' '.join(query)
            print(query)
            all_products = all_products.filter(
                Q(name__icontains=query) |
                Q(name__iexact=query)
            ).distinct()
            if len(all_products) == 0:
                add_query(query,
                          'search page',
                          all_products[:10],
                          nbool=False,
                          correct=query,
                          request=request)
            else:
                add_query(query,
                          'search page',
                          all_products[:10],
                          nbool=True, correct=query, request=request)
    else:
        query = query.split()
        new = []
        for stop_w in STOP_WORDS:
            if stop_w in query:
                query.remove(stop_w)
        for q in query:
            # q = correction(q)

            # print(q)
            new.append(q)
            # Put them all together

            all_products = all_products.filter(
                Q(name__icontains=q) |
                Q(name__iexact=q)
            ).distinct()

            query = ' '.join(query)
        made = ' '.join(new)
        if len(all_products) == 0:
            add_query(query, 'search page', all_products[:10], nbool=False, correct=made, request=request)
        else:
            add_query(query, 'search page', all_products[:10], nbool=True, correct=made, request=request)

    return all_products
