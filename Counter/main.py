import os
from quixstreams import Application, State
from quixstreams.models.serializers.quix import QuixDeserializer, QuixTimeseriesSerializer


app = Application.Quix("transformation-v1", auto_offset_reset="latest")

input_topic = app.topic(os.environ["input"], value_deserializer=QuixDeserializer())
output_topic = app.topic(os.environ["output"], value_serializer=QuixTimeseriesSerializer())

sdf = app.dataframe(input_topic)

def count_names(row: dict, state: State):

    # get the value from the name column for this row
    # so we can see if it's in state
    name = row["name"]

    # check state, if the name is already there then retrieve the count
    # default to 0 if the name wasn't in state
    name_count = state.get(name, 0)

    # add one to the name count
    name_count += 1

    # store the new count in state
    state.set(name, name_count)

    pass

sdf = sdf.apply(count_names)

sdf = sdf.update(lambda row: print(row))

sdf = sdf.to_topic(output_topic)

if __name__ == "__main__":
    app.run(sdf)