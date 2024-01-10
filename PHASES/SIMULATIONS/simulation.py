import importlib

def run_sim(sim_type, sim_args, **kwargs):
    module_call, function_call = split_string_at_last_dot(sim_type)
    module = importlib.import_module(module_call)
    return getattr(module, function_call)(**sim_args, **kwargs)

def split_string_at_last_dot(input_string):
    last_dot_index = input_string.rfind('.')

    if last_dot_index != -1:
        first_part = input_string[:last_dot_index]
        last_part = input_string[last_dot_index + 1:]
        return first_part, last_part
    else:
        # If there is no dot in the input string
        return None, None