# process_jobs.py
import pandas as pd

def process_job_data(input_file, output_file, top_n=20):
    df = pd.read_csv(input_file)

    # Normalize column names and job field
    df.columns = [col.lower().strip() for col in df.columns]
    if 'job' not in df.columns:
        raise ValueError(f"'job' column not found in {input_file}")

    # Count job frequencies
    top_jobs = df['job'].str.strip().value_counts().head(top_n).reset_index()
    top_jobs.columns = ['job', 'count']

    # Save to CSV
    top_jobs.to_csv(output_file, index=False)
    print(f"Saved top {top_n} jobs to {output_file}")

# Process both years
process_job_data('final_table_1901_clf.csv', 'top_jobs1901.csv', top_n=50)
process_job_data('final_table_1923_clf.csv', 'top_jobs1923.csv', top_n=50)
process_job_data('data/table_1951.csv', 'top_jobs1951.csv', top_n=50)
process_job_data('final_table_1885_clf.csv', 'top_jobs1885.csv', top_n=50)
