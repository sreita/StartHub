# 1. Usamos Nginx Alpine (Versión ligera y estable)
FROM nginx:1.25-alpine

# 2. Nos ubicamos en la carpeta donde Nginx sirve los archivos
WORKDIR /usr/share/nginx/html

# 3. Borramos los archivos por defecto de Nginx (el "Welcome to Nginx")
# Esto asegura que tu sitio esté limpio.
RUN rm -rf ./*

# 4. Copiamos TUS archivos (HTML, CSS, JS) al servidor
COPY . .

# 5. Exponemos el puerto 80 (el estándar web)
EXPOSE 80

# 6. Arrancamos el servidor
CMD ["nginx", "-g", "daemon off;"]