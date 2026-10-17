# step - 1:
#python .\app\tests\test_opensearch_connection.py



import os
from opensearchpy import OpenSearch

# password = os.getenv("OPENSEARCH_PASSWORD")

password = 'MyStrongPass123!ChangeMe'




# if not password:
#     raise RuntimeError(
#         "Set the OPENSEARCH_PASSWORD environment variable first."
#     )

# client = OpenSearch(
#     hosts=[{"host": "localhost", "port": 9200}],
#     http_auth=("admin", password),
#     use_ssl=True,
#     verify_certs=False,  # Local development only
#     ssl_show_warn=False,
# )

# print(client.info())
# print(client.cluster.health())
# client.close()




# from opensearchpy import OpenSearch

# client = OpenSearch(
#     hosts=[{"host": "127.0.0.1", "port": 9201}],
#     use_ssl=False,
#     verify_certs=False,
#     timeout=30,
# )

# print("Connected:", client.ping())

# info = client.info()

# print("Cluster:", info["cluster_name"])
# print("Version:", info["version"]["number"])




from opensearchpy import OpenSearch

client = OpenSearch(
    hosts=[{"host": "127.0.0.1", "port": 9201}],
    use_ssl=False,
    verify_certs=False,
    timeout=30,
)

print("Connected:", client.ping())

info = client.info()

print("Cluster:", info["cluster_name"])
print("Version:", info["version"]["number"])