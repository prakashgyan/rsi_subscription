import os
import psycopg2
from sqlalchemy import create_engine
import pandas as pd


DATABASE_URL = 'postgres://oumqflqnjhmvoz:9443bb2f405fc1b5803946ed1dfac3a5e1c2c8f324d76f132aca5ec3e4dbbf86@ec2-54-78-127-245.eu-west-1.compute.amazonaws.com:5432/d3hoanoeqnpsoa'
engine = create_engine(DATABASE_URL)
# conn = psycopg2.connect(DATABASE_URL, sslmode='require')

# c = conn.cursor()

# c.execute('show all')
# print(c.fetchall())
# conn.close()

with engine.connect() as conn:
    result = conn.execute(f"select * from stocks ")
        # return pd.DataFrame(c.fetchall(),columns=column_names)
    x = pd.DataFrame(result)
    print(x)

# print(os.environ['DATABSE_URL'])