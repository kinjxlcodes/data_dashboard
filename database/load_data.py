import json
import psycopg2
from datetime import datetime

# Load JSON data
with open('../data/jsondata.json') as f:
    data = json.load(f)


def handle_empty_integer(value):
    try:
        return int(value) if value != "" else None
    except ValueError:
        return None


def handle_empty_datetime(value):
    if value == "":
        return None
    try:
        return datetime.strptime(value, '%B, %d %Y %H:%M:%S').strftime('%Y-%m-%d %H:%M:%S')
    except ValueError:
        return None


try:
    # Connect to PostgreSQL
    conn = psycopg2.connect(
        dbname="data_dashboard",
        user="postgres",
        password="1234",
        host="localhost"
    )

    cursor = conn.cursor()

    # Insert JSON data into PostgreSQL
    for entry in data:
        end_year = handle_empty_integer(entry['end_year'])
        intensity = handle_empty_integer(entry['intensity'])
        start_year = handle_empty_integer(entry['start_year'])
        impact = handle_empty_integer(entry['impact'])
        relevance = handle_empty_integer(entry['relevance'])
        likelihood = handle_empty_integer(entry['likelihood'])

        added = handle_empty_datetime(entry['added'])
        published = handle_empty_datetime(entry['published'])

        cursor.execute("""
            INSERT INTO insights (end_year, intensity, sector, topic, insight, url, region, start_year, impact, added, published, country, relevance, pestle, source, title, likelihood)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            end_year, intensity, entry['sector'], entry['topic'], entry['insight'], entry['url'], entry['region'],
            start_year, impact, added, published, entry['country'], relevance,
            entry['pestle'], entry['source'], entry['title'], likelihood
        ))

    conn.commit()

except psycopg2.Error as e:
    print(f"Error connecting to PostgreSQL or executing query: {e}")

finally:
    if conn is not None:
        cursor.close()
        conn.close()
