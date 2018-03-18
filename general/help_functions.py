def get_subdictionary(full_dict,key):
    sub_dict = {}
    for k,v in full_dict.items():
        if k!=key:
            sub_dict[k] = v
    return sub_dict

def get_category(categories,key,val):
    for k,v in categories[key].items():
        if v==int(val):
            return k

def convert(sample,convert_rules):
    for col in sample.iteritems():
        states = convert_rules[col[0]]
        code = states[col[1]]
        sample[col[0]] = code

    return sample