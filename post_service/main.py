from fastapi import FastAPI,HttpException, Depends,status
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from typing import List, Opcional
from jose import JWTError, jwt
from pathlib import Path


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

current_file_path = Path(__file__).resolve()

start_hub_root = current_file_path.parent.parent / "StartHub"
public_key_path = start_hub_root / "login" / "src" / "main" / "recurces" / "certs" / "public.pem"

try:
    with open(public_key_path, "r") as f:
        public_key = f.read()
except FileNotFoundError:
    raise FileNotFoundError(f"Public key file not found at {public_key_path}. Please ensure the file exists.")

ALGORITHM = "RS256"

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HttpException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, public_key, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    return username


class PostBase(BaseModel):
    title: str
    content: str

class PostCreate(PostBase):
    pass

class Post(PostBase):
    id: int
    owner: str


posts_db = {
    1: Post(id=1, title="First Post", content="Content of the first post", owner="user1"),
    2: Post(id=2, title="Second Post", content="Content of the second post", owner="user2"),
}

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Welcome to the Post API!"}

@app.get("/posts/", response_model=List[Post])
def get_posts():
    return list(posts_db.values())

@app.post("/posts/{post_id}", response_model=Post)
def get_post(post_id: int):
    post = posts_db.get(post_id)
    if post is None:
        raise HttpException(status_code=404, detail="Post not found")
    return post

@app.post("/posts", response_model=Post,status_code=status.HTTP_201_CREATED)
def create_post(post: PostCreate, current_user: str = Depends(get_current_user)):
    new_id = max(posts_db.keys()) + 1 if posts_db else 1
    new_post = Post(id=new_id, title=post.title, content=post.content, owner=current_user)
    posts_db[new_id] = new_post
    return new_post
