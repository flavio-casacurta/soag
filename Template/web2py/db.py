# -*- coding: utf-8 -*-

from   gluon.tools import Mail, Auth, Crud, Service
import os

try:
    widgets = addgets
except:
    widgets = None

PROJECT_PATH = os.path.abspath(os.path.dirname(__file__))
execfile(os.path.join(PROJECT_PATH,'settings_local.db'))

response.generic_patterns = ['*'] if request.is_local else []

mail = Mail()

# Tabela auth_user

auth = Auth(db)

db.define_table(auth.settings.table_user_name
                  , Field('username'
                  ,         label='Usuário'
                  ,         requires=IS_NOT_EMPTY())
                  , Field('first_name'
                  ,         label='Nome'
                  ,         requires=IS_NOT_EMPTY())
                  , Field('last_name'
                  ,         label='SobreNome'
                  ,         requires=IS_NOT_EMPTY())
                  , Field('email'
                  ,         label='EMail')
                  , Field('password'
                  ,         'password'
                  ,         length=512
                  ,         readable=False
                  ,         label='Senha')
                  , Field('registration_key'
                  ,         length=512
                  ,         writable=False
                  ,         readable=False
                  ,         default='')
                  , Field('reset_password_key'
                  ,         length=512
                  ,         writable=False
                  ,         readable=False
                  ,         default='')
                  , Field('registration_id'
                  ,         length=512
                  ,         writable=False
                  ,         readable=False
                  ,         default='')
                  , format='%(first_name)s %(last_name)s')

custom_auth_table                  = db[auth.settings.table_user_name]
custom_auth_table.email.requires   = [IS_EMAIL(), \
                                     IS_NOT_IN_DB(db, custom_auth_table.email)]

auth.settings.table_user           = custom_auth_table

crud    = Crud(db)
service = Service()

mail.settings.server = 'logging' or 'smtp.gmail.com:587'
mail.settings.sender = ''
mail.settings.login  = ''

auth.settings.hmac_key = 'sha512:564b7207-eb26-4557-b868-762120bb9786'
auth.define_tables(username=True)
auth.settings.mailer = mail
auth.settings.registration_requires_verification = False
auth.settings.registration_requires_approval = False
auth.messages.verify_email = 'Click on the link http://' + \
    request.env.http_host+URL('default','user',args=['verify_email']) + \
        '/%(key)s to verify your email'
auth.settings.reset_password_requires_verification = True
auth.messages.reset_password = 'Click on the link http://' + \
    request.env.http_host+URL('default','user',args=['reset_password']) + \
        '/%(key)s to reset your password'
auth.settings.actions_disabled.append('register')

crud.settings.auth          = ''
crud.messages.submit_button = T('Submit')
crud.settings.hideerror     = True
crud.settings.showid        = False

response.db                 = db
response.tipoMenu           = 'dtree'

#########################################################################
# Tabelas da Aplicacao
