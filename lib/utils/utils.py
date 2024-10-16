

def fit_range(value:float, old_min:float, old_max:float, new_min:float, new_max:float):
    return_val = new_min + (value - old_min) * (new_max - new_min) / (old_max - old_min)
    return return_val