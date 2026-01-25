import requests
import sqlite3
import random


def connect():
    """Create and return a database connection."""
    connection = sqlite3.connect("countries.db")
    return connection


def create_table():
    """Create the Countries table if it doesn't exist."""
    connection = None
    try:
        connection = connect()
        cursor = connection.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Countries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name VARCHAR(100) NOT NULL,
                capital VARCHAR(100),
                flag VARCHAR(10),
                subregion VARCHAR(100),
                population INTEGER
            )
        """)
        connection.commit()
        cursor.close()
        print("Table ready.")
    except Exception as e:
        print(f"Error creating table: {e}")
    finally:
        if connection:
            connection.close()


def fetch_all_countries():
    """Fetch all countries from the REST Countries API."""
    url = "https://restcountries.com/v3.1/all"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error fetching data: {response.status_code}")
        return []


def get_random_countries(countries, count=10):
    """Select random countries from the list."""
    return random.sample(countries, count)


def extract_country_data(country):
    """Extract the required fields from a country object."""
    name = country.get("name", {}).get("common", "Unknown")

    # Capital is a list, get the first one
    capital_list = country.get("capital", [])
    if capital_list:
        capital = capital_list[0]
    else:
        capital = None

    flag = country.get("flag", "")
    subregion = country.get("subregion", None)
    population = country.get("population", 0)

    return (name, capital, flag, subregion, population)


def save_countries_to_db(countries):
    """Save countries to the database."""
    connection = None
    try:
        connection = connect()
        cursor = connection.cursor()

        query = """
            INSERT INTO Countries (name, capital, flag, subregion, population)
            VALUES (?, ?, ?, ?, ?)
        """

        for country in countries:
            data = extract_country_data(country)
            cursor.execute(query, data)
            print(f"Added: {data[0]}")

        connection.commit()
        cursor.close()
        print(f"\nSuccessfully added {len(countries)} countries to the database.")

    except Exception as e:
        print(f"Error saving to database: {e}")
    finally:
        if connection:
            connection.close()


def main():
    print("Setting up database...")
    create_table()

    print("Fetching countries from API...")
    all_countries = fetch_all_countries()

    if not all_countries:
        print("No countries fetched.")
        return

    print(f"Fetched {len(all_countries)} countries.")

    random_countries = get_random_countries(all_countries, 10)
    print(f"Selected 10 random countries.\n")

    save_countries_to_db(random_countries)


if __name__ == "__main__":
    main()
