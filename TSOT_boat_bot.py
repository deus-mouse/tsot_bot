import pyautogui
from time import sleep, time
import os
import json

DATA = [
    {
        "time": 3.0806829929351807,
        "type": "keyDown",
        "button": "a",
    },
    {
        "time": 3.089846134185791,
        "type": "keyDown",
        "button": "d",
    },
    {
        "time": 3.9670603275299072,
        "type": "keyUp",
        "button": "a",
    },
    {
        "time": 4.0006020069122314,
        "type": "keyUp",
        "button": "d",
    },
    {
        "time": 5.1823601722717285,
        "type": "keyDown",
        "button": "d",
    },
    {
        "time": 5.193557977676392,
        "type": "keyDown",
        "button": "a",
    },
    {
        "time": 6.386213064193726,
        "type": "keyUp",
        "button": "a",
    },
    {
        "time": 6.396932125091553,
        "type": "keyUp",
        "button": "d",
    },
    {
        "time": 7.859755992889404,
        "type": "keyDown",
        "button": "a",
    },
    {
        "time": 7.8708720207214355,
        "type": "keyDown",
        "button": "d",
    },
    {
        "time": 9.07453727722168,
        "type": "keyUp",
        "button": "a",
    },
    {
        "time": 9.108392238616943,
        "type": "keyUp",
        "button": "d",
    },
    {
        "time": 10.604932069778442,
        "type": "keyDown",
        "button": "a",
    },
    {
        "time": 10.616106271743774,
        "type": "keyDown",
        "button": "d",
    },
    {
        "time": 11.763318061828613,
        "type": "keyUp",
        "button": "a",
    },
    {
        "time": 11.786219120025635,
        "type": "keyUp",
        "button": "d",
    },
    {
        "time": 14.812397003173828,
        "type": "keyDown",
        "button": "Key.esc",
    },
    {
        "time": 14.902071952819824,
        "type": "keyUp",
        "button": "Key.esc",
    }
]

def main():
    initialize_pyautogui()
    countdown_timer()

    while True:
        play_actions("actions_test_01.json")
        # play_actions("open_space_go_to_nearest_doc.json")
        sleep(.50)

    print("Done")


def initialize_pyautogui():
    # Initialized PyAutoGUI
    # https://pyautogui.readthedocs.io/en/latest/introduction.html
    # When fail-safe mode is True, moving the mouse to the upper-left corner will abort your program.
    pyautogui.FAILSAFE = True


def countdown_timer():
    # Countdown timer
    print("Стартуем через 5 сек ", end="", flush=True)
    for i in range(0, 5):
        print(".", end="", flush=True)
        sleep(1)
    print("Гребем!")


def play_actions(filename):
    # Read the file
    # script_dir = os.path.dirname(__file__)
    # filepath = os.path.join(
    #     script_dir,
    #     'recordings',
    #     filename
    # )
    # with open(filepath, 'r') as jsonfile:
    #     # parse the json
    #     data = json.load(jsonfile)
    data = DATA
        # loop over each action
        # Because we are not waiting any time before executing the first action, any delay before the initial
        # action is recorded will not be reflected in the playback.
    for index, action in enumerate(data):
        action_start_time = time()

        # look for escape input to exit
        if action['button'] == 'Key.esc':
            break

        # perform the action
        if action['type'] == 'keyDown':
            key = convert_key(action['button'])
            pyautogui.keyDown(key)
            # print("keyDown on {}".format(key))
        elif action['type'] == 'keyUp':
            key = convert_key(action['button'])
            pyautogui.keyUp(key)
            # print("keyUp on {}".format(key))
        elif action['type'] == 'click':
            if action['button'] == 'Button.left':
                pyautogui.click(action['pos'][0], action['pos'][1], button='left', duration=0.25)
            if action['button'] == 'Button.right':
                # Right click recognize too
                pyautogui.click(action['pos'][0], action['pos'][1], button='right', duration=0.25)
            # print("click on {} {}".format(action['pos'], action['button']))

        # then sleep until next action should occur
        try:
            next_action = data[index + 1]
        except IndexError:
            # this was the last action in the list
            break
        elapsed_time = next_action['time'] - action['time']

        # if elapsed_time is negative, that means our actions are not ordered correctly. throw an error
        if elapsed_time < 0:
            raise Exception('Unexpected action ordering.')

        # adjust elapsed_time to account for our code taking time to run
        elapsed_time -= (time() - action_start_time)
        if elapsed_time < 0:
            elapsed_time = 0
        # print('sleeping for {}'.format(elapsed_time))
        print('Раз-Два')

        sleep(elapsed_time)


# convert pynput button keys into pyautogui keys
# https://pynput.readthedocs.io/en/latest/_modules/pynput/keyboard/_base.html#Key
# https://pyautogui.readthedocs.io/en/latest/keyboard.html
def convert_key(button):
    PYNPUT_SPECIAL_CASE_MAP = {
        'alt_l': 'altleft',
        'alt_r': 'altright',
        'alt_gr': 'altright',
        'caps_lock': 'capslock',
        'ctrl_l': 'ctrlleft',
        'ctrl_r': 'ctrlright',
        'page_down': 'pagedown',
        'page_up': 'pageup',
        'shift_l': 'shiftleft',
        'shift_r': 'shiftright',
        'num_lock': 'numlock',
        'print_screen': 'printscreen',
        'scroll_lock': 'scrolllock',
    }

    # example: 'Key.F9' should return 'F9', 'w' should return as 'w'
    cleaned_key = button.replace('Key.', '')

    if cleaned_key in PYNPUT_SPECIAL_CASE_MAP:
        return PYNPUT_SPECIAL_CASE_MAP[cleaned_key]

    return cleaned_key


if __name__ == "__main__":
    main()
