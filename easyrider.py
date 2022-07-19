import json
import re


def all_errors_func(data_json):  # check data format according to documentation
    bus_id, stop_id, stop_name, next_stop, stop_type, a_time = 0, 0, 0, 0, 0, 0
    sn_template = '(^[A-Z].+) (Road|Avenue|Boulevard|Street)$'
    at_template = r'^[0-2]\d:[0-5]\d$'
    for item in data_json:
        if isinstance(item['bus_id'], int) is False or item['bus_id'] == '':
            bus_id += 1
        if isinstance(item['stop_id'], int) is False or item['stop_id'] == '':
            stop_id += 1
        if item['stop_name'] == '' or isinstance(item['stop_name'], str) is False or re.match(sn_template, item['stop_name']) is None:
            stop_name += 1
        if isinstance(item['next_stop'], int) is False or item['next_stop'] == '':
            next_stop += 1
        if item['stop_type'] not in ['S', 'O', 'F'] and item['stop_type'] != '':
            stop_type += 1
        if isinstance(item['a_time'], str) is False or item['a_time'] == '' or re.match(at_template, item['a_time']) is None:
            a_time += 1
    a = f'''Type and required field validation: {bus_id + stop_id + stop_name + stop_type + a_time}\n\
bus_id: {bus_id}\nstop_id: {stop_id}\nstop_name: {stop_name}\nnext_stop: {next_stop}\nstop_type: {stop_type}\n\
a_time: {a_time}'''
    return a


def lists_creation(data_json, name):  # create lists from json data
    new_list = []
    for item in data_json:
        new_list.append(item[name])
    return new_list


def count_st_by_bus(data_json):  # count stops by bus_id
    bl_dict, s = {}, ''
    bus_id_list = lists_creation(data_json, 'bus_id')
    for i in set(bus_id_list):
        n = bus_id_list.count(i)
        bl_dict.update({i: n})
    for obj in bl_dict.items():
        s += f'bus_id: {obj[0]}, stops: {obj[1]}\n'
    a = f'''Line names and number of stops:\n{s}'''
    return a


def count_stops(data_json):
    stop_type_list, stop_name_list = lists_creation(data_json, 'stop_type'), lists_creation(data_json, 'stop_name')
    start_s_list, finish_s_list, tr_s_list = [], [], []
    for a, b in zip(stop_type_list, stop_name_list):
        if a == 'S':
            start_s_list.append(b)
        elif a == 'F':
            finish_s_list.append(b)
    for i in stop_name_list:
        if stop_name_list.count(i) > 1:
            tr_s_list.append(i)
    start_s_list = sorted(list(set(start_s_list)))
    tr_s_list = sorted(list(set(tr_s_list)))
    finish_s_list = sorted(list(set(finish_s_list)))
    a = f'''Start stops: {len(start_s_list)} {start_s_list}\n\
Transfer stops: {len(tr_s_list)} {tr_s_list}\nFinish stops: {len(finish_s_list)} {finish_s_list}'''
    return a


def time_test(data_json):  # Arrival time test
    bus_index, bl_dict, s = '', {}, ''
    bus_id_list, a_time_list = lists_creation(data_json, 'bus_id'), lists_creation(data_json, 'a_time')
    stop_name_list = lists_creation(data_json, 'stop_name')
    for i in set(bus_id_list):
        bus_index = bus_id_list.index(i)
        bus_index_new = bus_index + 1
        while i == bus_id_list[bus_index_new]:
            if a_time_list[bus_index_new] <= a_time_list[bus_index]:
                bl_dict.update({i: stop_name_list[bus_index_new]})
                break
            bus_index += 1
            bus_index_new += 1
            if bus_index_new > (len(bus_id_list) - 1):
                break
    if bl_dict != {}:
        for obj in bl_dict.items():
            s = f'bus id line {obj[0]}: wrong time on station {obj[1]}\n'
        a = f'''Arrival time test:\n{s}'''
    else:
        a = '''Arrival time test:\nOK'''
    return a


def dem_stops_test(data_json):  # On demand stop test
    stop_name_list = lists_creation(data_json, 'stop_name')
    stop_type_list = lists_creation(data_json, 'stop_type')
    temp_list, wrong_st_list = [], []
    for i in set(stop_name_list):
        for a, b in zip(stop_name_list, stop_type_list):
            if a == i:
                temp_list.append(b)
        if ('S' in temp_list or 'F' in temp_list) and 'O' in temp_list:
            wrong_st_list.append(i)
        temp_list = []
    for n in set(stop_name_list):
        if stop_name_list.count(n) > 1:
            for k, l in zip(stop_name_list, stop_type_list):
                if k == n:
                    temp_list.append(l)
            if 'O' in temp_list:
                wrong_st_list.append(n)
        temp_list = []
    a = f'Wrong stop type: {sorted(list(set(wrong_st_list)))}' if wrong_st_list else 'OK'
    a = 'On demand stops test:\n' + a
    return a


bus_data = json.loads(input())

# print(all_errors_func(bus_data))
# print(count_st_by_bus(bus_data))
# print(count_stops(bus_data))
# print(time_test(bus_data))
print(dem_stops_test(bus_data))
