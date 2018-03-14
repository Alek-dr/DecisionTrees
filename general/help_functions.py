
def get_subdictionary(full_dict,key):
    sub_dict = {}
    for k,v in full_dict.items():
        if k!=key:
            sub_dict[k] = v
    return sub_dict