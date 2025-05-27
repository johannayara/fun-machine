import pandas as pd
import os

CSV_FILES = ["test_geocoded.csv","geocoded_table_1901_clf_v2.csv", "geocoded_table_1923_clf.csv", "geocoded_table_1951_clf_v2.csv"]
def no_dup(filename):
    fixed_filename = os.path.join("fix_data","fix_"+filename)

    df = pd.read_csv(fixed_filename)  

    df.drop_duplicates(inplace=True)

    df.to_csv("a_"+filename, index=False)

for s in CSV_FILES:
    no_dup(s)