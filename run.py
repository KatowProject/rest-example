import os

system_type = os.name
try:
    if system_type == 'nt':
        os.system('py manage.py runserver')
    else:
        os.system('python3 manage.py runserver')
except KeyboardInterrupt:
    print('Turning off server...')
