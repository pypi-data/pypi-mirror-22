Square project:

Usage command line interface

setup:
pip install square-cli

get all inventory from env_id=1:
inventory.py --url=http://localhost:8000/api -e 1 --list

get all inventory from env_id=1 with hostvars:
inventory.py --url=http://localhost:8000/api -e 1 --list --hostvars

get host inventory from env_id=1:
inventory.py --url=http://localhost:8000/api -e 1 --host 729059-comp-disk-306

Also, we can use environment variables for send parameters to inventory.py:
REST_API_URL=http://localhost:8000/api ENVIRONMENT_ID=1 INVENTORY_HOSTVARS=true INVENTORY_ALL=true LIST=true inventory.py
