import prestodb
conn=prestodb.dbapi.connect(
    host='localhost',
    port=8080,
    user='the-user',
    # catalog='elasticsearch',
    # schema='default',
)
cur = conn.cursor()
query1 = 'SELECT * FROM kol_country_profile LIMIT 10'
query11 = 'SELECT * FROM elasticsearch.default.kol_country_profile LIMIT 10'

query2 = 'SELECT platform, COUNT(*) as platform_count FROM kol_country_profile GROUP BY platform'
query3 = 'SELECT * FROM elasticsearch.default.youtube_profile LIMIT 10'
# query3 = """CREATE TABLE kol_country_profile_copy 
#         WITH (format = \'json\', external_location = \'s3a://presto-test-bucket/kol_country_profile_copy/\') 
#         AS SELECT * FROM kol_country_profile """ 

cur.execute(query11)
rows = cur.fetchall()
print(rows)
print(type(rows))