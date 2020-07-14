import time
from behave import *
from common.factories import *
from django.contrib.auth import get_user_model

User = get_user_model()

use_step_matcher("re")


@given('user "(?P<username>(?:[^"]|\\")*)" exists')
def create_user(context, username):
    UserFactory(username=username)
    user = User.objects.filter(username=username).first()
    context.test.assertIsNot(user, None)
    context.test.assertEqual(user.username, username)


@then('(?:|I )fill in "(?P<field>(?:[^"]|\\")*)" with "(?P<value>(?:[^"]|\\")*)"')
def fill_in_with(context, field, value):

    context.browser.fill(field, value)


@then('(?:|I )press "(?P<button>(?:[^"]|\\")*)"')
def fill_in_with(context, button):
    element = context.browser.find_by_css(button)

    element.first.click()


@then('(?:|I )should be on "(?P<page>[^"]+)"')
def should_be_on(context, page):
    url = context.browser.url
    context.test.assertEqual(url, context.base_url + ('' if page == '/' else page))


def wait(wait_time):
    end_time = time.time() + wait_time

    x = 0
    while time.time() < end_time:
        x += 1  # do nothing, just wait
