from behave import fixture
from django.test.runner import DiscoverRunner
from django.test.testcases import LiveServerTestCase


@fixture
def django_test_runner(context):
    context.test_runner = DiscoverRunner()
    context.test_runner.setup_test_environment()
    context.old_db_config = context.test_runner.setup_databases()
    yield
    context.test_runner.teardown_databases(context.old_db_config)
    context.test_runner.teardown_test_environment()


@fixture
def django_test_case(context):
    context.test = LiveServerTestCase()
    context.test._pre_setup()
    context.test.setUpClass()
    yield
    context.test.tearDownClass()
    context.test._post_teardown()  # flush DB
    del context.test
