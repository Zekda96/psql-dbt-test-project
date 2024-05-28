import os
import json

# SQL Alchemy
from sqlalchemy import create_engine, inspect, text, Engine


def read_data_from_file(fp):
    with open(fp, "r") as f:
        data = json.load(f)
    
    return data
            

def get_db_engine(creds: str):

    credentials = json.load(open(creds, 'r'))

    USERNAME = credentials['USERNAME']
    PASSWORD = credentials['PASSWORD']
    DB_NAME =  credentials["DB_NAME"]

    database_uri = f"postgresql://{USERNAME}:{PASSWORD}@localhost:8080/{DB_NAME}"
    engine = create_engine(database_uri)
    
    return engine


def create_table(engine: Engine):
    with engine.connect() as connection:
        
        table = "web_events"
    
        inspect_eng = inspect(engine)
        if inspect_eng.has_table(table):
            query = f"""
            DROP TABLE {table}
            ;
            """
            connection.execute(text(query))
        
        query = f"""
        CREATE TABLE {table} (
            id SERIAL PRIMARY KEY,
            clickstream_data JSONB,
            inserted_time TIMESTAMPTZ DEFAULT Now()
        )
        ;
        """
        connection.execute(text(query))
        connection.commit()


def insert_data(engine: Engine, json_data: dict, chunksize=100):
    
    with engine.connect() as connection:
    # Truncate table and Insert data
        query = """
        TRUNCATE web_events RESTART IDENTITY;;
        """
        connection.execute(text(query))
        connection.commit()
        
        query = """INSERT INTO web_events (clickstream_data) VALUES"""
        c = 1
        chunk = chunksize
        data = json_data["data"]
        
        for i, s in enumerate(data):
            s = str(s).replace("\'", "\"")
            if c < chunk and i+1 < len(data):
                # Add row to insert statement
                query += f"('{s}'),\n"
                c += 1
                
            elif c==chunk or i+1==len(data):
                # End query and execute it
                query += f"('{s}')\n;"
                connection.execute(text(query))
                
                # Restart cycle
                query = """
                INSERT INTO web_events (clickstream_data)
                VALUES
                """
                c = 0
        
        connection.commit()
        
        # Read inserted data
        query = """
        SELECT id FROM web_events
        ORDER BY id DESC
        LIMIT 10
        ;
        """
        result = connection.execute(text(query))
        print("Last 10 row IDs from table: ", result.fetchall())
        connection.commit()


def main():
    credentials = os.path.join('credentials', 'credentials.json')
    engine = get_db_engine(credentials)
    # create_table(engine)
    
    fp = os.path.join("data", "clickstream_data.json")
    data = read_data_from_file(fp)

    insert_data(engine, data, chunksize=100)
    

if __name__ == "__main__":
    main()
    