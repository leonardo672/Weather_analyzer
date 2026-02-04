import schedule
import time
import subprocess
import sys
from pathlib import Path

from weather_analyzer.main import main
from weather_analyzer.plotting.plot_trends_postgres import (
    fetch_weather_data,
    compute_trends,
    plot_temperature_trends
)
from weather_analyzer.logger import get_logger
from weather_analyzer.config.settings import settings

logger = get_logger(__name__)

# Ensure plots folder exists
Path("plots").mkdir(parents=True, exist_ok=True)

CITIES = settings.CITIES


def job():
    logger.info("Scheduled job started")

    try:
        # 1️⃣ Run weather ingestion pipeline
        main(
            cities=CITIES,
            raw_output="data/history/raw"
        )

        # 2️⃣ Fetch historical data
        df = fetch_weather_data()
        if df.empty:
            logger.warning("No historical data available.")
            return

        # 3️⃣ Analytics
        overall_stats, daily_stats = compute_trends(df)

        logger.info("Weather analytics computed successfully.")
        logger.info(f"\nOverall stats:\n{overall_stats}")

        # 4️⃣ Analytics plots
        plot_temperature_trends(daily_stats)

        # 5️⃣ Run plot_trends.py USING VENV PYTHON
        logger.info("Running plot_trends.py (city temperature over time)")
        subprocess.run(
            [
                sys.executable,
                "-m",
                "weather_analyzer.plotting.plot_trends",
            ],
            check=True
        )

        logger.info("Scheduled job finished successfully")

    except Exception:
        logger.exception("Scheduled job failed")


schedule.every().day.at("21:32").do(job)
# schedule.every(10).minutes.do(job)

logger.info("Scheduler started. Waiting for jobs...")

while True:
    schedule.run_pending()
    time.sleep(60)