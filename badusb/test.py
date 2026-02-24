if event.type == ecodes.EV_KEY and event.value == 1:
    current_time = time.time()

    if last_time is not None:
        delay = current_time - last_time
        print("Delay:", delay)

    last_time = current_time