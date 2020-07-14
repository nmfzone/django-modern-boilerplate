from django.dispatch import Signal

pre_soft_delete = Signal(providing_args=['instance'])
post_soft_delete = Signal(providing_args=['instance'])
pre_restore = Signal(providing_args=['instance'])
post_restore = Signal(providing_args=['instance'])
