import numpy as np
#import plotly.graph_objects as go
import heapq

def running_average(new_value, current_average, count):
    return (current_average * count + new_value) / (count + 1)

def get_highest_time_in_heap_with_given_id(heap, id):
    filtered = [item for item in heap if item[1] == id]
    if not filtered:
        return 0
    result = max(filtered)[0]
    return result

def load_balancer(simulation_time, server_probabilities, rateIn, max_queue_length, service_rates):
    max_queue_length = [m + 1 for m in max_queue_length]
    cur_queue_length = [0, 0]
    time_of_finished_packages = []
    index_of_loader = -1

    packet_count = 0
    dropped_packets = 0

    waiting_time_count = 0
    waiting_time_average = 0
    service_time_count = 0
    service_time_average = 0

    current_time, server_id_from_queue = 0, index_of_loader
    while current_time <= simulation_time:

        if server_id_from_queue == index_of_loader:
            working = np.random.exponential(1 / rateIn)
            heapq.heappush(time_of_finished_packages, (current_time + working, index_of_loader))

            server_id = np.random.choice(len(server_probabilities), p=server_probabilities)

            if cur_queue_length[server_id] < max_queue_length[server_id]:
                server_working = np.random.exponential(1 / service_rates[server_id])

                latest_server_id_finished_time = get_highest_time_in_heap_with_given_id(time_of_finished_packages, server_id)
                if latest_server_id_finished_time != 0:
                    finish_time = latest_server_id_finished_time + server_working

                    waiting_time_average = running_average(latest_server_id_finished_time - current_time,
                                                           waiting_time_average, waiting_time_count)
                else:
                    finish_time = current_time + server_working

                    waiting_time_average = running_average(0, waiting_time_average, waiting_time_count)

                heapq.heappush(time_of_finished_packages, (finish_time, server_id))
                cur_queue_length[server_id] += 1

                waiting_time_count += 1
                service_time_average = running_average(server_working, service_time_average, service_time_count)
                service_time_count += 1
            else:
                dropped_packets += 1

        elif cur_queue_length[server_id_from_queue] > 0:
                packet_count += 1
                cur_queue_length[server_id_from_queue] -= 1

        current_time, server_id_from_queue = heapq.heappop(time_of_finished_packages)

    last_time_finished = current_time
    while time_of_finished_packages:
        last_time_finished, serv = heapq.heappop(time_of_finished_packages)
        packet_count += 1
    return packet_count, dropped_packets, last_time_finished, waiting_time_average, service_time_average



if __name__ == "__main__":
    simulation_time = 5000
    probs, rateIn, length_of_queues, ratesOut = [0.2,0.8], 200, [2,10], [20,190]
    recieved, dropped, last_finish, avg_waiting, avg_service = load_balancer(simulation_time, probs, rateIn, length_of_queues, ratesOut)

    print(f"{recieved} {dropped} {last_finish} {avg_waiting} {avg_service}")

    #
    #
    # simulations_time = [10, 100, 500, 1000, 2000, 2500]
    # result = []
    #
    # for simulate in simulations_time:
    #     temp_avg_waiting, temp_avg_service = 0,0
    #     for i in range(10):
    #         _, _, _, avg_waiting, avg_service = load_balancer(simulate, probs, rateIn, length_of_queues, ratesOut)
    #         temp_avg_waiting = running_average(avg_waiting, temp_avg_waiting, i)
    #         temp_avg_service = running_average(avg_service, temp_avg_service, i)
    #
    #     result.append(temp_avg_service + temp_avg_waiting)
    #
    # print(result)
    #
    # fig = go.Figure(data=go.Scatter(x=simulations_time, y=result, mode='lines+markers'))
    #
    # fig.update_layout(title='Delay time as function of Simulation time',
    #                   xaxis_title='Simulation Time',
    #                   yaxis_title='Delay Time')
    #
    # fig.show()

