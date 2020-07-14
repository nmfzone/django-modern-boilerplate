from common.factories import UserFactory

order = 0


def handle(command):
    UserFactory(
        name='Administrator',
        username='superman',
        email='hi@app.com',
        is_admin=True
    )
