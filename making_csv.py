import os
import pandas as pd

# --- Configuration ---
INPUT_FOLDER = 'Processed_Resumes_Txt' # The folder created by the previous script
OUTPUT_CSV_FILE = 'resumes_from_txt.csv' # Name for the new CSV file
# --- End Configuration ---

filenames = []
resume_data = []

# Check if the input folder exists
if not os.path.isdir(INPUT_FOLDER):
    print(f"Error: Input folder '{INPUT_FOLDER}' not found.")
    print(f"Current directory: {os.getcwd()}")
    print("Please make sure the script is in the correct directory and the previous script ran successfully.")
else:
    print(f"Reading text files from: '{INPUT_FOLDER}'")
    processed_count = 0
    failed_count = 0

    # List all files directly in the input folder
    try:
        all_files = os.listdir(INPUT_FOLDER)
    except Exception as e:
        print(f"Error listing files in {INPUT_FOLDER}: {e}")
        all_files = []

    for filename in all_files:
        # Process only .txt files
        if filename.lower().endswith('.txt'):
            file_path = os.path.join(INPUT_FOLDER, filename)
            # print(f"  Reading: {filename}") # Optional: uncomment for verbose logging
            try:
                # Read the entire content of the text file
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()

                # Append filename and content to lists
                filenames.append(filename)
                resume_data.append(content)
                processed_count += 1

            except FileNotFoundError:
                print(f"    Error: File not found at {file_path}")
                failed_count += 1
            except UnicodeDecodeError:
                print(f"    Error: Could not decode file {filename} with UTF-8. Trying 'latin-1'.")
                # Try reading with a different encoding as a fallback
                try:
                     with open(file_path, 'r', encoding='latin-1') as f:
                         content = f.read()
                     filenames.append(filename)
                     resume_data.append(content)
                     processed_count += 1
                except Exception as e_alt:
                     print(f"    Error: Failed to read {filename} with alternative encoding: {e_alt}")
                     failed_count += 1
            except Exception as e:
                print(f"    Error reading file {filename}: {e}")
                failed_count += 1
        else:
            # Optionally log skipped non-txt files
            # print(f"  Skipping non-txt file: {filename}")
            pass

    # Check if any data was collected
    if filenames and resume_data:
        # Create a pandas DataFrame
        df = pd.DataFrame({
            'Filename': filenames,
            'Data': resume_data
        })

        # Save the DataFrame to a CSV file
        try:
            df.to_csv(OUTPUT_CSV_FILE, index=False, encoding='utf-8')
            print(f"\nSuccessfully created CSV file: '{OUTPUT_CSV_FILE}'")
            print(f"Total text files processed: {processed_count}")
            if failed_count > 0:
                print(f"Files failed to read: {failed_count}")

            # --- Updated Preview ---
            print("\nFirst 5 rows of the CSV (basic print):")
            # Use basic print(df.head()) which doesn't require 'tabulate'
            print(df.head())
            # --- End Updated Preview ---

        except Exception as e:
            print(f"\nError saving DataFrame to CSV '{OUTPUT_CSV_FILE}': {e}")
    else:
        print("\nNo text files were successfully processed. CSV file not created.")
        if failed_count > 0:
             print(f"Files failed to read: {failed_count}")

