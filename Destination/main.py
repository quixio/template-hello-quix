import os
from quixstreams import Application
from quixstreams.models.serializers.quix import JSONDeserializer

app = Application.Quix("transformation-v1", auto_offset_reset="latest")

input_topic = app.topic(os.environ["input"], value_deserializer=JSONDeserializer())

sdf = app.dataframe(input_topic)

# write code to publish your data to any destination
# use any Python library you like!

sdf = sdf.update(lambda row: print(row))

if __name__ == "__main__":
    app.run(sdf)