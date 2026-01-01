import pandas as pd
import psycopg2
import matplotlib.pyplot as plt
from pathlib import Path
from weather_analyzer.logger import get_logger
from dotenv import load_dotenv
import os

logger = get_logger(__name__)

# ----------------------
# PostgreSQL connection
# ----------------------
load_dotenv()  # loads variables from .env

DB_CONFIG = {
    "host": os.getenv("DB_HOST"),
    "port": int(os.getenv("DB_PORT", 5432)),
    "dbname": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD")
}


def fetch_weather_data():
    """Fetch historical weather data from PostgreSQL."""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        query = """
            SELECT city, temperature, humidity, fetched_at
            FROM weather_summary
            ORDER BY fetched_at ASC;
        """
        df = pd.read_sql(query, conn, parse_dates=["fetched_at"])
        conn.close()
        logger.info("Weather data fetched from PostgreSQL successfully.")
        return df
    except Exception as e:
        logger.error(f"Error fetching data from PostgreSQL: {e}")
        return pd.DataFrame()  # return empty DataFrame on failure


# ----------------------
# Analytics
# ----------------------
def compute_trends(df: pd.DataFrame):
    if df.empty:
        logger.warning("No data available for analytics.")
        return None, None

    # 🔑 Force normalization (THIS IS THE FIX)
    df["fetched_at"] = pd.to_datetime(df["fetched_at"], errors="coerce")

    # Drop rows that failed conversion (very important)
    df = df.dropna(subset=["fetched_at"])

    # Create date column safely
    df["date"] = df["fetched_at"].dt.date

    overall_stats = (
        df.groupby("city")["temperature"]
        .agg(["min", "max", "mean"])
        .reset_index()
    )

    daily_stats = (
        df.groupby(["city", "date"])["temperature"]
        .agg(["min", "max", "mean"])
        .reset_index()
    )

    return overall_stats, daily_stats



# ----------------------
# Plotting
# ----------------------
def plot_temperature_trends(daily_stats: pd.DataFrame):
    """Plot min, max, avg temperatures per city over time."""
    if daily_stats is None or daily_stats.empty:
        logger.warning("No data available for plotting.")
        return

    plots_path = Path("plots")
    plots_path.mkdir(parents=True, exist_ok=True)

    cities = daily_stats["city"].unique()

    for city in cities:
        city_data = daily_stats[daily_stats["city"] == city]
        plt.figure(figsize=(10, 5))
        plt.plot(city_data["date"], city_data["min"], label="Min Temp", marker='o')
        plt.plot(city_data["date"], city_data["max"], label="Max Temp", marker='o')
        plt.plot(city_data["date"], city_data["mean"], label="Avg Temp", marker='o')
        plt.title(f"Temperature Trends for {city}")
        plt.xlabel("Date")
        plt.ylabel("Temperature (°C)")
        plt.xticks(rotation=45)
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        file_path = plots_path / f"temperature_trends_{city}.png"
        plt.savefig(file_path)
        plt.close()
        logger.info(f"Temperature trend plot saved: {file_path}")


# ----------------------
# Main
# ----------------------
def main():
    df = fetch_weather_data()
    overall_stats, daily_stats = compute_trends(df)

    if overall_stats is not None:
        logger.info("Overall temperature stats per city:\n" + str(overall_stats))

    plot_temperature_trends(daily_stats)


if __name__ == "__main__":
    main()
