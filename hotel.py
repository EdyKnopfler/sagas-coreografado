from broker import sagas_service_setup, start_consuming


fly_queue = 'fly'
hotel_queue = 'hotel'
car_queue = 'car'


def on_message(action, data):
    if action == 'proceed':
        print('executing', data)
    else:
        print('reverting', data)
        
    return 'ok'


sagas_service_setup(
    hotel_queue, queue_prev=fly_queue, queue_next=car_queue)

start_consuming(
    hotel_queue, on_message, queue_prev=fly_queue, queue_next=car_queue)