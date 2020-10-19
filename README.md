# PDF information extractor

The aim of this project is to extract informations form a scientific article (PDF format) and put them in an Excel file.

The data will be then transferred to a Neo4j database.

The second part of the project is to find the main topics from a posted abstract. 

The project is divided in three main parts

* `info-extractor-app`, an app where you can extract information from a PDF or fill up entries in the database
* `model-app`, an app written udner Streamlit dedicated to the model's conception
* `article-app`, an app exploiting the models directly

**Note :** this project was designed to support several databases, but due to a time problem, only SQLite is currently supported.

## Getting started

### Conda (recommended)

```shell
conda env create -f environment.yml
conda activate pdf-extraction-env
```

### Pip

Pip is version 20.2.3 when this project was created

```shell
pip install -r requirements.txt
```

### Docker

For the app (note: it might not work because of the database inclusion)

```shell
cd article-app
docker build -t article-app .
docker run -d --name app-demo -p 5000:5000 article-app

# Stop the container
docker stop app-demo
```

`docker-compose.yml` coming soon!

### Database

If you're using a SQL database, please run the following command :

```shell
cd info-extractor-app
python -c "from server_module import db, app" "with app.app_context(): db.create_all()"
```

## Launch the app

**Article app**

```shell
cd article-app
export FLASK_APP=server.py
python server.py
```

**Model app**

```shell
cd model-app
streamlit run stapp.py 
```

**Extractor app**

```shell
cd info-extractor-app
python -c "from server_module import db, app" 
python -c "with app.app_context(): db.create_all()"
export FLASK_APP=server.py
python server.py
```


## Troubleshooting

PDF extraction might not be the best method to get some information such as the ID. The main API would be more useful. Besides, `PyPDF2` can have some trouble sorting data properly.

