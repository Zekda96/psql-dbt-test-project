# PE-exercises


## Setup
1. Open a terminal on the project directory and install project requirements.
```
pip install -r requirements.txt
```

2. Build and run docker container with PostgreSQL database:
```
docker-compose up -d --build
```
3. Run python scrypts to generate fake clickstream data and upload the data to the psql database.

```
python .\src\script1_generate-fake-data.py

python .\src\script2_load-to-db.py
```

4. Go to dbt project directory:
```
cd .\pe_clickstream\
```

5. Run dbt
```
dbt run
```