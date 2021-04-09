WEB=`docker-compose ps | grep gunicorn | cut -d\  -f 1 | head -n 1`
FILE=production.yml
ENV_STAGE = ``


#------------------------------------------------------------/
# GIT 
#------------------------------------------------------------/

git-pull:
	git stash
	git pull origin master


#------------------------------------------------------------/
# SHELLS
#------------------------------------------------------------/

shell-ikon:
	docker exec -ti $(WEB) bash

shell-celeryw:
	docker exec -ti ikon-celery-worker /bin/bash

shell-celeryb:
	docker exec -ti ikon-celery-beat /bin/bash

shell-redis:
	docker exec -ti hit-redis /bin/bash


#------------------------------------------------------------/
# LOGS
#------------------------------------------------------------/

log-nginx:
	docker-compose logs nginx

log-web:
	docker-compose logs web

log-web-live:
	docker logs --tail 50 --follow --timestamps $(WEB)

log-celeryw:
	docker-compose logs celeryworker

log-celeryb:
	docker-compose logs celerybeat	

#------------------------------------------------------------/
# DJANGO ikon
#------------------------------------------------------------/

collectstatic:
	docker exec $(WEB) /bin/sh -c "cd ikon; python manage.py collectstatic --noinput --clear" ;\

migrate:
	docker exec $(WEB) /bin/sh -c "cd ikon; python manage.py migrate"

makemigrations:
	docker exec $(WEB) /bin/sh -c "cd ikon; python manage.py makemigrations"

install-requirements:
	docker exec $(WEB) /bin/sh -c "pip install --no-cache-dir -r requirements.txt"

#------------------------------------------------------------/
# PRODUCTION
#------------------------------------------------------------/

start:
	docker-compose -f $(FILE) start

stop:
	docker-compose -f $(FILE) stop

build-up:
	docker-compose -f $(FILE) up --build

ps:
	docker-compose -f $(FILE) ps
	@echo "---------------------------"
	@echo "Web:     `ps aux | grep /usr/local/bin/gunicorn | grep -v grep | wc -l` threads running"

clean: stop
	docker-compose -f $(FILE) rm -f

restart: clean build up ps
	@echo "Restarted all containers"
