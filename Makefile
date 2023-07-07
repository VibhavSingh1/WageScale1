.PHONY: all

LOG_DIR := flaskr/logs/$(shell date +'%Y%m%d')
DATA_DIR = flaskr/data
CELERY_LOG_PATH = $(LOG_DIR)/celery.log
CELERY_BEAT_SCHEDULE_PATH = $(DATA_DIR)/celery/celerybeat-schedule

# DATABASES_DIR_PATH = flaskr/database
# CELERY_BACKEND_DB = $(DATABASES_DIR_PATH)/celery_results.db

update-sys:
	# Upadating the system
	sudo apt-get update
	sudo apt-get -y upgrade

install: update-sys
	# Create and activate the virtual environment
	$(MAKE) set-venv ; $(MAKE) get-rabbitmq
	

get-rabbitmq: update-sys
	# Installing RabbitMQ server
	sudo apt-get install erlang
	sudo apt-get install rabbitmq-server

# RabbitMQ Setup
set-rabbitmq:
	# Setting up the rabbitmq server configurations
	sudo systemctl enable rabbitmq-server
	sudo rabbitmq-plugins enable rabbitmq_management
	sudo rabbitmqctl list_users | grep -q '^flaskroot1\b' || sudo rabbitmqctl add_user flaskroot1 flaskroot1
	sudo rabbitmqctl set_user_tags flaskroot1 administrator
	sudo rabbitmqctl set_permissions -p / flaskroot1 ".*" ".*" ".*"

start-rabbitmq:
	# Start RabbitMQ server
	sudo systemctl start rabbitmq-server
	
stop-rabbitmq:
	# stop RabbitMQ server
	# sudo systemctl stop rabbitmq-server
	sudo rabbitmqctl stop

check-rabbitmq:
	# checking the status of RabbitMQ-server
	sudo systemctl status rabbitmq-server

# Celery Setup
start-celery:
	# Start celery worker
	mkdir -p $(LOG_DIR)
	mkdir -p $(DATA_DIR)/celery
	rm -rf $(CELERY_BEAT_SCHEDULE_PATH)
	. venv/bin/activate && \
	celery -A flaskr.celery_conf.celery_app worker --loglevel=info -E -f $(CELERY_LOG_PATH) \
	--schedule=$(CELERY_BEAT_SCHEDULE_PATH) --beat

stop-celery:
	# Stop the celery worker
	ps aux | grep 'flaskr.celery_conf.celery_app worker' | grep -v grep | awk '{ print $$2 }' | xargs -r kill


# Virtual Environments

set-venv: 
	sudo python3 -m venv venv && \
	. venv/bin/activate && \
	sudo venv/bin/python -m pip install --upgrade pip && \
	venv/bin/pip install -r requirements.txt

# App level targets
start-app-services: 
	# Starting the services required
	$(MAKE) start-rabbitmq
	sleep 5
	$(MAKE) start-celery
	

shut-app-services:
	# Shutting down running services
	$(MAKE) stop-celery
	sleep 5
	$(MAKE) stop-rabbitmq
