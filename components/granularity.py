def granularity_freq(granularity):
    if granularity == 'Week':
        freq = 'W'
    elif granularity == 'Month':
        freq = 'ME'
    elif granularity == 'Quarter':
        freq = 'QE'
    elif granularity == 'Year':
        freq = 'YE'
    else:
        freq = 'ME'  # Default to Monthly if granularity is not recognized
    return freq