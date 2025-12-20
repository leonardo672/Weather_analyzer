import pandas as pd
import matplotlib.pyplot as plt

CSV_PATH = "data/history/weather_summary.csv"

def plot_temperature():
    df = pd.read_csv(CSV_PATH)

    # Convert fetched_at to datetime
    df["fetched_at"] = pd.to_datetime(df["fetched_at"])

    # Plot temperature per city
    for city in df["city"].unique():
        city_data = df[df["city"] == city]
        plt.plot(city_data["fetched_at"], city_data["temperature"], marker="o", label=city)

    plt.xlabel("Time")
    plt.ylabel("Temperature (°C)")
    plt.title("Temperature per City Over Time")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()

    plt.show()


if __name__ == "__main__":
    plot_temperature()
