import ias_client

conn = ias_client.Connection(username="toto",password="tutu")

print(conn.authenticate())
print(conn.authenticate())