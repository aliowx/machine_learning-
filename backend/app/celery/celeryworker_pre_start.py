import logging 

from tenacity import after_log, before_log, retry, stop_after_attempt, wait_fixed


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

#_______________________________________________

max_tries = 60 * 3  # 3 minutes
wait_seconds = 1

@retry(
    stop=stop_after_attempt(max_tries),
    wait=wait_fixed(wait_seconds),
    before=before_log(logger, logging.INFO),
    after=after_log(logger, logging.WARN),
)
def init() -> None:
    try:
        # Try to create session to check if DB is awake
        # db = SessionLocal()
        # db.execute("SELECT 1")
        ...
    except Exception as e:
        logger.error(e)
        raise e


def main() -> None:
    logger.info("Initializing services")
    init()
    logger.info("Service finished initializing")


if __name__ == "__main__":
    main()
