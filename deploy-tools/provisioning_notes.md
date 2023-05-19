Provisioning a New Site
=======================

## Required packages:

* nginx
* Python 3.6
* venv + pip
* Git

eg, on Ubuntu:

    sudo apt update
    sudo apt install nginx

## Nginx Virtual Host config

* see nginx.template.conf
* replace SITENAME with, e.g., staging.my-domain.com

## Systemd service

* see gunicorn-systemd.template.service
* replace SITENAME with, e.g., staging.my-domain.com

## Folder structure:

Assume we have a user account at /home/username

/home/username
└── sites
    ├── SITENAME
    │    ├── database
    │    ├── source
    │    ├── static
    │    └── .venv
    └── SITENAME
