
# Use the official MariaDB image as the base image
FROM mariadb:10.11

# Set environment variables for the root password and the database name
ENV MYSQL_ROOT_PASSWORD=my-secret-pw
ENV MYSQL_DATABASE=mydatabase
ENV MYSQL_USER=myuser
ENV MYSQL_PASSWORD=mypassword


# Expose port 3306 for MariaDB
EXPOSE 3306