.PHONY: migrate
migrate:
	docker-compose exec web flask db upgrade

.PHONY: migrations
migrations:
	docker-compose exec web flask db migrate

.PHONY: test
test:
	docker-compose exec web pytest -W ignore::DeprecationWarning

