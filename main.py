import board

## Load Standard Modules for Keyboard
from kmk.kmk_keyboard import KMKKeyboard
from kmk.keys import KC
from kmk.scanners import DiodeOrientation
from kmk.hid import HIDModes

## Load Split Extensions for Split Keyboard
from kmk.modules.split import Split, SplitType, SplitSide
from storage import getmount

## Load RGB Extensions for RGB Backlight
from kmk.extensions.RGB import RGB
from kmk.extensions.rgb import AnimationModes

## Initialize Keyboard Object 
keyboard = KMKKeyboard()
keyboard.debug_enabled = True
keyboard.diode_orientation = DiodeOrientation.ROW2COL

side = SplitSide.RIGHT if str(getmount('/').label)[-1] == 'R' else SplitSide.LEFT
tx = board.D0 # TX0
rx = board.D1 # Rx0

## Pin Assignments
keyboard.col_pins = (board.D2, board.D3, board.D4, board.D6, board.D7, board.D8)
rgb_pixel_pin = board.A3
if split.split_side == SplitSide.RIGHT:
    print("R")
    keyboard.row_pins = (board.D9, board.A2, board.A1, board.A0, board.D10)
else:
    print("L")
    keyboard.row_pins = (board.D9, board.A3, board.A2, board.A0, board.NEOPIXEL)

## Setup Split-Module
split = Split(
    split_flip=False,  # If both halves are the same, but flipped, set this True
    split_side=side,  # Sets if this is to SplitSide.LEFT or SplitSide.RIGHT, or use EE hands
    split_type=SplitType.UART,  # Defaults to UART
    split_target_left=False,  # Assumes that left will be the one on USB. Set to False if it will be the right
    uart_interval=20,  # Sets the uarts delay. Lower numbers draw more power
    data_pin=rx,  # The primary data pin to talk to the secondary device with
    data_pin2=tx,  # Second uart pin to allow 2 way communication
    uart_flip=True,  # Reverses the RX and TX pins if both are provided
    use_pio=False,  # Use RP2040 PIO implementation of UART. Required if you want to use other pins than RX/TX
)

## Keymap Assignment 
keyboard.keymap = [
    [
        KC.N7,   KC.N8,   KC.N9,  KC.A,  KC.B,   KC.C,                                           KC.N7,   KC.N8,   KC.N9,  KC.A,  KC.B,   KC.D, 
        KC.N1,   KC.N2,   KC.N3,  KC.N4, KC.N5,  KC.N6,                                          KC.N7,   KC.N8,   KC.N9,  KC.N0, KC.A,   KC.B,
        KC.D,    KC.E,    KC.F,   KC.G,  KC.H,   KC.I,                                           KC.N7,   KC.N8,   KC.N9,  KC.A,  KC.B,   KC.C,
        KC.J,    KC.K,    KC.L,   KC.M,  KC.N,   KC.O,                                           KC.N7,   KC.N8,   KC.N9,  KC.A,  KC.B,   KC.C, 
                          KC.P,    KC.Q, KC.R,   KC.S,  KC.T,   KC.U,          KC.N7,   KC.N8,   KC.N9,   KC.A,    KC.B,   KC.C,
    ]
]

## Coordination Mapping for MDMa
keyboard.coord_mapping = [
    35, 34, 33, 32, 31, 30,    0,  1,  2,  3,  4,  5,
    41, 40, 39, 38, 37, 36,    6,  7,  8,  9, 10, 11,
    47, 46, 45, 44, 43, 42,    12, 13, 14, 15, 16, 17,
    53, 52, 51, 50, 49, 48,    18, 19, 20, 21, 22, 23,
    59, 58, 57, 56, 55, 54,    24, 25, 29, 28, 26, 27,
]

keyboard.modules.append(split)


## Setup RGB Module
rgb = RGB(pixel_pin=rgb_pixel_pin,
        num_pixels=30,
        val_limit=25,
        hue_default=160,
        sat_default=255,
        rgb_order=(1, 0, 2),  # GRB WS2812
        val_default=20,
        hue_step=5,
        sat_step=5,
        val_step=1,
        animation_speed=1,
        breathe_center=1.5,  # 1.0-2.7
        knight_effect_length=3,
        animation_mode=AnimationModes.BREATHING,
        reverse_animation=False,
        refresh_rate=60,
        )

keyboard.extensions.append(rgb)

if __name__ == '__main__':

    keyboard.go(hid_type=HIDModes.USB)
