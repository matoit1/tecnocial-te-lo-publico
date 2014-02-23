MYSQL_ROOT_PASSWORD=$1
MYSQL_USER="tecnocial"
MYSQL_PASSWORD="tecnocial"
MYSQL_DB="tecnocial"

mysql -u root -ptecnocial --execute="CREATE USER '${MYSQL_USER}'@'localhost' IDENTIFIED BY '${MYSQL_PASSWORD}';"
mysql -u root -ptecnocial --execute="CREATE DATABASE ${MYSQL_DB};"
mysql -u root -ptecnocial --execute="GRANT ALL PRIVILEGES ON ${MYSQL_DB}.* TO '${MYSQL_USER}'@'localhost';"