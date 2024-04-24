# Import additional modules as needed
import pandas as pd
import random
import json
import time
import os

# import our get_app function to help with building the app for local/Quix deployed code
from app_factory import get_app

# import the dotenv module to load environment variables from a file
from dotenv import load_dotenv

load_dotenv(override=False)

# get the environment variable value or default to False
USE_LOCAL_KAFKA = os.getenv("use_local_kafka", False)

# Create an Application.
app = get_app(use_local_kafka=USE_LOCAL_KAFKA)

# Define the topic using the "output" environment variable
topic_name = os.environ["output"]
topic = app.topic(topic_name)

# Get the directory of the current script
script_dir = os.path.dirname(os.path.realpath(__file__))
# Construct the path to the CSV file
csv_file_path = os.path.join(script_dir, "demo-data.csv")


# this function loads the file and sends each row to the publisher
def read_csv_file(file_path: str):
    """
    A function to read data from a CSV file in an endless manner.
    It returns a generator with stream_id and rows
    """

    # Read the CSV file into a pandas.DataFrame
    print("CSV file loading.")
    df = pd.read_csv(file_path)

    print("File loaded.")

    # Get the number of rows in the dataFrame for printing out later
    row_count = len(df)

    # Generate a unique ID for this data stream.
    # It will be used as a message key in Kafka
    stream_id = f"CSV_DATA_{str(random.randint(1, 100)).zfill(3)}"

    # Get the column headers as a list
    headers = df.columns.tolist()

    # Continuously loop over the data
    while True:
        # Print a message to the console for each iteration
        print(f"Publishing {row_count} rows.")

        # Iterate over the rows and convert them to
        for _, row in df.iterrows():
            time.sleep(0.25)  # wait a little before sending more data

            # Create a dictionary that includes both column headers and row values
            row_data = {header: row[header] for header in headers}

            # add a new timestamp column with the current data and time
            row_data["Timestamp"] = time.time_ns()

            # Yield the stream ID and the row data
            yield stream_id, row_data

        print("All rows published")

        # Wait a moment before outputting more data.
        time.sleep(1)


def main():
    """
    Read data from the CSV file and publish it to Kafka
    """

    # Create a pre-configured Producer object.
    # Producer is already setup to use Quix brokers.
    # It will also ensure that the topics exist before producing to them if
    # Application.Quix is initiliazed with "auto_create_topics=True".

    with app.get_producer() as producer:
        # Iterate over the data from CSV file
        for message_key, row_data in read_csv_file(file_path=csv_file_path):
            json_data = json.dumps(row_data)
            # publish the data to the topic
            producer.produce(
                topic=topic.name,
                key=message_key,
                value=json_data,
            )


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Exiting.")
