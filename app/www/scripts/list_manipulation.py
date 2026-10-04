# Working with lists using the rows of csv/fruits.csv.
from scripts.get_csv import _read_fruits



# Returns every row of fruits.csv: [{"id": "1", "fruit": "melon"}, ...]
def upload_fruits(body=None):
    try:
        fruits = _read_fruits()
    except FileNotFoundError:
        raise FileNotFoundError("fruits.csv not found")
    if not fruits:
        raise ValueError("no fruits found")
    return fruits


# Counts how many times one fruit appears. The body is just a string, e.g. "apple".
def count_fruit(body):
    target = body
    fruits = upload_fruits()
    # A generator gives 1 for every matching row; sum() adds them up.
    count = sum(1 for row in fruits if row["fruit"] == target)
    if count == 0:
        return {"error": f'{target} not found'}

    return {"fruit": target, "count": count}

# Builds a new list with one {"id", "description"} item per fruit.
def prepare_data(body=None):
    prepared =[]
    fruits= upload_fruits(None)
    print(fruits)

    for fruit in fruits:
        prepared.append({
            "id" : fruit['id'],
            "description": fruit["fruit"] + " is a sort of fruit"
        })
    return prepared
