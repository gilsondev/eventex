# Eventex

Project that implement a event management

## Prepare environment

```bash
git clone git@github.com:/gilsondev/eventex.git
cd eventex
python -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt
cp contrib/env-sample .env
```

## How deploy this Project

```bash
heroku create myapp

heroku config:set SECRET_KEY=`python contrib/secret_gen.py`
heroku config:set DEBUG=False
heroku config:set ALLOWED_HOSTS=.herokuapp.com

# Configure o email com sendgrid
heroku addons:create sendgrid:starter
heroku config:set EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
heroku config:set EMAIL_HOST_USER=`heroku config:get SENDGRID_USERNAME`
heroku config:set EMAIL_HOST_PASSWORD=`heroku config:get SENDGRID_PASSWORD`

make heroku-deploy
```

## Scenarios

1. Create a subscription

```gherkin
Dado que temos um visitante qualquer
Quando ele acessa o endereço **/inscricao/**
Então ele vê a página de inscrição
  E a página possui um formulário
  E o formulário possui 4 campos
  E os campos são nome, email, cpf e telefone
  E o formulário possui um botão para inscrever.
```
