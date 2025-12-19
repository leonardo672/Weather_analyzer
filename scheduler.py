import schedule
import time
from main import main
from logger import get_logger

logger = get_logger(__name__)


def job():
    logger.info("Scheduled job started")

    main(
        cities=["Stockholm", "London", "New York"],
        output="data/weather_summary.csv",
        raw_output="data/raw_weather.json"
    )

    logger.info("Scheduled job finished")


# Schedule the job
# run every day at 06:20
schedule.every().day.at("17:28").do(job)

# Alternative:
# schedule.every(1).hours.do(job)

logger.info("Scheduler started. Waiting for jobs...")

while True:
    schedule.run_pending()
    time.sleep(60)  # check every minute
