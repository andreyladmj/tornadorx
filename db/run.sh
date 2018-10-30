#!/usr/bin/env bash
service mysql start
mysql -e 'create database edusson_ds'
mysql edusson_ds < db/backup.sql
mysql -e "update mysql.user set plugin = 'mysql_native_password'"
mysql -e "FLUSH PRIVILEGES"
export ENV_NAME=/usr/src/app/.env
python3 -c "from edusson_ds_main.db.connections import DBConnection; DBConnection.migrate()"