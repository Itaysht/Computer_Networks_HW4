import numpy as np
import queue
import threading
import heapq

packet_count = 0
dropped_packets = 0

def simulateLoadBalancer():
    # Simulation parameter

    # Simulation parameters
    x = 200  # packets per time unit
    simulation_time = 5000  # Total time to simulate
    current_time = 0

    # Server configuration
    server_probabilities = [0.2, 0.8]
    service_rates = [20, 190]
    max_queue_length = [2, 10]

    # Initialize queues and tracking variables
    server_queues = [queue.Queue(maxsize=max_queue_length[i]) for i in range(len(server_probabilities))]

    total_wait_time = 0

    terminate_event = threading.Event()
    lock = threading.Lock()

    # Function to handle server processing
    def server_thread(server_id):
        global packet_count
        while True:
            try:
                # Wait for a packet to process
                # arrival_time = server_queues[server_id].get()
                #service_time = np.random.exponential(1 / service_rates[server_id])
                #time.sleep(service_time)
                server_queues[server_id].get(timeout=1)
                with lock:
                    packet_count += 1
                # with lock:
                #     global current_time
                #     total_wait_time += (current_time - arrival_time)
                #     packet_count += 1
            except queue.Empty:
                if terminate_event.is_set():
                    break

    def load_balancer_thread():
        global dropped_packets
        current_time = 0
        while current_time < simulation_time:
            working = np.random.exponential(1 / x)
            #time.sleep(working)
            current_time += working
            server_id = np.random.choice(len(server_probabilities), p=server_probabilities)

            # Ensure that we lock access to the queues to avoid race conditions
            with lock:
                if not server_queues[server_id].full():
                    server_queues[server_id].put(current_time)
                else:
                    dropped_packets += 1

            print(current_time)

        terminate_event.set()

    threads = []
    for i in range(len(server_probabilities)):
        t = threading.Thread(target=server_thread, args=(i,))
        t.start()
        threads.append(t)
    t = threading.Thread(target=load_balancer_thread)
    t.start()
    threads.append(t)

    for t in threads:
        t.join()  # Wait for threads to complete

    # Calculate average wait time
    # average_wait_time = total_wait_time / packet_count if packet_count > 0 else 0

    # Print results
    print(f"Simulation over {simulation_time} time units (continuous time)")
    print(f"Rate of incoming packets: {x} packets/time unit")
    print(f"Total dropped packets: {dropped_packets}")
    print(f"Accepted packets: {packet_count}")
    # print(f"Average wait time per packet: {average_wait_time:.2f} time units")


if __name__ == "__main__":
    simulateLoadBalancer()