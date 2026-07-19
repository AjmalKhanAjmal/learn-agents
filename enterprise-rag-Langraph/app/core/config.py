from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Application configuration.

    Values are loaded from .env.
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )

    APP_NAME: str = "Enterprise RAG"

    APP_ENV: str = "development"

    LOG_LEVEL: str = "INFO"

    UPLOAD_DIR: str = "uploads"

    MAX_FILE_SIZE: int = 50 * 1024 * 1024

    CHUNK_SIZE: int = 1000

    CHUNK_OVERLAP: int = 200

    EMBEDDING_MODEL: str

    PINECONE_API_KEY: str

    PINECONE_INDEX: str


@lru_cache
def get_settings() -> Settings:
    """
    Return cached application settings.
    """

    return Settings()


settings = get_settings()




# Interview Note
# What is @lru_cache?

# @lru_cache is a decorator from Python's functools module that stores the result of a function after its first execution.
# When the function is called again with the same arguments, Python returns the cached result instead of executing the
# function again. In FastAPI, it is commonly used with get_settings() to ensure that the Settings object is created 
# only once and reused throughout the application's lifetime. This improves performance, reduces unnecessary object 
# creation, supports lazy initialization, and integrates well with FastAPI's dependency injection and testing patterns.



# pydantic-settings is a library used to manage application configuration in a clean, secure, and production-ready way. Instead of manually reading environment variables using os.getenv() throughout the project, we define all configuration values in a single Settings class. This class automatically loads values from the .env file, converts them to the correct data types, and validates them before the application starts. As a result, the code becomes easier to maintain, more organized, and less error-prone.

# For example, in an Enterprise RAG project, configuration values such as PINECONE_API_KEY, CHUNK_SIZE, EMBEDDING_MODEL, DATABASE_URL, and UPLOAD_DIR are stored in the .env file. Using pydantic-settings, these values are loaded automatically into a Settings object, allowing developers to access them anywhere in the project using settings.CHUNK_SIZE or settings.PINECONE_API_KEY without repeatedly calling os.getenv().

# Another major advantage of pydantic-settings is automatic type conversion. Environment variables are always stored as strings, but this library automatically converts them into the correct Python data types such as int, bool, float, or list. For example, if CHUNK_SIZE=1000 is stored in the .env file, settings.CHUNK_SIZE will automatically be an integer (1000) instead of a string ("1000"). This eliminates the need to manually convert values using functions like int() or bool().

# pydantic-settings also provides built-in validation. If a required configuration value is missing or has an invalid type, the application raises a clear validation error during startup instead of failing later at runtime. This helps developers detect configuration mistakes early and makes debugging much easier.

# From a software engineering perspective, pydantic-settings follows the principle of centralized configuration management. All application settings are defined in one place, making the project more scalable and easier to maintain. If a new configuration value needs to be added, the developer only updates the Settings class and the .env file, rather than modifying multiple files across the project.

# Earlier versions of Pydantic included BaseSettings inside the main pydantic package. However, starting with Pydantic v2, BaseSettings was moved to a separate package called pydantic-settings. Therefore, it must be installed separately using:

# pip install pydantic-settings

# In modern FastAPI and enterprise applications, pydantic-settings is considered the standard approach for configuration management because it provides type safety, validation, centralized configuration, better readability, and improved maintainability. It is widely used in production systems to manage environment variables securely and efficiently.