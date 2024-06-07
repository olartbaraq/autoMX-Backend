p_up:
	#create all services listed in docker compose file with docker
	docker compose up -d

p_down:
	#delete all services listed in docker compose file
	docker compose down

db_up:
	#create a database from the db server
	docker exec -it automx-postgres createdb --username=root --owner=root automx_db

db_down:
	#delete a database from the db server
	docker exec -it automx-postgres dropdb --username=root automx_db

run: 
	# run the flask server
	flask --app automx run --debug --with-threads

init-db:
	# Initialized the database
	flask --app automx init-db