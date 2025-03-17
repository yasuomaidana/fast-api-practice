# Database notes

You could use docker compose, but we are playing with docker, therefore for the moment I'll use basic docker commands
and files.

## Using multiples 

To see all the explanation [see](https://stackoverflow.com/questions/25540711/docker-postgres-pgadmin-local-connection)

1. Postgres with Docker... or start with our Make command
2. PgAdmin with Docker... or start with our Make command
3. Connection string for PgAdmin: Enter [PgAdmin](http://localhost:5050). Then add a server with:
    ```
    name: container-postgresdb
    host: host.docker.internal
    database: postgres
    user: postgres
    password: admin
    ```
