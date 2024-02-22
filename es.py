from elasticsearch import Elasticsearch
import os 
import csv
import pandas as pd
import numpy as np
def conn_es(es_config):
    """
    Establish a connection to Elasticsearch using the provided configuration.

    Args:
        es_config (dict): Dictionary containing Elasticsearch connection configuration.
                          Should include 'host', 'port', 'user', 'password'.

    Returns:
        Elasticsearch: Elasticsearch client instance.
    """
    
    host = es_config['host']
    port = es_config['port']
    user = es_config['user']
    pwd = es_config['password']
    es = Elasticsearch(
        [f"http://{host}:{port}"],
        basic_auth=(f'{user}', f'{pwd}'),
        verify_certs=False,
        request_timeout=60
    )

    return es
def create_index_content(table_str:str):
    """
    Generate the Elasticsearch index mapping based on the schema configuration.

    Args:
        table_str (str): Name of the table for which the index mapping is generated.

    Returns:
        dict: Elasticsearch index mapping.
    """
    configPath_str = os.path.join(os.getcwd(),"schema",table_str,f"{table_str}.yaml")
    
    # schema_config = IACConfigHelper.get_conn_info(configPath_str)
    # Generate Elasticsearch index mapping
    index_mapping = {
        "mappings": {
            "properties": {}
        }
    }
    for column in schema_config["columns"]:
        field_name = column["name"]
        field_type = column["type"]
        # Handle specific field types or transformations if needed
        if field_type == "text":
            field_mapping = {"type": "text"}
        elif field_type == "boolean":
            field_mapping = {"type": "boolean"}
        elif field_type == "bigint":
            field_mapping = {"type": "double"}
        elif field_type == "double precision":
            field_mapping = {"type": "double"}
        elif field_type == "jsonb":
            field_mapping = {"type": "object"}
        elif field_type == "bytea":
            field_mapping = {"type": "binary"}
        else:
            # Default to text type if no specific mapping is defined
            field_mapping = {"type": "text"}

        index_mapping["mappings"]["properties"][field_name] = field_mapping
    return index_mapping
def create_index(es,index_name,index_mapping):
    # try:
        # Check if the index already exists
    if not es.indices.exists(index=index_name):
        # Create the index with mapping and settings
        # index_mapping = create_index_content(index_name)
        es.indices.create(index=index_name, body=index_mapping)
        print(f"Index '{index_name}' created successfully.")
    else:
        print(f"Index '{index_name}' already exists.")
    # except Exception as e:
    #     print(f"An error occurred: {e}")
def es_info_check(es):
    client_version = pkg_resources.get_distribution("elasticsearch").version
    print(client_version)
    print(es.ping())
    print(es.cluster.health())
    print(es.info())       
def import_csv_to_elasticsearch(es,csv_file, index_name):

    df = pd.read_csv(csv_file)
    # df['biography'].fillna('Unknown', inplace=True)
    # df['platform_name'].fillna('Unknown', inplace=True)
    df['country'].fillna('Unknown', inplace=True)
    df["total_video_count"] = pd.to_numeric(df["total_video_count"], errors="coerce")
    df["total_view_count"] = pd.to_numeric(df["total_view_count"], errors="coerce")
    df["follower_count"] = pd.to_numeric(df["follower_count"], errors="coerce")
    # Generate random numbers for 'id' column
    random_ids = np.random.randint(1000, 999999, size=len(df))  # Generating random digit numbers
    # Assign random ids to the DataFrame
    df['id'] = random_ids
    data = df.to_dict(orient='records')
    print(df.info())
    # print(data)
    # Index documents into Elasticsearch
    for doc in data:
        try:
            es.index(index=index_name, body=doc)
        except Exception as e:
            print(f"Error indexing document: {e}")

def delete_index(es, index_name):
    """
    Delete an Elasticsearch index with the specified name.

    Args:
        es: Elasticsearch client.
        index_name (str): Name of the index to be deleted.
    """

    try:
        es.indices.delete(index=index_name, ignore=[400, 404])
        print(f"Index '{index_name}' deleted successfully.")
    except Exception as e:
        print(f"Error deleting index '{index_name}': {e}")     

if __name__ == "__main__":
    es_config={
        "host":"localhost",
        "port":9200,
        "user":"elastic",
        "password":"elastic"
    }
    csv_file_path = 'youtube_profile.csv'
    index_name = 'youtube_profile'
    kol_country_profile_mapping = {
        "mappings": {
            "properties": {
                "kol_id": {"type": "keyword"},
                "name": {"type": "text"},
                "radar_url": {"type": "text"},
                "country": {"type": "keyword"},
                "idx": {"type": "integer"},
                "platform_user_id": {"type": "keyword"},
                "platform": {"type": "keyword"},
                "biography": {"type": "text"},
                "platform_name": {"type": "keyword"}
            }
        }
    }
    kol_scoring_mapping ={
            "mappings": {
                "properties": {
                "kol_id": {
                    "type": "keyword"
                },
                "score": {
                    "type": "double"
                },
                "score_type": {
                    "type": "text"
                },
                "country": {
                    "type": "text"
                },
                "platform": {
                    "type": "text"
                }
                }
            }
            }
    mapping3={
            "mappings": {
                "properties": {
                "id": {
                    "type": "text"
                },
                "platform": {
                    "type": "text"
                },
                "platform_user_id": {
                    "type": "keyword"
                },
                "country": {
                    "type": "text"
                },
                "name": {
                    "type": "text"
                },
                "total_video_count": {
                    "type": "long"
                },
                "total_view_count": {
                    "type": "long"
                },
                "follower_count": {
                    "type": "long"
                }
                }
            }
            }


    es = conn_es(es_config)
    # delete_index(es, index_name)
    # es_info_check(es)
    # es = Elasticsearch([{'host': 'localhost', 'port':9200, 'scheme':'http'}])
    # url = "http://localhost:9200"
    # es =  Elasticsearch([url], basic_auth=("elastic", "elastic"))
    create_index(es,index_name,mapping3)
    for i in range(0,10000):
        print(i)
        import_csv_to_elasticsearch(es,csv_file_path, index_name)