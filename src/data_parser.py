
from datetime import datetime
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

def date_parser(date_string):
    date_string = "20181024"
    date_format = "%Y%m%d"
    # Convert string to date
    date_object = datetime.strptime(date_string, date_format).date()
    return date_object

def time_parser(time_string):
    time_string = "0930"
    time_format = "%H%M"
    # Convert string to time
    return datetime.strptime(time_string, time_format).time()