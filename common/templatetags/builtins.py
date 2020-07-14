import json
import pydash as _
from common.exceptions import FormErrorBag
from django import template
from django.shortcuts import resolve_url
from django.template.base import Node, NodeList, TemplateSyntaxError
from django.template.defaultfilters import stringfilter
from django.utils.safestring import mark_safe

register = template.Library()


# Filters
###################################################

@register.filter('resolve_url')
def do_resolve_url(value):
    return resolve_url(value)


@register.filter('to_int')
def do_to_int(value):
    return int(value)


@register.filter('isinstance')
def do_isinstance(value, _type):
    if _type == 'list':
        return isinstance(value, list)
    elif _type == 'str':
        return isinstance(value, str)
    elif _type == 'int':
        return isinstance(value, int)
    elif _type == 'bool':
        return isinstance(value, bool)

    raise ValueError("isinstance template filter doesn't support '%s' type." % _type)


@register.filter('divided_by')
def do_divided_by(value, by):
    return value/by


@register.filter('current_url_is')
@stringfilter
def do_current_url_is(value, request):
    operator = ','

    if ',' in value and '|' in value:
        raise TemplateSyntaxError(
            "current_url_is: You can use ',' or '|', but not both."
        )
    elif '|' in value:
        operator = '|'

    for pattern in value.split(operator):
        if operator == ',' and not request.match(pattern):
            return False
        elif operator == '|' and request.match(pattern):
            return True

    if operator == ',':
        return True

    return False


@register.filter('truncate', is_safe=True)
@stringfilter
def do_truncate(value, arg):
    try:
        bits = str(arg).split(':')
        length = int(bits[0])
        omission = '...'

        if len(bits) > 1:
            omission = bits[1]

        return _.truncate(value, length, omission)

    except (ValueError, TypeError):
        return value  # Fail silently.


# Simple Tags
###################################################

@register.simple_tag
def method_override(method):
    method_override_html = '<input type="hidden" name="_method" value="{value}">'.format(value=method)

    return mark_safe(method_override_html)


@register.simple_tag(takes_context=True)
def calculate_index(context, index, per_page=10):
    page = int(context.request.GET.get('page', 1))

    return ((page - 1) * per_page) + index


def get_old_input_from_session(session):
    return session.get('_old_input')


@register.simple_tag(takes_context=True)
def old_input(context, key, value=''):
    _old_input = get_old_input_from_session(context.request.session)

    value = _.get(_old_input, key, value)

    if value is None or len(str(value)) == 0:
        return ''

    return value


def get_errors_from_session(session):
    return FormErrorBag(json.loads(session.get('_errors', '{}')))


@register.simple_tag(takes_context=True)
def get_error(context, key):
    return get_errors_from_session(context.request.session).get(key, '')


# Tags
###################################################

@register.tag(name='error')
def do_error(parser, token):
    _token = token
    condition = True
    nodelist = parser.parse(('else', 'enderror'))
    conditions_nodelists = [(condition, nodelist)]
    token = parser.next_token()

    # {% else %} (optional)
    if token.contents == 'else':
        nodelist = parser.parse(('enderror',))
        conditions_nodelists.append((None, nodelist))
        token = parser.next_token()

    # {% enderror %}
    if token.contents != 'enderror':
        raise TemplateSyntaxError('Malformed template tag at line {0}: "{1}"'.format(token.lineno, token.contents))

    try:
        tag_name, key = _token.split_contents()
    except ValueError:
        raise TemplateSyntaxError(
            "%r tag requires exactly one arguments" % _token.contents.split()[0]
        )

    if not (key[0] == key[-1] and key[0] in ('"', "'")):
        raise TemplateSyntaxError(
            "%r tag's argument should be in quotes" % tag_name
        )

    return IFHasErrorsNode(conditions_nodelists, key[1:-1])


# Tag Nodes
###################################################

class IFHasErrorsNode(Node):
    def __init__(self, conditions_nodelists, key):
        self._key = key
        self.conditions_nodelists = conditions_nodelists

    def __repr__(self):
        return '<%s>' % self.__class__.__name__

    def __iter__(self):
        for _, nodelist in self.conditions_nodelists:
            yield from nodelist

    @property
    def nodelist(self):
        return NodeList(self)

    def render(self, context):
        for condition, nodelist in self.conditions_nodelists:

            if condition:
                match = get_errors_from_session(context.request.session).has(self._key)
            else:
                match = True

            if match:
                return nodelist.render(context)

        return ''
