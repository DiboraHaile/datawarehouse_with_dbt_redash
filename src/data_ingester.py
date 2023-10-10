import pandas as pd
import glob
import sys
import psycopg2 as p
from psycopg2 import sql
sys.path.append("../data/")

def get_file_location(file_path):
    files = glob.glob(file_path)
    file_names = glob.iglob(file_path)
    locations = []
    for file_name in file_names:
        location_str = str(file_name).split('/')[-1].split('.csv')[0].split('_')[1]
        location_val = int(location_str.replace('d',''))
        locations.append(location_val)
    return files,locations


def prepare_for_record(track_id,value_list):
    record_list = []
    stripped = [*map(lambda x: x.strip(),value_list)]
    record_list.append(track_id)
    print()
    record_list.extend([*map(float,stripped[:7])])
    return record_list
    
def prepare_for_trajectory(value_list,location):
    trajectory_list = []
    stripped = [*map(lambda x: x.strip(),value_list)]
    track_id = int(stripped[0])
    float_values = [*map(float,stripped[2:4])]
    trajectory_list.append(track_id)
    trajectory_list.append(stripped[1])
    trajectory_list.extend(float_values)
    trajectory_list.append(location)
    return track_id,trajectory_list


def ingest_to_db(file_path = r'../data/*.csv'):
    conn = p.connect(dbname="traffic_stream_record",user="root",password="root",host='0.0.0.0',port=32771)
    cur = conn.cursor()

    trajectory_table = 'trajectory'
    record_table = 'record'
    trajectory_cols = ['track_id', 'vehicle_type', 'traveled_d','avg_speed','geo_location']
    record_cols = ['track_id','lat','lon','speed','lon_acc','lat_acc','record_time']
    
    files,geo_locations = get_file_location(file_path)
    for file,location in zip(files,geo_locations):
        df = pd.read_csv(file)
        for i in range(df.shape[0]):
            row = df.iloc[i,0].split(';')
            track_id,trajectory_data = prepare_for_trajectory(row[0:4],location)
            print(trajectory_data)
            sql_trajectory = create_insert_stmt(trajectory_table,trajectory_cols)
            cur.execute(sql_trajectory, trajectory_data)
            for i in range(4,len(row),6):
                if len(row[i:i+6]) != 1:
                    record_data = prepare_for_record(track_id,row[i:i+6])
                    sql_record = create_insert_stmt(record_table,record_cols)
                    print(record_data)
                    cur.execute(sql_record, record_data)
    conn.commit()
    conn.close()
    
def create_tables(replace=True):
    conn = p.connect(dbname="traffic_stream_record",user="root",password="root",host='0.0.0.0',port=32771)
    cur = conn.cursor()
    sql_create_trajectory = "create table trajectory (track_id int primary key, vehicle_type varchar (50), traveled_d float8 check (traveled_d >= 0), avg_speed float8 check(avg_speed >= 0),geo_location int);"
    if replace:
        cur.execute("DROP TABLE IF EXISTS record;")
        cur.execute("DROP TABLE IF EXISTS trajectory;")
    cur.execute(sql_create_trajectory)
    sql_create_record = "create table record (track_id int references trajectory (track_id), lat float8, lon float8, speed float8, lon_acc float8, lat_acc float8,record_time float8 check (record_time >= 0));"
    cur.execute(sql_create_record)
    conn.commit()
    conn.close()

def create_insert_stmt(table_name,cols):
    return sql.SQL("INSERT INTO {} ({}) VALUES ({})").format(
            sql.Identifier(table_name),
            sql.SQL(', ').join(map(sql.Identifier, cols)),
            sql.SQL(', ').join(sql.Placeholder() * len(cols))
            )