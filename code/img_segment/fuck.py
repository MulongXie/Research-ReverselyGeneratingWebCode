import pandas as pd

# Creating the first Dataframe using dictionary
df1 = df = pd.DataFrame()

# Creating the Second Dataframe using dictionary
df2 = pd.DataFrame({"a": [1, 2, 3],
                    "b": [5, 6, 7]})

# Print df1
print(df1, "\n")

print(df1.append(df2))