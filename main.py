from fastapi import FastAPI
from pydantic import BaseModel
import psycopg2, time
from fastapi.middleware.cors import CORSMiddleware
# from psycopg2.extras import RealDictCursor
class Temp(BaseModel):
    t: float
    p: float
    a: float

URI = "postgres://shivanshguleria:IBsZzCVWO12f@ep-little-glitter-39121056.ap-southeast-1.aws.neon.tech/neondb"

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins = ["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)
while True:

    try:
        #database_url = 'postgres://my_postgres_k3r8_user:UVNqRtNaXWB8Zbaj2L6kxCPwSUniE5aA@dpg-ck8rumfq54js73ds19mg-a.oregon-postgres.render.com/posts'
        #conn = psycopg2.connect(database_url, sslmode='require', cursor_factory = RealDictCursor)
        conn = psycopg2.connect(URI)
        cursor = conn.cursor()
        print('[INFO]\tDatabase connection was successfull')
        break
    except Exception as error:
        print(f'Connection failed \n Error was {error}')
        time.sleep(2)

@app.get("/")
def root():
    return {"message": "Hello World"}

@app.post("/post")
def post(post: Temp):
    cursor.execute("CREATE TABLE IF NOT EXISTS temp (id serial NOT NULL, temp REAL NOT NULL, pressure REAL NOT NULL, altitude REAL NOT NULL, created_at timestamp  NOT NULL DEFAULT now())")
    cursor.execute("""INSERT INTO temp (temp, pressure, altitude) VALUES (%s, %s, %s) RETURNING * """, (post.t, post.p, post.a))
    post = cursor.fetchone()
    conn.commit()
    return {"data": post}

@app.get("/one")
def get_one():
    cursor.execute("""SELECT temp, pressure, altitude FROM temp ORDER BY id DESC LIMIT 1""")
    post = cursor.fetchone()
    print(post)
    return {"temp": post[0],
            "pressure": post[1],
            "altitude": post[2]
            }

@app.get("/all")
def get_all():
    cursor.execute("""SELECT temp, pressure, altitude, created_at FROM temp""")
    post = cursor.fetchall()
    temp, pressure, altitude, time = [], [], [], []
    for index in range(len(post)): 
        temp.append(post[index][0])
        pressure.append(post[index][1])
        altitude.append(post[index][2])
        time.append(str( post[index][3])[11:19])
    # print(temp)
    # print(altitude)
    # print(pressure)
    return {"temp": temp,
            "altitude": altitude,
            "pressure": pressure,
            "time": time
            }

@app.get("/danger")
def close():
    cursor.execute("DROP TABLE temp")
