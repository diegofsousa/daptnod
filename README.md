# daptnod

> A shared note maker

<img alt="languages" src="https://img.shields.io/github/languages/count/diegofsousa/daptnod">
<img alt="last commit" src="https://img.shields.io/github/last-commit/diegofsousa/daptnod">

`daptnod` is a simple Django web application that creates quick notes that can be shared via a url. A more complete alternative to the popular dontpad.com. The implementation strives to be simple and free of unnecessary dependencies.

![Example](/docs/gif-daptnod.gif)


## Goals

- Easy and quick to create notes
- It is not necessary to create an account
- URL for a note is hashed (ex: https://<url_server>/EreQR5z)
- Possibility to create an account to save notes (**differential**) 
- Possibility to deprive notes for yourself (**differential**) 
- Ability to block changing the content of a note (**differential**) 
- Ability to know when a note was created and the last time it was changed (**differential**) 
- Ability to know who viewed a note (**differential**) 
- Search for notes by fragment of content (**differential**) 
- Adapted for mobile devices (responsive) (**differential**) 
- Dark mode (**differential**) 

## Structure

- `/daptnod/settings/base.py` General project settings file
- `/daptnod/settings/heroku.py` Production environment settings in heroku
- `/daptnod/urls.py` General routing for modules
- `/daptnod/core` Module with information shared among other embedded applications
- `/daptnod/accounts` Application responsible for user account actions
- `/daptnod/notes` Application responsible for managing notes

## Instructions

1. Install Python version 3.8+
1. Install pip and virtual environment (virtualenv, virtualenvwrapper, pyenv)
1. Create a virtual environment
1. Fork and clone repository
1. `pip install -r requirements.txt`
1. `make migrations && make migrate`
1. `make run`
1. Open <http://127.0.0.1:8000/> and verify

## Configuration

- `SECRET_KEY` Set to specify the secret key used by Django (never share)
- `DEBUG` Set to `True` to show relevant error information (never use `True` in production)
- `HASHID_FIELD_SALT` Set to specify the secret key used by django-hashid-field to create unique hashes for notes (never share)

## Dependencies

| Project      | Home Page                                    |
|--------------|----------------------------------------------|
| Django       | <https://www.djangoproject.com/>                     |
| Django Debug Toolbar        | <https://django-debug-toolbar.readthedocs.io/en/latest/>                       |
| django-hashid-field       | <https://pypi.org/project/django-hashid-field/>                |
| django-widget-tweaks  | <https://pypi.org/project/django-widget-tweaks/> |
| Gunicorn | <https://gunicorn.org/>                   |
| psycopg2-binary         | <https://pypi.org/project/psycopg2-binary/>                        |
| python-decouple          | <https://pypi.org/project/python-decouple/>         |
| whitenoise          | <http://whitenoise.evans.io/en/stable/>         |
| Bulma          | <https://bulma.io/>         |
| bulma-prefers-dark         | <https://github.com/jloh/bulma-prefers-dark>         |
| Pure-Javascript-Toaster-Plugin          | <https://github.com/kvinbabbar/Pure-Javascript-Toaster-Plugin>         |


## Contributing

- Open issue, discuss proposal
- Fork and clone repository
- Change code
- Review changes
- Send pull request

## License

[MIT](LICENSE)