# airflow-kafka-cassandra-streaming-proj

Introduction:

Constructed a comprehensive end-to-end data engineering pipeline, this project guides through each stage, encompassing data ingestion, processing, and storage. It employs a robust tech stack comprising Apache Airflow, Python, Apache Kafka, Apache Zookeeper, Apache Spark, and Cassandra. The entire system is containerized with Docker.

Technologies Used:

- Apache Airflow
- Python
- Apache Kafka
- Apache Zookeeper
- Apache Spark
- Cassandra
- PostgreSQL
- Docker

The project incorporates the following components:

- Data Source: Utilizes the randomuser.me API to generate random user data for the pipeline.
- Apache Airflow: Orchestrates the pipeline and stores fetched data in a PostgreSQL database.
- Apache Kafka and Zookeeper: Streams data from PostgreSQL to the processing engine.
- Control Center and Schema Registry: Facilitates monitoring and schema management of Kafka streams.
- Apache Spark: Performs data processing with master and worker nodes.
- Cassandra: Serves as the storage for the processed data.

Steps to run the project:

- Starts all container using docker compose file (cmd - docker compose proj-docker-compose.yml -f up -d)
- Go to Control center and create a topic and mention same in kafka producer code
- Navigate to WebServer and iniate the dag execution.
- Run the spark code to ingest data into cassandra
- Check cassandra table if data is ingested or not.




