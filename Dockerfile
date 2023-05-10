FROM python:3.10-alpine

RUN apk update
RUN apk add gcc libc-dev g++ libffi-dev libxml2 unixodbc-dev unixodbc mariadb-dev libstdc++6
#si tirar error, borrar nginx
RUN apk add bash icu-libs krb5-libs libgcc libintl libssl1.1 libstdc++ zlib curl gnupg

WORKDIR /apps

# Copy into "/apps" all app files
COPY . .

# Install dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

###########################################################

#Para correrlo LOCAL
#Port_app:
EXPOSE 8000
#Port_Gunicorn:
EXPOSE 8001

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

############################################################

#Para correrlo en un server
#EXPOSE 80
#EXPOSE 8001
#CMD ["python", "manage.py", "runserver", "0.0.0.0:80"] 

############################################################