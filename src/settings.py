from dotenv import load_dotenv
import os
import certifi

load_dotenv()

SCHEMA_REGISTRY_CONFIG = {
    "url": os.getenv("SCHEMA_REGISTRY_ENDPOINT"),
    "basic.auth.credentials.source": os.getenv(
        "SCHEMA_REGISTRY_CREDENTIALS_SOURCE"
    ),
    "basic.auth.user.info": os.getenv("SCHEMA_REGISTRY_INFO"),
    "ssl.ca.location": certifi.where(),
}
KAFKA_PRODUCER_CONFIG = {
    "bootstrap.servers": os.getenv("BOOTSTRAP_SERVERS"),
    "security.protocol": "SASL_SSL",
    "sasl.mechanisms": "PLAIN",
    "sasl.username": os.getenv("SASL_USERNAME"),
    "sasl.password": os.getenv("SASL_PASSWORD"),
}
