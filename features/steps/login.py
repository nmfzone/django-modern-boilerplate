from behave import *
import crayons


@given('a web browser is on the Login page')
@when('a web browser is on the Login page')
def step_impl(context):
    path = '/login'.lstrip('/')
    context.browser.visit(context.base_url + '/' + path)


def console(text, bold=False):
    print(crayons.yellow(text, bold=bold))
