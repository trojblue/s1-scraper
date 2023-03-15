import csv, json
def json_to_csv(json_file_path, csv_file_path):
    # Read the JSON file
    with open(json_file_path, 'r', encoding="utf-8") as f:
        data = json.load(f)

    # Extract the header from the first row of data
    header = list(data[0].keys())

    # Write the data to the CSV file
    with open(csv_file_path, 'w', newline='', encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=header)
        writer.writeheader()
        for row in data:
            writer.writerow(row)

if __name__ == '__main__':
    name = "forum-6"
    json_to_csv(f"{name}.json", f"{name}.csv")