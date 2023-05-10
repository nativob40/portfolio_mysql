# Imagen base de Docker
FROM nginx

# Copiar archivo de configuración personalizado en el contenedor
COPY default.conf /etc/nginx/conf.d
# Copiar archivo estaticos en el contenedor
COPY static /usr/share/nginx/html

# Exponer el puerto 9000
EXPOSE 9000

# Comando que se ejecutará cuando el contenedor se inicie
CMD ["nginx", "-g", "daemon off;"]

