from django.apps import AppConfig
from watson import search as watson

class FinditConfig(AppConfig):
    name = 'findit'
    def ready(self):
        Products = self.get_model('Products')
        watson.register(Products)
        
