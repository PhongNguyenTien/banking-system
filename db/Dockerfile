FROM mysql:8.0

COPY init.sql /docker-entrypoint-initdb.d/
COPY conf/my.cnf /etc/mysql/conf.d/my.cnf
