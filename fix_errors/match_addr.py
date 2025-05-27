import pandas as pd
from rapidfuzz import process, fuzz
import os

# Load data
ERROR_CSV_FILES = ["test_error.csv","geocode_errors_1901.csv", "geocode_errors_1923.csv", "geocode_errors_1951.csv"]
CSV_FILES = ["test_geocoded.csv","geocoded_table_1901_clf_v2.csv", "geocoded_table_1923_clf.csv", "geocoded_table_1951_clf_v2.csv"]
all_addresses_df = pd.read_csv("lausanne_addresses.csv") 

def correct_geocoding(error_file_name):
    error_file = os.path.join("../geocoding/errors", error_file_name)

    mistyped_df = pd.read_csv(error_file)  

    # Extract list of correct addresses
    all_addresses = all_addresses_df["address"].dropna().tolist()

    # Fuzzy match function
    def find_best_match(mistyped, choices):
        match, score, _ = process.extractOne(mistyped, choices, scorer=fuzz.ratio)
        return pd.Series([match, score], index=["best_match", "match_score"])

    # Apply matching
    results = mistyped_df["LOC"].apply(lambda x: find_best_match(x, all_addresses))

    # Join match results with original mistyped_df
    final_df = pd.concat([mistyped_df, results], axis=1)

    # Filter to only good matches
    good_match = final_df[final_df['match_score'] > 60].copy()
    rate = good_match.shape[0]/mistyped_df.shape[0]
    print(f"good match rate : {rate}")
    # Append Lausanne-specific suffix to best matches

    # Merge coordinates using the best matched address
    all_addresses_df['COOR'] = list(zip(all_addresses_df['latitude'], all_addresses_df['longitude']))
    good_match = good_match.merge(all_addresses_df, left_on='best_match', right_on='address', how='left')
    good_match["best_match"] = good_match["best_match"] + " Lausanne, District de Lausanne, Vaud, Schweiz/Suisse/Svizzera/Svizra"
    
    # Drop unnecessary columns and rename
    good_match.drop(columns=["ERROR", "match_score", "latitude", "longitude", "address"], errors='ignore', inplace=True)
    good_match.rename(columns={"LOC": "mistyped_loc","best_match": "LOC"}, inplace=True)

    # Save result
    good_match.to_csv("fix_"+error_file_name, index=False)

def fill_geocoding(fix_error_file_name, geocoded_file_name):
    fix_df = pd.read_csv(fix_error_file_name)
    geo_path = os.path.join("../geocoding/out", geocoded_file_name)
    geo_df = pd.read_csv(geo_path)  

    result = geo_df.merge(fix_df, left_on='LOC', right_on='mistyped_loc', how='left', suffixes=('', '_new'))
    result.drop(columns=["LOC", "mistyped_loc"], inplace=True)
    result['POS'] = result['POS'].fillna(result['LOC_new'])
    result['COOR'] = result['COOR'].fillna(result['COOR_new'])

    result.drop(columns=["LOC_new", "COOR_new"], inplace=True)
    fixed_filename = os.path.join("fix_data","fix_"+geocoded_file_name)
    result.to_csv(fixed_filename, index=False)


for err,geo in zip(ERROR_CSV_FILES, CSV_FILES):
    correct_geocoding(err)
    fix_filename = "fix_"+ err
    fill_geocoding(fix_filename, geo)




