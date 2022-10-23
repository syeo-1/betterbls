import concurrent.futures
import multiprocessing
import time

def do_something(a):
    print('sleeping 1 second')
    time.sleep(1)
    print(a)
    print('done sleeping!')

test_list = [i for i in range(0, 501)]

# given a function and data
# split the function to as many processors/threads as possible
# and run the function with each of the split up pieces of data
def threaded_function(func, data):
    # get the total number of available processors
    num_cpus = multiprocessing.cpu_count()

    with concurrent.futures.ThreadPoolExecutor(max_workers=num_cpus) as executor:
        # print(data)
        return executor.map(func, data)
        # for thing in a:
        #     print(thing)

    # assume data is a list

if __name__ == '__main__':    
    # threaded_function(1,2)
    print(test_list)