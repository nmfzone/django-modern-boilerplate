from django.utils.text import slugify


class SluggableModelMixin:
    def _generate_slug(self, value):
        slug = original = slugify(value, allow_unicode=True)

        i = 0
        while True:
            if not self.__class__._default_manager.filter(slug=slug).exists():
                break
            slug = '{}-{}'.format(original, ++i)

        return slug
