import pandas as pd
from concurrent.futures import ThreadPoolExecutor

class MapReduce:
    def __init__(self, num_threads):
        self.num = num_threads

    def map(self, data):
        # create a dictionary to store and count
        counts = {}

        # Traverse the list and count
        for i in data:
            if i in counts:
                counts[i] += 1
            else:
                counts[i] = 1

        return counts

    def reduce(self, counts_list):
        # create a list to count
        counts = {}

        # count
        for i in counts_list:

            for name, count in i.items():
                if name in counts:
                    counts[name] += count
                else:
                    counts[name] = count

        return counts

    def map_reduce(self, data):
        # split the subset
        sub_size = len(data) // self.num
        subsets = [data[i:i+sub_size] for i in range(0, len(data), sub_size)]

        # create the threadpool
        with ThreadPoolExecutor(max_workers=self.num) as executor:
            # Concurrent execution of each map
            map_data = executor.map(self.map, subsets)

        # execute the reduce and merge
        reduce_data = self.reduce(map_data)

        return reduce_data

# read file
dataset = pd.read_csv('AComp_Passenger_data_no_error_DateTime.csv')

# select the passenger list
data_column = dataset.iloc[:, 0]

# turn to list
data = data_column.tolist()

# set the process
num_processes = 2

# create object
count_times = MapReduce(num_processes)

# conduct the mapreduce
result = count_times.map_reduce(data)

max_count = max(result.values())
most_frequent_passenger = [(number, count) for number, count in result.items() if count == max_count]

for number, count in most_frequent_passenger:
    print(f"Passenger:{number}")
    print(f"times:{count}")