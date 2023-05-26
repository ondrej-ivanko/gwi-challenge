## Instalation
```
git clone git@github.com:ondrej-ivanko/gwi-challenge.git
cd gwi-challenge
install poetry.py
poetry install
```

## Run
```
poetry shell
cd dinopedia
./manage.py createsuperuser --username <your username> --email <your email> --password
./manage.py runserver 0.0.0.0:8000
```

## Run with Docker compose
```
docker-compose up -d --remove-orphans
```

## Exposed REST endpoints
- **/admin/** - Admin intefrace for managing application resources. Includes Picture, Dinosaur and User models management.
- **/dinosaurs** - list all dinosaurs in database. Filtering of dinosaurs by attributes can be done via Filter widget on top of the webpage. 
List favourite dinosaurs by using `favourite=true` query parameter.
- **/dinosaurs/<pk>**- list specific dinosaur. Extra action on top of the bar allows making of relationship between authenticated User and his favourite Dinosaur.
- **/dinosaurs/<pk>/update_dino_favourite**- allows creation/deletion of Favourite dinosaur for authenticated User.
You can also user curl:
- `curl -X POST --user <superusername:superuser password> "http://0.0.0.0:8000/dinosaurs/2/update_dino_favourite" -v`
- `curl -X DELETE --user <superusername:superuser password> "http://0.0.0.0:8000/dinosaurs/2/update_dino_favourite" -v`
