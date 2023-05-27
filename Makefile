.PHONY: all

update-sys:
	# Upadating the system
	sudo apt-get update
	sudo apt-get -y upgrade

install: update-sys
	# Create and activate the virtual environment
	get-venv
	

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
	sudo systemctl stop rabbitmq-server

start-celery:
	# Start celery worker
	celery -A your_module worker --loglevel=info

# Virtual Environments
get-venv:
	# Setting virtual environment
	sudo python3 -m venv venv

set-venv: get-venv start-venv
	# Install dependencies
	sudo venv/bin/python -m pip install --upgrade pip
	venv/bin/pip install -r requirements.txt

start-venv:
	# starting the virtual environment
	. venv/bin/activate

