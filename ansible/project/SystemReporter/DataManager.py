import psutil
import datetime
from SystemReporter.Row import Row
from SystemReporter.util_methods import Average, bytes2human
PLACEHOLDER = "--"


class DataManager:

    def __init__(self):
        self.rows = []  # All rows to be written : instances of Row
        self.disk_last_values = []  # Disk starting values to show the difference every row [Read count, Write Count]
        self.network_last_values = []  # Network starting values to show the difference every row [bytes sent,
        # bytes received]
        self.cpu_count = psutil.cpu_count()
        self.summary_data = {"CPU": {"Total": [], "Cores": [[] for _ in range(self.cpu_count)]},
                             "MEMORY": []}

    def get_rows(self):
        return self.rows

    def new_row(self, data):
        """
        Creates and appends an instance of Row into the self.rows list[]
        @param data:
        @return:
        """
        self.rows.append(Row(data))

    def prepare_data(self, cpu, memory, disk, network):
        """
        Prepares data with only the necessary information

        @param cpu: List[cpu total, list[core1,core2,...]]
        @param memory: Tuple(total, used,...)
        @param disk: Tuple()
        @param network: Tuple()
        @return: None
        """
        data = []

        time_now = datetime.datetime.now()
        data.append(time_now.strftime("%m/%d/%Y, %H:%M:%S"))

        cleaned_cpu = self.prepare_cpu_data(cpu)
        data.extend(cleaned_cpu)

        cleaned_memory = self.prepare_memory_data(memory)
        data.append(cleaned_memory)

        cleaned_disk = self.prepare_disk_data(disk)
        data.extend(cleaned_disk)

        cleaned_network = self.prepare_network_data(network)
        data.extend(cleaned_network)

        # If no value in row replace with placeholder
        for i, item in enumerate(data):
            if item is None:
                data[i] = PLACEHOLDER

        self.new_row(data)

    def prepare_summary_rows(self, summary_data):
        max_row = ["Max", summary_data["CPU"]["Total"]["Max"]]
        min_row = ["Min", summary_data["CPU"]["Total"]["Min"]]
        avg_row = ["Avg", summary_data["CPU"]["Total"]["Avg"]]
        for key, value in summary_data["CPU"]["Cores"].items():
            max_row.append(value["Max"])
            min_row.append(value["Min"])
            avg_row.append(value["Avg"])

        max_row.append(summary_data["MEMORY"]["Max"])
        min_row.append(summary_data["MEMORY"]["Min"])
        avg_row.append(summary_data["MEMORY"]["Avg"])

        return [max_row, min_row, avg_row]

    def create_summary(self):
        """
        Creates a summary of all data
        @return: summary: list[]
        """
        core_summary = {}
        for index, core in enumerate(self.summary_data["CPU"]["Cores"]):
            core_summary[f"Core {index + 1}"] = {"Max": max(core),
                                                 "Min": min(core),
                                                 "Avg": Average(core)}

        summary_data = {
            "CPU":
                {"Total": {"Max": max(self.summary_data["CPU"]["Total"]),
                           "Min": min(self.summary_data["CPU"]["Total"]),
                           "Avg": Average(self.summary_data["CPU"]["Total"])}

                    , "Cores": core_summary
                 }

            , "MEMORY":
                {"Max": max(self.summary_data["MEMORY"]),
                 "Min": min(self.summary_data["MEMORY"]),
                 "Avg": Average(self.summary_data["MEMORY"])}
        }

        return self.prepare_summary_rows(summary_data)

    def prepare_cpu_data(self, data):
        """
        Cleans memory data received from psutils
        @param data: List[cpu total, list[core1,core2,...]]

        @return: list[cpu total, core1,core2,...]
        """

        cpu_total_value = data[0]
        cpu_core_values = data[1]
        self.summary_data["CPU"]["Total"].append(cpu_total_value)  # Add CPU total value to summary data

        # Add each core value to the summary data
        for index, core_value in enumerate(cpu_core_values):
            self.summary_data["CPU"]["Cores"][index].append(core_value)

        cpu_data = [cpu_total_value]  # Total Cpu
        cpu_data.extend(cpu_core_values)  # All Cores
        return cpu_data

    def prepare_memory_data(self, data):
        """
        Cleans memory data received from psutils
        @param data: Tuple(total, used,...)
        @return: Memory Total usage %
        """

        memory_total = data.percent  # memory % in use
        self.summary_data["MEMORY"].append(memory_total)
        memory_data = memory_total
        return memory_data

    def prepare_disk_data(self, data):
        """
        Cleans disk data received from psutils
        @param data: Tuple()
        @return: list[]
        """

        if not self.disk_last_values:
            self.disk_last_values = [data.read_count, data.write_count]
            disk_data = [data.read_time, data.write_time, data.read_count, data.write_count]
            return disk_data

        read_count_difference = data.read_count - self.disk_last_values[0]
        write_count_difference = data.write_count - self.disk_last_values[1]
        disk_data = [data.read_time, data.write_time, read_count_difference, write_count_difference]
        self.disk_last_values = [data.read_count, data.write_count]
        return disk_data

    def prepare_network_data(self, data):
        """
        Cleans network data received from psutils
        @param data: Tuple()
        @return: list[]
        """

        if not self.network_last_values:
            self.network_last_values = [data.bytes_sent, data.bytes_recv, data.dropin]
            network_data = [bytes2human(data.bytes_sent), bytes2human(data.bytes_recv), data.errin, data.errout,
                            data.dropin, data.dropout]
            return network_data

        bytes_sent_difference = data.bytes_sent - self.network_last_values[0]
        bytes_received_difference = data.bytes_recv - self.network_last_values[1]
        dropin_difference = data.dropin - self.network_last_values[2]

        network_data = [bytes_sent_difference, bytes_received_difference, data.errin,
                        data.errout,
                        dropin_difference,
                        data.dropout]

        self.network_last_values = [data.bytes_sent, data.bytes_recv, data.dropin]
        return network_data
