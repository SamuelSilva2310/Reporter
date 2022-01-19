import os
import csv
import config


def get_headers():

    headers = config.headers
    fieldnames = []
    for header in headers:
        if header == "CPU":

            cpu_count = headers[header]

            fieldnames.append("CPU%")
            for i in range(1, cpu_count + 1):
                fieldnames.append(f"Core {i} %")
        else:

            for item in headers[header]:
                fieldnames.append(item)

    return fieldnames


class Exporter:

    def __init__(self, data_manager):
        self.rows = []
        self.data_manager = data_manager

    def export(self, filename):

        self.rows = self.data_manager.get_rows()

        output_dir = os.path.join(config.OUTPUT_DIR_CSV)

        if not os.path.exists(output_dir):
            os.mkdir(output_dir)
        file_path = os.path.join(output_dir, f"{filename}.csv")

        fieldnames = get_headers()
        with open(file_path, 'w', newline='') as csv_file:
            writer = csv.writer(csv_file)

            writer.writerow(fieldnames)

            # 1st row doesnt need to be written
            for row in self.rows[1:]:
                writer.writerow(row.data)
