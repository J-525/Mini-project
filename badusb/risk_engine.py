import statistics
import config
import sus

def evaluate_risk(delays, total_keys, backspace_count):
    risk = 0

    if len(delays) < config.WINDOW_SIZE:
        return 0,False

    avg_delay = statistics.mean(delays)
    std_dev = statistics.stdev(delays) if len(delays) > 1 else 0
    mistake_ratio = backspace_count / total_keys if total_keys else 0
    keys_per_sec = len(delays) / sum(delays) if avg_delay > 0 else 0

    #print(mistake_ratio)

    if avg_delay < config.AVG_DELAY_THRESHOLD:
        risk += 3

    if std_dev < config.STD_DEV_THRESHOLD:
        risk += 3

    if keys_per_sec > config.BURST_THRESHOLD:
        risk += 4

    if mistake_ratio < config.MISTAKE_RATIO_MIN:
        risk += 2

    if sus.is_sus:
        #print(risk)
        risk += 5

    alert = risk >= config.RISK_THRESHOLD
    
    pauses = [delay for delay in delays if delay > config.PAUSE_THRESHOLD]
    pauces_ratio = len(pauses) / len(delays) if delays else 0

    if pauces_ratio < config.PAUSE_RATIO_THRESHOLD:
        #print(risk)
        risk += 2

    rythm_ratio=std_dev / avg_delay if avg_delay > 0 else 0

    if rythm_ratio < config.RYTHM_THRESHOLD:
        #print(risk)
        risk += 2
    
    #alert = risk >= config.RISK_THRESHOLD

    return risk,alert


'''if __name__ == "__main__":
    # Example usage
    example_delays = [0.01, 0.02, 0.015, 0.01, 0.02, 0.015, 0.01, 0.02]
    total_keys = 8
    backspace_count = 0

    risk, alert = evaluate_risk(example_delays, total_keys, backspace_count)
    print(f"Risk Level: {risk}, Alert: {alert}")'''