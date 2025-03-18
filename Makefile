create-postgresql:
	docker build -t fast_api_postgresql -f testing_db.dockerfile .
	docker run -d --name fast_api_postgresql_db -p 5432:5432 fast_api_postgresql
test:
	#python -m unittest discover
	coverage run -m unittest discover
	coverage report -m
	coverage xml -o coverage.xml
run-db-viewer:
	docker run --rm --name db_viewer\
      -p 5050:80 \
      -e "PGADMIN_DEFAULT_EMAIL=a@b.com" \
      -e "PGADMIN_DEFAULT_PASSWORD=aa" \
      -d dpage/pgadmin4
update-postgresql:
	source .zshrc && alembic -c postgres.alembic.ini revision --autogenerate -m $(message)
upgrade-postgresql:
	source .zshrc && alembic -c postgres.alembic.ini upgrade head
