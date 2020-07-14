<p align="center"><img src="https://www.djangoproject.com/s/img/logos/django-logo-positive.png" width="250px" alt="Django Boilerplate"></p>

# Django Boilerplate

Django Modern Boilerplate for building awesome web applications.

## Features

- TailwindCss, for styling the interfaces
- Laravel Mix, for bundling static assets through Webpack
- Configured behave for testing your application in BDD (Behavior-driven development)
- Support soft-delete on your Django models (thanks to [django-softdelete](https://github.com/scoursen/django-softdelete) package)
- Built-in fields for `PositiveAutoField`, `PositiveBigAutoField` and `PositiveBigIntegerField` 
- Built-in commands for migrate-fresh, migrate-refresh and database seeder
- Prefixed templates with the module name (`app:layouts/app.html`)
- Support HTTP Method Spoofing via Form (`_method`) or via `HTTP_X_HTTP_METHOD_OVERRIDE` header

## Requirements

- Python >= 3.5
- Pip
- Mysql
- NodeJs (optional)
- Yarn (optional)
- Redis (optional)
- Virtualenv (optional)
- Pyenv (optional)

## How to use

1. Download or clone this repository `git clone git@github.com:nmfzone/django-modern-boilerplate.git`
2. Navigate into that directory
3. Install the provided packages `pip install -r requirements.txt`
4. Duplicate `.env.example` to `.env`
5. Change the appropriate setting in the `.env`
6. Migrate the database schema `python manage.py migrate`
7. Seed the initial data `python manage.py seed`
8. Start the server `python manage.py runserver`
9. Open `http://localhost:8000` in your browser
10. Let's rock!

## Contributing

Want to contribute? Awesome. Just send a pull request.

## Bugs

If you discover a bug within this Boilerplate, please send an e-mail to Nabil Muhammad Firdaus at 123.nabil.dev@gmail.com.

## License

This Boilerplate is open-sourced software licensed under the [MIT license](http://opensource.org/licenses/MIT).
