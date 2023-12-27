FROM mariadb:10
COPY dump.sql.gz /docker-entrypoint-initdb.d/
