from passlib.context import CryptContext

#here we are telling passlib to use bcrypt to hash our passwords
# deprecated="auto" means that it will use the most secure algorithm available
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password):
    return pwd_context.hash(password)