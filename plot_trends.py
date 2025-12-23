import psycopg2
import pandas as pd
import matplotlib.pyplot as plt
from logger import get_logger
from dotenv import load_dotenv
import os


logger = get_logger(__name__)

load_dotenv()  # loads variables from .env

DB_CONFIG = {
    "host": os.getenv("DB_HOST"),
    "port": int(os.getenv("DB_PORT", 5432)),
    "dbname": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD")
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
