from fastapi import  FastAPI, HTTPException, status, Response
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time 


app = FastAPI()

class Post (BaseModel):
    title: str
    content: str
while True:
    try:
        conn = psycopg2.connect(host = 'localhost', password = 'umair1122', user = 'postgres', dbname = 'postgres', cursor_factory = RealDictCursor )
        cursor = conn.cursor()
        print ('Conncetion successful')
        break
    except Exception as error:
        print ('Connectin to database failed', error)
        time.sleep(3)

my_posts = [{"title": "titile of post 1", "content": "content of post 1", "id" :1}, {"title": "Fav food", "content": "I like eating shawarma", "id": 2}]

def find_post (id):
    for p in my_posts:
        if p ['id'] == id:
            return p

def find_index (id: int):
    for i, p  in enumerate (my_posts):
        if p['id']== id:
            return i 
    return None       

@app.get("/")
def read_root():
    return {"Hello": "Welcome to my api"}

@app.get("/allposts")
def get_posts():
    try:
      cursor.execute("""SELECT * FROM posts""")
      posts= cursor.fetchall()
      return {"data": posts}
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code= status.HTTP_500_INTERNAL_SERVER_ERROR, detail= f'Error found: {e}')
        

@app.post("/post")
def createposts(new_post: Post):
    try:
        cursor.execute("""INSERT INTO posts (content) VALUES (%s) RETURNING * """, (new_post.content,))
        added_post= cursor.fetchall()
        conn.commit()
        return {"data": added_post}
    except Exception as e:
            conn.rollback()
            raise HTTPException(status_code= status.HTTP_500_INTERNAL_SERVER_ERROR, detail= f'Error found: {e}') 

@app.get("/posts/{id}")
def get_post(id: int):
    cursor = conn.cursor()
    try:
     cursor.execute(''' SELECT * FROM posts WHERE id = %s ''', (id,))
     cursor.fetchone()
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code= status.HTTP_500_INTERNAL_SERVER_ERROR, detail= f'ERROR FOUND: {e}')

#Delete Operation 
@app.delete("/posts/{id}")
def deletepost(id: int):
    index = find_index(id)
    if index is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f'Post with id: {id} doesnt found')
    my_posts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
def update_post(id: int, updated_post: Post):
    index = find_index(id)
    if index is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f'Post with id: {id} doesnt found')
    updated_post_dict = updated_post.model_dump()
    updated_post_dict['id']=id
    my_posts[index] = updated_post_dict
    return {"data": updated_post_dict}