import random

from fabric.api import env
from fabric.api import local
from fabric.api import run
from fabric.contrib.files import append
from fabric.contrib.files import exists
from fabric.contrib.files import sed

REPO_URL = "https://github.com/michaelwknott/obey-the-testing-goat.git"


def deploy():
    site_folder = f"/home/{env.user}/sites/{env.host}"
    source_folder = f"{site_folder}/source"
    _create_directory_structure_if_necessary(site_folder)
    _get_latest_source(source_folder)
    _update_settings(source_folder, site_folder, env.host)
    _update_virtualenv(source_folder)
    _update_static_files(source_folder)
    _update_database(source_folder)


def _create_directory_structure_if_necessary(site_folder):
    for subfolder in ("database", "static", ".venv", "source"):
        run(f"mkdir -p {site_folder}/{subfolder}")


def _get_latest_source(source_folder):
    if exists(f"{source_folder}/.git"):
        run(f"cd {source_folder} && git fetch")
    else:
        run(f"git clone {REPO_URL} {source_folder}")
    current_commit = local("git log -n 1 --format=%H", capture=True)
    run(f"cd {source_folder} && git reset --hard {current_commit}")


def _update_settings(source_folder, site_folder, site_name):
    settings_path = f"{source_folder}/superlists/settings.py"
    sed(settings_path, "DEBUG = True", "DEBUG = False")
    sed(settings_path, "ALLOWED_HOSTS =.+$", f'ALLOWED_HOSTS = ["{site_name}"]')
    dot_env_file = f"{site_folder}/.env"
    if not exists(dot_env_file):
        chars = "abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)"
        key = "".join(random.SystemRandom().choice(chars) for _ in range(50))
        append(dot_env_file, f'SECRET_KEY = "{key}"')


def _update_virtualenv(source_folder):
    virtualenv_folder = f"{source_folder}/../.venv"
    if not exists(f"{virtualenv_folder}/bin/pip"):
        run(f"python3 -m venv {virtualenv_folder}")
    run(f"{virtualenv_folder}/bin/pip install -r {source_folder}/requirements.txt")


def _update_static_files(source_folder):
    run(f"cd {source_folder} && ../.venv/bin/python manage.py collectstatic --noinput")


def _update_database(source_folder):
    run(f"cd {source_folder} && ../.venv/bin/python manage.py migrate --noinput")
