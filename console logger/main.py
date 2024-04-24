import os

# import our get_app function to help with building the app for local/Quix deployed code
from app_factory import get_app

# get the environment variable value or default to False
USE_LOCAL_KAFKA = os.getenv("use_local_kafka", False)

# Create an Application.
app = get_app(consumer_group="my-first-consumer-group", use_local_kafka=USE_LOCAL_KAFKA)

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
