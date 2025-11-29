import pandas as pd
import random
import string

def random_name(size=6):
    return ''.join(random.choices(string.ascii_uppercase, k=size))

def generate_large_data(num_rows=10000):
    data = {
        "Name": [random_name() for _ in range(num_rows)],
        "Score": [random.randint(0, 100) for _ in range(num_rows)],
    }
    df = pd.DataFrame(data)
    df.to_csv("data.csv", index=False)
    print(f"Generated data.csv with {num_rows} rows.")

if __name__ == "__main__":
    generate_large_data(10000)  # generate 10,000 rows
