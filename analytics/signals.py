from django.dispatch import Signal

object_viewed = Signal(providing_args=['instance','request'])
