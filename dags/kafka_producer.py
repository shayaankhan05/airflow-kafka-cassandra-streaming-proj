import uuid
from datetime import datetime, timedelta
import json
from airflow import DAG
from airflow.operators.python import PythonOperator

# Default Args for our DAG
default_args = {
    'owner': 'Shayaan',
    'start_date' : datetime(2024, 2, 27)
}

def get_data():
    # Request package to get data from random user api
    import requests
    response = requests.get("https://randomuser.me/api/")

    # printing raw data that we got from api
    print(response)
    
    # Converting response into json format data
    json_data = response.json()

    # Getting only user related information from response
    res = json_data['results'][0]

    return res

def format_data(res):
    data = {}

    location = res['location']
    data['id'] = str(uuid.uuid4())
    data['first_name'] = res['name']['first']
    data['last_name'] = res['name']['last']
    data['gender'] = res['gender']
    data['address'] = f"{str(location['street']['number'])} {location['street']['name']}, " \
                      f"{location['city']}, {location['state']}, {location['country']}"
    data['post_code'] = location['postcode']
    data['email'] = res['email']
    data['username'] = res['login']['username']
    data['dob'] = res['dob']['date']
    data['registered_date'] = res['registered']['date']
    data['phone'] = res['phone']
    data['picture'] = res['picture']['medium']

    return (data)


def stream_data():
    from kafka import KafkaProducer
    import time
    import logging

    producer = KafkaProducer(bootstrap_servers='broker:29092')
    curr_time = time.time()

    while True:
        # To ingest data for a period of 1 minute
        if time.time() > curr_time + 60:
            break
        try:
            raw_data = get_data()
            formatted_data = format_data(raw_data)
            
            # convertong formatted dict data into json data, encoding and publishing to topic
            producer.send('test', json.dumps(formatted_data).encode('utf-8'))

        except Exception as e:
            logging.error(f"Couldn't get data from api due to following error: {e}")
            continue


# DAG Object Creation
# dag = DAG(
#     'airflow-spark-cassandra-project',
#     default_args = default_args,
#     schedule_interval = timedelta(days=1)
# )


# stream_data_task = PythonOperator(
#     task_id = 'get_data_from_api',
#     python_callable = stream_data(),
#     dag = dag
# )

# dag.add_task(stream_data_task)

with DAG('airflow-spark-cassandra-project',
         default_args=default_args,
         schedule_interval = timedelta(days=1),
         catchup=False) as dag:

    streaming_task = PythonOperator(
        task_id='get_data_from_api',
        python_callable=stream_data
    )
