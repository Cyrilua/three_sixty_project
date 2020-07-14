command = '/home/www/code/project360/env/bin/gunicorn'
pythonpath = '/home/www/code/project360/three_sixty_project'
bind = '127.0.0.1:8000'
workers = 5
user = 'www'
limit_request_fields = 32000
limit_request_field_size = 0
raw_env = 'DJANGO_SETTINGS_MODULE=three_sixty_project.settings'
