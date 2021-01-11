import environ

from daptnod.settings.base import *

env = environ.Env()

DEBUG = env.bool("DEBUG", False)

SECRET_KEY = env("SECRET_KEY")

ALLOWED_HOSTS = env.list("ALLOWED_HOSTS")

HASHID_FIELD_SALT = env('SECRET_SALT_HASH')

DATABASES = {
  "default": env.db(),
}