from __future__ import annotations

import math
from collections import deque

import tqdm


def parse(data):
    specs = data.strip().split("\n")

    modules = {}
    for spec in specs:
        type_name, outputs = spec.split(" -> ")

        if type_name == "broadcaster":
            modules[type_name] = {"type": "b", "state": None, "out": outputs.split(", ")}
        elif type_name[0] == "%":
            modules[type_name[1:]] = {"type": "%", "state": "off", "out": outputs.split(", ")}
        elif type_name[0] == "&":
            modules[type_name[1:]] = {"type": "&", "state": {}, "out": outputs.split(", ")}

    # now populate the input states of conjunction modules
    for mod_name, mod in modules.items():
        for output_name in mod["out"]:
            if output_name not in modules:
                continue
            output_mod = modules[output_name]
            if output_mod["type"] == "&":
                output_mod["state"][mod_name] = "low"

    modules["button"] = {"type": "x", "state": None, "out": ["broadcaster"]}
    return modules


def solve(input, watch_low=("qm", "jd", "pm", "nf")):
    pulse_count = {"low": 0, "high": 0}
    seen_low = {}

    for k in tqdm.tqdm(range(5000)):
        if (not watch_low and k == 1000) or (watch_low and len(seen_low) == len(watch_low)):
            break

        pulse_queue = deque([("button", "broadcaster", "low")])
        while pulse_queue:
            source, dest, pulse = pulse_queue.popleft()
            pulse_count[pulse] += 1

            if dest not in input:
                continue  # e.g. 'output'

            dest_mod = input[dest]
            if dest_mod["type"] == "b":
                for next_dest in dest_mod["out"]:
                    pulse_queue.append((dest, next_dest, pulse))

            elif dest_mod["type"] == "%":
                if pulse == "high":
                    continue

                if dest_mod["state"] == "off":
                    dest_mod["state"] = "on"
                    next_pulse = "high"
                else:
                    dest_mod["state"] = "off"
                    next_pulse = "low"

                for next_dest in dest_mod["out"]:
                    pulse_queue.append((dest, next_dest, next_pulse))

            else:
                dest_mod["state"][source] = pulse
                if all(s == "high" for s in dest_mod["state"].values()):
                    next_pulse = "low"
                else:
                    next_pulse = "high"

                if next_pulse == "low" and dest in watch_low and dest not in seen_low:
                    seen_low[dest] = k + 1

                for next_dest in dest_mod["out"]:
                    pulse_queue.append((dest, next_dest, next_pulse))

    return pulse_count["low"] * pulse_count["high"], math.lcm(*seen_low.values())
