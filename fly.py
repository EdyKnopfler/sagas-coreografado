from broker import sagas_service_setup, start_consuming


fly_queue = 'fly'
hotel_queue = 'hotel'


def on_message(action, data):
    if action == 'proceed':
        print('executing', data)
    else:
        print('reverting', data)

    return 'ok'


sagas_service_setup(fly_queue, queue_next=hotel_queue)
start_consuming(fly_queue, on_message, queue_next=hotel_queue)