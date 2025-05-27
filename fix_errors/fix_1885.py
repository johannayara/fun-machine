import pandas as pd
import os

table = os.path.join("../geocoding/out","geocoded_table_1885_clf_v2.csv")

df = pd.read_csv(table)

null_pos_entries = df[df['POS'].isna()]
null_pos_entries = null_pos_entries.drop(columns=["COOR", "POS","job","job_clf","salaire"])
null_pos_entries["ERROR"]= "No result or retry failed"
error_path = os.path.join("../geocoding/errors","geocode_errors_1885.csv")
null_pos_entries.to_csv(error_path, index=False)

