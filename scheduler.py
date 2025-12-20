import schedule
import time
from main import main
from logger import get_logger

logger = get_logger(__name__)

def job():
    logger.info("Scheduled job started")

    main(
        cities=["Stockholm", "London", "New York"],
        output="data/history/weather_summary.csv",  # historical CSV
        raw_output="data/history/raw"               # folder for raw JSON history
    )

    logger.info("Scheduled job finished")


# Schedule the job
# Run every day at 01:48
schedule.every().day.at("02:20").do(job)

# Alternative: run every 1 hour
# schedule.every(1).hours.do(job)

logger.info("Scheduler started. Waiting for jobs...")

while True:
    schedule.run_pending()
    time.sleep(60)  # check every minute
