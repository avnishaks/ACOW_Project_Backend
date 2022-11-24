import sqlalchemy.orm as _orm
import  database as _database , models as _models,  schemas as _schemas


# Creating DataBase
def create_database():
    return _database.Base.metadata.create_all(bind=_database.engine)

# Getting Connection with DB
def get_db():
    db=_database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Getting information for the E-mail
def get_user_by_email(db: _orm.Session, email: str):
    return db.query(_models.User).filter(_models.User.email == email).first()


#Create a User
def create_user(db: _orm.Session, user: _schemas.UserCreate):
    fake_hashed_password = user.password + "thisisnotsecure"
    db_user = _models.User(email=user.email, hashed_password=fake_hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# To get the List of User

def get_all_users(db: _orm.Session, skip: int = 0, limit: int = 100):
    return db.query(_models.User).offset(skip).limit(limit).all()

# To get the user based on id

def get_user_by_id(db: _orm.Session, user_id: int):
    return db.query(_models.User).filter(_models.User.id == user_id).first()

# Create the Post

def create_post(db: _orm.Session, post: _schemas.PostCreate, user_id: int):
    post = _models.Post(**post.dict(), owner_id=user_id)
    db.add(post)
    db.commit()
    db.refresh(post)
    return post


# Get the List of ALl the Post

def get_posts(db: _orm.Session, skip: int = 0, limit: int = 10):
    return db.query(_models.Post).offset(skip).limit(limit).all()

# Get the post by post id

def get_post(db: _orm.Session, post_id: int):
    return db.query(_models.Post).filter(_models.Post.id == post_id).first()

#Delete the Post

def delete_post(db: _orm.Session, post_id: int):
    db.query(_models.Post).filter(_models.Post.id == post_id).delete()
    db.commit()