import asyncio

from fastapi import FastAPI, Request
from fastapi.responses import ORJSONResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from settings import get_settings
from logger import get_logger
from core.exceptions import (
    NotFoundError,
    DuplicateEntryError,
    AlreadyExistsError,
    InvalidCredentialsError,
    TokenExpiredError,
    InvalidTokenError,
    InvalidRequestError,
)
from interface.routers import router

from infrastructure.broker.producer import broker_producer
from infrastructure.broker.consumer import broker_consumer


settings = get_settings()
logger = get_logger()


@asynccontextmanager
async def lifespan(app: FastAPI):
    consumer_task = None
    try:
        # Инициализация Kafka Producer
        await broker_producer.open_connection()
        logger.info("Kafka Producer started.")

        # Инициализация Kafka Consumer
        await broker_consumer.open_connection()
        logger.info("Kafka Consumer started.")

        consumer_task = asyncio.create_task(broker_consumer.consume_callback_message())

        yield  # Продолжаем выполнение FastAPI после успешного старта

    except Exception as e:
        logger.error(f"Ошибка при инициализации Kafka: {e}")
        raise  # Повторно выбрасываем исключение, чтобы FastAPI завершился

    finally:
        # Гарантированное закрытие даже при ошибке
        if consumer_task:
            consumer_task.cancel()
            try:
                await consumer_task
            except asyncio.CancelledError:
                logger.info("Consumer task cancelled.")

        await broker_consumer.close_connection()
        logger.info("Kafka Consumer stopped.")

        await broker_producer.close_connection()
        logger.info("Kafka Producer stopped.")

        raise

        

app = FastAPI(
    title=settings.project_name,
    docs_url="/docs",
    openapi_url="/api/openapi.json",
    default_response_class=ORJSONResponse,
    description=settings.project_description,
    version=settings.project_version,
    lifespan=lifespan,
    debug=settings.is_debug_mode,
)


@app.middleware("http")
async def custom_exception_middleware(request: Request, call_next):
    try:
        response = await call_next(request)
        return response
    except NotFoundError as e:
        return JSONResponse(status_code=404, content={"detail": str(e)})
    except DuplicateEntryError as e:
        return JSONResponse(status_code=409, content={"detail": str(e)})
    except AlreadyExistsError as e:
        return JSONResponse(status_code=409, content={"detail": str(e)})
    except InvalidCredentialsError as e:
        return JSONResponse(status_code=401, content={"detail": str(e)})
    except TokenExpiredError as e:
        return JSONResponse(status_code=401, content={"detail": str(e)})
    except InvalidTokenError as e:
        return JSONResponse(status_code=401, content={"detail": str(e)})
    except InvalidRequestError as e:
        return JSONResponse(status_code=400, content={"detail": str(e)})
    except Exception as e:
        logger.error(f"Unhandled error: {e}")
        return JSONResponse(
            status_code=500, content={"detail": "Internal Server Error"}
        )


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(router, prefix="/api")