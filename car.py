from broker import sagas_service_setup, start_consuming


hotel_queue = 'hotel'
car_queue = 'car'


def on_message(action, data):
    raise Exception('crashed')


sagas_service_setup(car_queue, queue_prev=hotel_queue)
start_consuming(car_queue, on_message, queue_prev=hotel_queue)