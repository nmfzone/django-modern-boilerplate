import factory
import django
import dotenv
import faker
import inspect
import logging
import os
import splinter
import time
from behave import use_fixture
from behave.log_capture import capture
from django.conf import settings
from features.behave_fixtures import django_test_runner, django_test_case
from webdriver_manager.chrome import ChromeDriverManager


try:
    inspect_file = inspect.getfile(inspect.currentframe())
    env_path = os.path.dirname(os.path.abspath(inspect_file))
    env_file = "{}/../.env.behat".format(env_path,)

    if os.path.exists(env_file):
        dotenv.load_dotenv(env_file)
except Exception as e:
    pass


os.environ['DJANGO_SETTINGS_MODULE'] = 'core.settings'

django.setup()


@capture
@factory.Faker.override_default_locale(getattr(settings, 'FAKER_LOCALE', 'en_US'))
def before_all(context):
    use_fixture(django_test_runner, context)

    # Add fake factory
    context.faker = faker.Faker()

    # Add logging
    context.config.setup_logging()
    context.logger = logging.getLogger('behave')

    # Dir to output test artifacts
    context.artifacts_dir = 'artifacts'


@capture
def before_scenario(context, scenario):
    use_fixture(django_test_case, context)

    context.base_url = context.test.live_server_url
    os.environ['APP_URL'] = context.base_url

    purge_old_screenshots(context)

    browser = splinter.Browser('chrome', headless=True, executable_path=ChromeDriverManager().install())
    context.browser = browser


@capture
def after_scenario(context, scenario):
    screenshot_on_error(context, scenario)

    context.browser.quit()


def purge_old_screenshots(context):
    scenario_error_dir = os.path.join(context.artifacts_dir, 'feature_errors')

    for the_file in os.listdir(scenario_error_dir):
        file_path = os.path.join(scenario_error_dir, the_file)

        if file_path.endswith('.png'):
            os.unlink(file_path)


def screenshot_on_error(context, scenario):
    if scenario.status == 'failed':
        scenario_error_dir = os.path.join(context.artifacts_dir, 'feature_errors')
        make_dir(scenario_error_dir)
        scenario_file_path = os.path.join(scenario_error_dir, '%s_%s.png' % (
                scenario.feature.name.replace(' ', '_'),
                time.strftime("%H%M%S_%d_%m_%Y")
        ))
        context.browser.driver.save_screenshot(scenario_file_path)


def make_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)
