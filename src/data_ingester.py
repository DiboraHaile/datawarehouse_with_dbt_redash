import pandas as pd
import glob
import sys
import psycopg2 as p
from psycopg2 import sql
import argparse
from data_parser import prepare_for_record,prepare_for_trajectory
sys.path.append("../data/")
import logging

def create_insert_stmt(table_name,cols):
    return sql.SQL("INSERT INTO {} ({}) VALUES ({})").format(
            sql.Identifier(table_name),
            sql.SQL(', ').join(map(sql.Identifier, cols)),
            sql.SQL(', ').join(sql.Placeholder() * len(cols))
            )

class IngestData:
    def __init__(self,file_path,dbname,user,password,host,port):
        self.file_path = file_path
        self.dbname= dbname
        self.user= user
        self.password= password
        self.host= host
        self.port= port
        self.initialize_db_connection()

    def initialize_db_connection(self):
        self.conn = p.connect(dbname=self.dbname,user=self.user,password=self.password,host=self.host,port=self.port)
        self.cur = self.conn.cursor()

    def get_file_location(self):
        files = glob.glob(self.file_path)
        file_names = glob.iglob(self.file_path)
        locations = []
        for file_name in file_names:
            location_str = str(file_name).split('/')[-1].split('.csv')[0].split('_')[1]
            location_val = int(location_str.replace('d',''))
            locations.append(location_val)
        return files,locations

    def ingest_to_db(self):
        trajectory_table = 'trajectory'
        record_table = 'record'
        trajectory_cols = ['track_id', 'vehicle_type', 'traveled_d','avg_speed','geo_location']
        record_cols = ['track_id','lat','lon','speed','lon_acc','lat_acc','record_time']
        
        files,geo_locations = self.get_file_location()
        for file,location in zip(files,geo_locations):
            df = pd.read_csv(file)
            for i in range(df.shape[0]):
                row = df.iloc[i,0].split(';')
                track_id,trajectory_data = prepare_for_trajectory(row[0:4],location)
                logging.info(trajectory_data)
                sql_trajectory = create_insert_stmt(trajectory_table,trajectory_cols)
                self.cur.execute(sql_trajectory, trajectory_data)
                for i in range(4,len(row),6):
                    if len(row[i:i+6]) != 1:
                        record_data = prepare_for_record(track_id,row[i:i+6])
                        sql_record = create_insert_stmt(record_table,record_cols)
                        logging.info(record_data)
                        self.cur.execute(sql_record, record_data)
                        logging.info("row inserted")
        self.conn.commit()
        self.conn.close()
        logging.info("ingestion successfull")
        
    def create_tables(self,replace=True):
        sql_create_trajectory = "create table trajectory (id int primary key, track_id int , vehicle_type varchar (50), traveled_d float8 check (traveled_d >= 0), avg_speed float8 check(avg_speed >= 0),geo_location int);"
        if replace:
            self.cur.execute("DROP TABLE IF EXISTS record;")
            self.cur.execute("DROP TABLE IF EXISTS trajectory;")
        self.cur.execute(sql_create_trajectory)
        sql_create_record = "create table record (trajectory_id references trajectory (id),track_id int, lat float8, lon float8, speed float8, lon_acc float8, lat_acc float8,record_time float8 check (record_time >= 0));"
        self.cur.execute(sql_create_record)
        self.conn.commit()
        self.conn.close()
    
    def get_last_id(self):
        self.last_id = self.cur.execute("select max(id) from trajectory;")



def main(params):
    user = params.user
    password = params.password
    host = params.host
    port = params.port
    db = params.db
    url = params.url
    file_path = params.file_path
    id = IngestData(file_path,db,user,password,host,port)
    if params.execute == 'ingest':
        id.ingest_to_db()
    elif params.execute == 'rewrite_table':
        id.create_tables()


if __name__ == '__main__':
    # user 
    # password
    # host
    # port
    # database name
    # url of the csv
    # date
    parser = argparse.ArgumentParser(description='Ingest csv data to Postgres')
    parser.add_argument('--user',help='role for postgres',default="root")
    parser.add_argument('--password',help='password for postgres',default="root")
    parser.add_argument('--host',help='host for postgres',default="0.0.0.0")
    parser.add_argument('--port',help='port for postgres',default=5435)
    parser.add_argument('--db',help='database name for postgres',default="traffic_stream_record")
    parser.add_argument('--url',help='url of the csv file',default="root")
    parser.add_argument('--file_path',help='location of csv file',default=r"../data/*.csv")

    parser.add_argument('--execute', choices=['rewrite_table','ingest'], default='ingest',
                        help='specifiy an action to run from rewritting table/ ingesting data')
    
    params = parser.parse_args()
    main(params)
     