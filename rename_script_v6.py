import obspython as obs  # Import OBS Python API
import time  # For timestamp generation
import os  # For file operations like renaming

def script_description():
    """
    Provides a brief description of the script in OBS.
    """
    return "Rename recordings based on the active Scene Collection"

def script_load(settings):
    """
    Called when the script is loaded in OBS.
    Registers the event callback to listen for OBS events.
    """
    obs.obs_frontend_add_event_callback(on_event)

def script_unload():
    """
    Called when the script is unloaded in OBS.
    Removes the previously registered event callback.
    """
    obs.obs_frontend_remove_event_callback(on_event)

def script_update(settings):
    """
    Called when the script settings are updated in OBS.
    Not used in this script but kept for compatibility.
    """
    pass

def on_event(event):
    """
    Event callback function that listens for OBS events.
    Triggers specific actions based on the event type.
    """
    if event == obs.OBS_FRONTEND_EVENT_RECORDING_STOPPED:
        # If a recording is stopped, call the function to handle file renaming
        recording_finished()

def recording_finished():
    """
    Handles the renaming of the last recording file after recording stops.
    """
    try:
        # Get the name of the active scene collection
        active_collection = obs.obs_frontend_get_current_scene_collection()
        if not active_collection:
            print("Error: Failed to get active scene collection.")
            return

        # Create a timestamp in the desired format
        timestamp = time.strftime("%m.%d.%Y %I-%M-%S%p")
        
        # Generate the new filename based on the active scene collection and timestamp
        filename = f"{active_collection} {timestamp}.mp4"

        # Get the path of the last recorded file
        last_file = obs.obs_frontend_get_last_recording()
        if not last_file:
            print("Error: No recording file found.")
            return

        # Determine the new file path (same directory as the last file)
        renamed_file = os.path.join(os.path.dirname(last_file), filename)

        # Rename the file
        os.rename(last_file, renamed_file)
        print(f"Success: Renamed file from {last_file} to {renamed_file}")

    except FileNotFoundError:
        # Handle case where the file to rename does not exist
        print(f"Error: File not found - {last_file}")
    except PermissionError:
        # Handle case where the file cannot be renamed due to permissions
        print(f"Error: Permission denied when renaming {last_file} to {renamed_file}")
    except Exception as e:
        # Catch any other errors
        print(f"Unexpected error during renaming: {e}")