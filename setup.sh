#! /bin/sh

echo 'setting up Marqo docker'
docker pull marqoai/marqo:latest
docker rm -f marqo
docker run --name marqo -d -p 8882:8882 marqoai/marqo:latest

echo 'Setting up your environment...'
python3 -m venv .venv

echo 'Activating virtual environment...'
source .venv/bin/activate

echo 'Installing dependencies...'
pip install -r requirements.txt
