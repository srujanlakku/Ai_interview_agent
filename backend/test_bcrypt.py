
from passlib.context import CryptContext
import logging

# Setup logging manually since we aren't using the app's config
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def test_hash():
    password = "Srujan@123"
    print(f"Testing hash for: '{password}' (len={len(password)})")
    try:
        hashed = pwd_context.hash(password)
        print(f"Success! Hash: {hashed}")
        return True
    except Exception as e:
        print(f"Failed! Error: {e}")
        return False

if __name__ == "__main__":
    test_hash()
