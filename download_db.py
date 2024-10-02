import os
import requests
import gzip
import shutil

# Step 1: Download the .gz file
URL = os.getenv("GZIP_FILE")
headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11'
}
response = requests.get(URL, headers=headers)
gz_file_path = os.path.join("/data", os.getenv("GZIP_FILENAME"))
with open(gz_file_path, 'wb') as f:
    f.write(response.content)


# Step 2: Extract the .gz file to get the .sql file

sql_file_path = os.path.join("/data", os.getenv("SQL_FILENAME"))

with gzip.open(gz_file_path, 'rb') as f_in:
    with open(sql_file_path, 'wb') as f_out:
        shutil.copyfileobj(f_in, f_out)

print(f"Extracted {sql_file_path}")
