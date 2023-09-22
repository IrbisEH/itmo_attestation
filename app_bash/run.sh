#!/usr/bin/bash

. ../.env

sql_dump="database/books_shop.backup"

cd ..

sudo su - postgres <<EOF
createdb $DB_NAME;
psql -c "CREATE USER $DB_USER WITH PASSWORD '$DB_PASSWORD';"
psql -c "GRANT ALL PRIVILEGES ON DATABASE $DB_NAME TO $DB_USER;"
EOF

psql -U $DB_USER -d $DB_NAME -a -h localhost -p 5432 -f $sql_dump