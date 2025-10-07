
def str_int_flat_dict(cheeky_dict: dict):
    well_mannered_dict = {key: {"N": str(value)} for key, value in cheeky_dict.items()}
    return well_mannered_dict
