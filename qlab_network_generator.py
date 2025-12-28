import subprocess
import pandas
import sys

def generate_network_cues(data_frame, identifying_character, dca_identifier, network_patch):
    cue_number = 0

    first_column = get_first_numeric_column(data_frame)
    total_cues = len(data_frame.columns[first_column:])

    print(f"Creating {total_cues} cues...")

    for cue in data_frame.columns[first_column:]:
        channels_to_unmute, channels_to_mute, channels_ensemble_bus = get_channel_mute_data(data_frame, cue, identifying_character, dca_identifier)
        
        create_cue(("Q" + str(cue)), str(cue), channels_to_unmute, channels_ensemble_bus, str(len(channels_to_unmute) + len(channels_to_mute)), network_patch)

        percent = round(((cue_number + 1) / total_cues) * 100)
        sys.stdout.write("\033[K") 
        print(f"'Q{cue}' created. ({percent}%)", end="\r", flush=True)

        cue_number += 1

    print(f"\nCreated {total_cues} cues.")

def get_channel_mute_data(data_frame, cue, identifying_character, dca_identifier):
    channels_to_unmute = []
    channels_to_mute = []
    channels_ensemble_bus = []
    for _, row in data_frame.iterrows():
        if pandas.notna(row[cue]) and row[cue] == identifying_character or (dca_identifier is not None and pandas.notna(row[cue]) and row[cue] == dca_identifier):
            mic_num = int(row.iloc[0])
            channels_to_unmute.append(mic_num)
            if dca_identifier is not None and pandas.notna(row[cue]) and row[cue] == dca_identifier:
                mic_num = int(row.iloc[0])
                channels_ensemble_bus.append(mic_num)
        else:
            mic_num = int(row.iloc[0])
            channels_to_mute.append(mic_num)
            
    return channels_to_unmute, channels_to_mute, channels_ensemble_bus

def get_first_numeric_column(data_frame):
    for column in data_frame.columns:
        if isinstance(column, (int, float)):
            return data_frame.columns.get_loc(column)
    return None

import os

def create_cue(cue_name, cue_number, channels_to_unmute, channels_ensemble_bus, max_channels, network_patch=1):
    channel_unmute_string = "{" + ", ".join(str(channel) for channel in channels_to_unmute) + "}"
    channel_ensemble_string = "{" + ", ".join(str(channel) for channel in channels_ensemble_bus) + "}"
    
    script_path = os.path.join(os.path.dirname(__file__), "applescript/network.applescript")
    with open(script_path, "r") as file:
        script_template = file.read()

    final_script = (script_template
                    .replace("{{MAX_CHANNELS}}", str(max_channels))
                    .replace("{{CHANNELS_TO_UNMUTE}}", channel_unmute_string)
                    .replace("{{CHANNELS_ENSEMBLE_BUS}}", channel_ensemble_string)
                    .replace("{{CUE_NAME}}", str(cue_name))
                    .replace("{{CUE_NUMBER}}", str(cue_number))
                    .replace("{{NETWORK_PATCH}}", str(network_patch)))

    stdout, stderr = run_apple_script(final_script)
    
    if stderr:
        print(stderr.decode("utf-8"))
def run_apple_script(script):
    process = subprocess.Popen(['osascript', '-e', script], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    return stdout, stderr
