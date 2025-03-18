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

## Migrations

1. Install alembic `uv add alembic`
2. Create the alembic.ini file 
   ```bash
   alembic init migrations
   ```
3. We are going to use two configurations one for TinySQL and
   another for Postgres.
   - For TinySQL we are going to use the `sqlite` configuration. The default alembic configuration.
   - For Postgres, we are going to use the `postgres` configuration. We are going to create a new file `alembic.ini` with
   ```bash 
   alembic -c postgres.init init postgres.migrations
   ```
4. Configure the `alembic.ini` file with the correct connection string.
   1. Add the imports to `script.py.mako` file
      ```python
      # other imports ...
      from alembic import op
      import sqlalchemy as sa
      # Starts here
      import sqlmodel
      import models
      #Stops here
      from settings import database_settings
      # ${imports if imports else ""}
      # other imports ...
      ```
   2. Modify the `sqlalchemy.url` value, we can do it by using our `database_settings`, to do it we need to do the following:
       ```python
       # migrations/env.py
       import models # This module contains all the models
       from settings import database_settings
       from alembic import context
       """ Other imports and code """
       config = context.config
       config.set_main_option('sqlalchemy.url', database_settings.dsn)
       assert database_settings.type == "sqlite"
       ```
      The assert statement is used to ensure we are using the correct database type.
       > You can also hardcode the value in the `alembic.ini` file.
       > `sqlalchemy.url = driver://user:pass@localhost/dbname`
5. Create the changes by using the following command:
   ```bash
   alembic revision --autogenerate -m "YOUR MIGRATION MESSAGE"
   ```
6. Apply the changes by using the following command:
   ```bash
   alembic upgrade head
   ```
