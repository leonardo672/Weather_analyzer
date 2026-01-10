import psycopg2
import pandas as pd
import matplotlib.pyplot as plt
from weather_analyzer.logger import get_logger
from dotenv import load_dotenv
import os
from weather_analyzer.config.settings import settings


logger = get_logger(__name__)

DB_CONFIG = {
    "host": settings.DB_HOST,
    "port": settings.DB_PORT,
    "dbname": settings.DB_NAME,
    "user": settings.DB_USER,
    "password": settings.DB_PASSWORD
}


def fetch_weather_history():
    """Query historical weather data from PostgreSQL"""
    conn = psycopg2.connect(**DB_CONFIG)
    query = """
        SELECT city, temperature, fetched_at
        FROM weather_summary
        ORDER BY fetched_at ASC;
    """
    df = pd.read_sql(query, conn)
    conn.close()
    return df


def plot_temperature_trends(df):
    """Plot temperature trends per city"""
    plt.figure(figsize=(10, 6))

    for city in df['city'].unique():
        city_data = df[df['city'] == city]
        plt.plot(city_data['fetched_at'], city_data['temperature'], marker='o', label=city)

    plt.xlabel("Time")
    plt.ylabel("Temperature (°C)")
    plt.title("Temperature Trends by City")
    plt.xticks(rotation=45)
    plt.legend()
    plt.tight_layout()

    # Save plot
    plt.savefig("plots/temperature.png")
    logger.info("Temperature trend plot saved: plots/temperature.png")
    plt.show()


if __name__ == "__main__":
    df = fetch_weather_history()
    if df.empty:
        logger.warning("No historical data found to plot.")
    else:
        plot_temperature_trends(df)
