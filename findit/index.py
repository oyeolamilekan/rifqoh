import algoliasearch_django as algoliasearch

from .models import Products

algoliasearch.register(Products)