FROM mariadb:10.11

# Variables d'environnement pour la configuration
ENV MYSQL_ROOT_PASSWORD=root_password
ENV MYSQL_DATABASE=futurisys_ml
ENV MYSQL_USER=api_user
ENV MYSQL_PASSWORD=api_password

# Exposer le port MariaDB
EXPOSE 3306
