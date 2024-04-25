import os
from quixstreams import Application, State

# import the dotenv module to load environment variables from a file
from dotenv import load_dotenv
load_dotenv(override=False)

# Create an Application.
app = Application(
    broker_address=os.getenv("KAFKA_BROKER_ADDRESS"),
    consumer_group="name-counter-group",
    auto_offset_reset="earliest",
    auto_create_topics=True,
    use_changelog_topics=False,
)

input_topic = app.topic(os.environ["input"])
output_topic = app.topic(os.environ["output"])

sdf = app.dataframe(input_topic)


def count_names(row: dict, state: State):
    # get the value from the name column for this row
    # so we can see if it's in state
    name = row["Name"]

    # check state, if the name is already there then retrieve the count
    # default to 0 if the name wasn't in state
    name_count = state.get(name, 0)

    # add one to the name count
    name_count += 1

    # add the name count to the row data
    row["count"] = name_count

    # store the new count in state
    state.set(name, name_count)

    # return the updated row so more processing can be done on it
    return row


# apply the result of the count_names function to the row
sdf = sdf.apply(count_names, stateful=True)

# print the row with this inline function
sdf = sdf.update(lambda row: print(row))

# publish the updated row to the output topic
sdf = sdf.to_topic(output_topic)

if __name__ == "__main__":
    app.run(sdf)
