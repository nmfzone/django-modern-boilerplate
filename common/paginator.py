from django.core.paginator import Paginator as BasePaginator


class Paginator(BasePaginator):
    on_each_side = 2
    current_page = 1

    @property
    def page_elements(self):
        window = self.on_each_side * 2
        result = {
            'first': None,
            'slider': None,
            'last': None
        }

        if self.num_pages < (self.on_each_side * 2) + 6:
            result['first'] = list(range(1, self.num_pages + 1))
        elif self._current_page <= window:
            result = {
                'first': list(range(1, window + 2)),
                'slider': None,
                'last': list(range(self.num_pages, self.num_pages + 1))
            }
        elif self._current_page > (self.num_pages - window):
            result = {
                'first': list(range(1, 3)),
                'slider': None,
                'last': list(range(self.num_pages - window, self.num_pages + 1))
            }
        elif self.num_pages > 1:
            result = {
                'first': list(range(1, 3)),
                'slider': list(range(
                    self._current_page - self.on_each_side,
                    self._current_page + self.on_each_side + 1
                )),
                'last': list(range(self.num_pages, self.num_pages + 1))
            }

        return filter(None, [
            result['first'],
            '...' if isinstance(result['slider'], list) else None,
            result['slider'],
            '...' if isinstance(result['last'], list) else None,
            result['last']
        ])

    @property
    def _current_page(self):
        current_page = int(self.current_page)

        return 1 if current_page < 1 else current_page
