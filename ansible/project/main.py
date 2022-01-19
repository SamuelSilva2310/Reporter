import os.path
import signal
import psutil
import datetime
import time
import argparse


from SystemReporter.DataManager import DataManager
from SystemReporter.Exporter import Exporter


def handle_args():
    """
    Handles all arguments when executing the code using a parser

    @return: parser arguments and the parser itself
    """
    parser = argparse.ArgumentParser(description='Resource Reporter')
    parser.add_argument('-o', '--output', dest='output_path', help='Output location and filename', required=True)
    parser.add_argument('-p', '--period', dest='period', help='Time period in seconds between each data query',
                        required=True)

    return parser.parse_args(), parser


class GracefulKiller:
    kill_now = False

    def __init__(self):
        signal.signal(signal.SIGINT, self.exit_gracefully)
        signal.signal(signal.SIGTERM, self.exit_gracefully)

    def exit_gracefully(self, *args):
        self.kill_now = True


if __name__ == '__main__':
    killer = GracefulKiller()
    arguments, parser = handle_args()
    start_time = time.time()
    data_manager = DataManager()

    print(os.getpid())
    if not os.path.exists("Output"):
        os.mkdir("Output")

    while not killer.kill_now:
        print("Adding Data: ", datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
        cpu = [psutil.cpu_percent(interval=0.1), psutil.cpu_percent(interval=0.1, percpu=True)]
        memory = psutil.virtual_memory()
        disk = psutil.disk_io_counters()
        network = psutil.net_io_counters()

        data_manager.prepare_data(cpu, memory, disk, network)

        # Time sleep before each check
        time.sleep(int(arguments.period) - ((time.time() - start_time) % int(arguments.period)))

    # Save Data into a .csv when exiting gracefully
    exporter = Exporter(data_manager)
    exporter.export(arguments.output_path)
    print("[END] Gracefully Killed, FILE SAVED")
