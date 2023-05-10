command = '/env-portfolio_mysql/bin/gunicorn'
pythonpath = '/apps/'
#bind = '172.26.0.4:8001' #ip container app con el puerto de unicorn
bind = '0.0.0.0:8001'
workers = 3

#sudo fuser -k 8000/tcp

#gunicorn -c config/gunicorn/gunicorn_config.py config.wsgi #Comando para correr Gunicorn