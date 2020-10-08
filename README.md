# PDF information extractor

The aim of this project is to extract informations form a scientific article (PDF format) and put them in an Excel file.

The data will be then transferred to a Neo4j database.

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

For the app

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



## Troubleshooting

PDF extraction might not be the best method to get some information such as the ID. The main API would be more useful. Besides, `PyPDF2` can have some trouble sorting data properly.

