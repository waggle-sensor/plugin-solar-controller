
# TODO: Add more metrics to collect
registry_to_topicname_table = {
    "0x0020": "env.solar.current.array",
    "0x001f": "env.solar.current.load",
    "0x0063": "env.solar.current.system.charging",
    "0x0064": "env.solar.current.system.battery",
    "0x0065": "env.solar.current.system.load",
    
    "0x0023": "env.solar.voltage.load",
    "0x0022": "env.solar.voltage.array",
    "0x0021": "env.solar.voltage.battery",
    "0x0025": "env.solar.voltage.battery.sense",

    "0x0075": "env.solar.temperature.battery",
    "0x0077": "env.solar.temperature.heatsink",

    "0x0080": "env.solar.state.charging",
    "0x0100": "env.solar.state.load",
}

transform_func = {
    "0x0020": lambda x: float(x),
    "0x001f": lambda x: float(x),
    "0x0063": lambda x: float(x),
    "0x0064": lambda x: float(x),
    "0x0065": lambda x: float(x),
    
    "0x0023": lambda x: float(x),
    "0x0022": lambda x: float(x),
    "0x0021": lambda x: float(x),
    "0x0025": lambda x: float(x),

    "0x0075": lambda x: float(x),
    "0x0077": lambda x: float(x),

    "0x0080": lambda x: int(x),
    "0x0100": lambda x: int(x),
}

meta_table = {
    "0x0020": {"unit": "A"},
    "0x001f": {"unit": "A"},
    "0x0063": {"unit": "A"},
    "0x0064": {"unit": "A"},
    "0x0065": {"unit": "A"},
    
    "0x0023": {"unit": "V"},
    "0x0022": {"unit": "V"},
    "0x0021": {"unit": "V"},
    "0x0025": {"unit": "V"},

    "0x0075": {"unit": "C"},
    "0x0077": {"unit": "C"},
}

# Charge state for 0x0080
# 0 = starting
# 1 = night check
# 2 = disconnected
# 3 = night
# 4 = fault
# 5 = bulk
# 6 = absorption
# 7 = float
# 8 = equalize

# Load state for 0x0100
# 0 = start
# 1 = norm
# 2 = lvdwarn
# 3 = lvd
# 4 = fault 