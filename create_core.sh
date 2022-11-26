
python3 -m venv .venv

source .venv/bin/activate

pip install -r requiremments.txt

solr create -c motorcycles__

cd src

scrapy crawl Motorcycle -O motorcycles.json

post -c motorcycles__ motorcycles.json

cd .. 
FLASK_APP=src flask run
 
