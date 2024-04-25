import os
from quixstreams import Application

# import the dotenv module to load environment variables from a file
from dotenv import load_dotenv

load_dotenv(override=False)
# Create an Application.
app = Application(
    broker_address=os.getenv("KAFKA_BROKER_ADDRESS"),
    consumer_group="console-logger-group",
    auto_offset_reset="earliest",
    auto_create_topics=True,
)

# create the input topic object and use a JSON deserializer
input_topic = app.topic(os.environ["input"])

sdf = app.dataframe(input_topic)

print(" ")
print(" ")
print(" ")
print("-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~")
print("Publish this data to your destination")
print("Write any Python code you need and use any Python library you fancy!")
print("-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~")
print(" ")
print(" ")
print(" ")


def publish_to_destination(row: dict):
    # write code to publish your data to any destination
    # use any Python library you like!
    print("-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~")
    print("This is one row of your data")
    print("Transform it here or publish it to an external data store")
    print(row)
    print("-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~")


sdf = sdf.apply(publish_to_destination)

if __name__ == "__main__":
    app.run(sdf)
