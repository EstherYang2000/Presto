import psycopg2
from elasticsearch import Elasticsearch
from es import conn_es, create_index, import_csv_to_elasticsearch, delete_index, es_info_check
from elasticsearch.helpers import bulk
import pandas as pd
import numpy as np

def conn_pg(pg_config):
    try:
        conn = psycopg2.connect(**pg_config)
        print("Connected to PostgreSQL")
        return conn
    except Exception as e:
        print("Error:", e)
        return None

def read_pg(conn, table_name):
    try:
        cursor = conn.cursor()
        query = f"SELECT * FROM {table_name} limit 100000;"
        cursor.execute(query)
        print("Query executed successfully.")
        # Retrieve column names from cursor description
        column_names = [desc[0] for desc in cursor.description]
        print(column_names)
        rows = cursor.fetchall()
        print(len(rows))
        df = pd.DataFrame(rows, columns=column_names)
        df_filled = df.fillna(method='ffill')
        print(df_filled.info())
        # df_filled = df.fillna(value=np.nan)
        df_filled = df_filled.to_dict(orient='records')
        # print(df_filled.info())
        return df_filled
    except Exception as e:
        print("Error:", e)
        return None
    # finally:
    #     if cursor:
    #         cursor.close()
    #     if conn:
    #         conn.close()
# Define a function to prepare the data for bulk insertion
def prepare_data_for_bulk_insertion(rows,index_name):
    for row in rows:
        # Assuming each row is a dictionary with column names as keys
        yield {
            '_index': index_name,
            '_type': '_doc',  # '_type' is deprecated in recent Elasticsearch versions
            '_source': row
        }     
def import_data_from_postgres_to_elasticsearch(conn, es,rows, index_name):
    cursor = conn.cursor()
    try:   
        
    # Iterate over the rows and index them in Elasticsearch
        for row in rows:
        # Assuming the table has columns: id, name, description
        # document = {
        #     'id': row[0],
        #     'name': row[1],
        #     'description': row[2]
        # }
        # Index the document in Elasticsearch
        # Prepare the data for bulk insertion
        # data_for_bulk_insertion = prepare_data_for_bulk_insertion(rows,index_name)
        
        # # # Use the bulk API to insert the data in bulk
        # success, _ = bulk(es, data_for_bulk_insertion, index=index_name)
        
        # print("Data imported successfully from PostgreSQL to Elasticsearch.")
        # print(f"Number of documents indexed: {success}")
            es.index(index=index_name,body=rows)

        print("Data imported successfully from PostgreSQL to Elasticsearch.")

    except Exception as e:
        print("Error:", e)

    finally:
        # Close the cursor and connection
        if cursor:
            cursor.close()
        if conn:
            conn.close()

if __name__ == "__main__":
    
    # Elasticsearch connection settings
    es_config={
        "host":"localhost",
        "port":9200,
        "user":"elastic",
        "password":"elastic"
    }
    # PostgreSQL connection settings
    pg_config = {
        'dbname': 'datahub',
        'user': 'de_intern',
        'password': 'de_intern',
        'host': 'localhost',
        'port': '5433'
    }
    table_name_1 = "data.latest_instagram_post"
    table_name_2 = "data.latest_instagram_profile"
    latest_instagram_post_mapping = {
        "mappings": {
            "properties": {
            "id": {
                "type": "long"
            },
            "platform": {
                "type": "text"
            },
            "platform_user_id": {
                "type": "text"
            },
            "owner_id": {
                "type": "text"
            },
            "platform_post_id": {
                "type": "text"
            },
            "post_time": {
                "type": "text",
            },
            "shortcode": {
                "type": "text"
            },
            "like_count": {
                "type": "long"
            },
            "comment_count": {
                "type": "long"
            },
            "share_count": {
                "type": "long"
            },
            "view_count": {
                "type": "long"
            },
            "play_count": {
                "type": "long"
            },
            "content": {
                "type": "text"
            },
            "url": {
                "type": "text"
            },
            "is_video": {
                "type": "boolean"
            },
            "is_live": {
                "type": "boolean"
            },
            "is_disable_like": {
                "type": "boolean"
            },
            "is_short": {
                "type": "boolean"
            },
            "product_type": {
                "type": "text"
            },
            "edge_media_to_caption": {
                "type": "nested"
            },
            "dimensions": {
                "type": "nested"
            },
            "edge_sidecar_to_children_edges": {
                "type": "nested"
            },
            "display_resources": {
                "type": "nested"
            },
            "edge_media_to_sponsor_user": {
                "type": "nested"
            },
            "gating_info": {
                "type": "nested"
            },
            "fact_check_overall_rating": {
                "type": "nested"
            },
            "fact_check_information": {
                "type": "nested"
            },
            "felix_profile_grid_crop": {
                "type": "nested"
            },
            "dash_info": {
                "type": "nested"
            },
            "thumbnail_resources": {
                "type": "nested"
            },
            "typename": {
                "type": "text"
            },
            "comments_disabled": {
                "type": "boolean"
            },
            "display_url": {
                "type": "text"
            },
            "edge_liked_by_count": {
                "type": "long"
            },
            "location_id": {
                "type": "text"
            },
            "media_preview": {
                "type": "text"
            },
            "owner_username": {
                "type": "text"
            },
            "thumbnail_src": {
                "type": "text"
            },
            "tracking_token": {
                "type": "text"
            },
            "viewer_can_reshare": {
                "type": "boolean"
            },
            "created_at": {
                "type": "text",
            },
            "updated_at": {
                "type": "text",
            },
            "deleted_at": {
                "type": "text",
            },
            "crawled_at": {
                "type": "text",
            }
            }
        }
    }
    es = conn_es(es_config)
    conn = conn_pg(pg_config)
    rows = read_pg(conn, table_name_1)
    delete_index(es, table_name_1)
    create_index(es,table_name_1,latest_instagram_post_mapping)
    import_data_from_postgres_to_elasticsearch(conn, es,rows, table_name_1)
    
