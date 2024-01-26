import os
from quixstreams import Application
from quixstreams.models.serializers.quix import JSONDeserializer

app = Application.Quix("destination-v1", auto_offset_reset="latest")

input_topic = app.topic(os.environ["input"], value_deserializer=JSONDeserializer())

sdf = app.dataframe(input_topic)

print(" ")
print(" ")
print(" ")
print("-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~")
print("Publish this data to your destination\nWrite any Python code you need and use any Python library you fancy!")
print("-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~")
print(" ")
print(" ")
print(" ")


def publish_to_destination(row: dict):
    # write code to publish your data to any destination
    # use any Python library you like!

    print(row)

sdf = sdf.apply(publish_to_destination)

if __name__ == "__main__":
    app.run(sdf)