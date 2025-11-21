from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from pydantic import BaseModel

# Configuration for JWT
# The algorithm should match what your Spring Boot application uses to sign tokens
ALGORITHM = "RS256" 

# Load the public key from the file system.
# In a production environment, you might load this from an environment variable or a secure vault.
PUBLIC_KEY = """-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAoOrDJBjqTl2ARzcRZJrQ
gyYkJ9f4ytqtLD6xfuvpmAJWVaFipoU6invRrkrNkxQ4i3R1OR1jWmMsTlPrOaMC
YNhXZnSyM+VRI+M5M2PYX0YwEIBgmO/LodKPmwB88Zm2AeR5n+Qpnbq9RENcXkcl
Ic6OQETJhggTrzVpP4aLP6jqzD3xrZpASOXRL/fhC68YX2eZs0w90QJ4doKMjuz1
Lw/cZ7jbJtuofgYVKsdBXms1X8r2N/YmQlXA2usgKnaW4XZ1KkQboOOGXvekTCEP
aS/VQuorK/5qGJ12pKKO9RQAeobDOKmWrnVcUaTPfzrmh0yRekVR+xJvAz32/LzO
oQIDAQAB
-----END PUBLIC KEY-----"""

# OAuth2PasswordBearer will handle extracting the token from the Authorization header
# The tokenUrl parameter points to the endpoint where clients can get a token (your Spring Boot login)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="http://localhost:8080/process-login")

class TokenData(BaseModel):
    user_id: int | None = None

class User(BaseModel):
    id: int
    # You might add other user fields here if they are in the JWT payload
    # username: str
    # email: str

def decode_access_token(token: str) -> TokenData:
    """
    Decodes and validates a JWT token.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        # Decode the token using the public key and algorithm
        payload = jwt.decode(token, PUBLIC_KEY, algorithms=[ALGORITHM])
        
        # The 'sub' (subject) claim typically holds the user identifier
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
        token_data = TokenData(user_id=int(user_id))
    except JWTError:
        raise credentials_exception
    return token_data

async def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    """
    Dependency to get the current authenticated user.
    """
    token_data = decode_access_token(token)
    if token_data.user_id is None:
        raise HTTPException(status_code=400, detail="User not found in token")
    
    # In a real application, you might fetch user details from a database
    # or another microservice using this user_id.
    # For now, we'll just create a dummy User object.
    user = User(id=token_data.user_id) 
    return user
