# 1. Usamos Nginx Alpine (Versión ligera y estable)
FROM nginx:1.25-alpine

# 2. Nos ubicamos en la carpeta donde Nginx sirve los archivos
WORKDIR /usr/share/nginx/html

# 3. Borramos los archivos por defecto de Nginx (el "Welcome to Nginx")
# Esto asegura que tu sitio esté limpio.
RUN rm -rf ./*

# 4. Copiamos TUS archivos (HTML, CSS, JS) al servidor
COPY . .

# 5. Creamos configuración de Nginx para servir home.html como índice
RUN echo 'server { \
    listen 80; \
    server_name localhost; \
    root /usr/share/nginx/html; \
    index home.html; \
    \
    # Deshabilitar caché para archivos JS, CSS y HTML \
    location ~* \.(js|css|html)$ { \
        add_header Cache-Control "no-store, no-cache, must-revalidate, proxy-revalidate, max-age=0"; \
        add_header Pragma "no-cache"; \
        add_header Expires "0"; \
        try_files $uri =404; \
    } \
    \
    location / { \
        try_files $uri $uri/ /home.html; \
    } \
}' > /etc/nginx/conf.d/default.conf

# 6. Exponemos el puerto 80 (el estándar web)
EXPOSE 80

# 7. Arrancamos el servidor
CMD ["nginx", "-g", "daemon off;"]