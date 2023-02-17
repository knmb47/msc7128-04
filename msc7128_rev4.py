import spidev
import time

def reverse(a):
    a = (((a & 0x0f) << 4) | ((a & 0xf0) >> 4))
    a = (((a & 0x33) << 2) | ((a & 0xcc) >> 2))
    a = (((a & 0x55) << 1) | ((a & 0xaa) >> 1))
    return a

# C7128-04
def conv_msc(c):
    if (c == '['):
        return 26
    if (c == '\\'):
        return 27
    if (c == ']'):
        return 28
    if (c == 'Ⅱ'):
        return 29
    if (c == '!'):
        return 32+26+1
    if (c == '→'):
        return 32+26+2
    if (c == '#'):
        return 32+26+3
    if (c == '←'):
        return 32+26+4
    if (c == '&'):
        return 64
    if (c == '\''):
        return 65
    if (c == '('):
        return 66
    if (c == ')'):
        return 67
    if (c == '*'):
        return 68
    if (c == '+'):
        return 69
    if (c == ','):
        return 70
    if (c == '-'):
        return 71
    if (c == '.'):
        return 72
    if (c == '/'):
        return 73
    if (c == ':'):
        return 84
    if (c == ';'):
        return 85
    if (c == '<'):
        return 86
    if (c == '='):
        return 87
    if (c == '>'):
        return 88
    if (c == '?'):
        return 89
    if (c == '↑'):
        return 90

    c = ord(c)
    if ( c >= 65 and c <= 90):
        # A-Z
        return c - 65
    if ( c >= 97 and c <= 122):
        # a-z
        # c - 97 + 26 = c - 71
        return c - 97 + 32
    if ( c >= 48 and c <= 57):
        # 0-9
        # c - 48 + 74 = c + 26
        return c + 26
    return 127

# usage
# [ reverse(conv_msc(x)) for x in "text" ]


command_address_set = 0b10000001
address_0 = 0b00000000

command_character_code_set = 0b10011001

command_number_of_display = 0b10111101
com_displayed_0 = 0b11111111

command_display_duty = 0b10100101
display_duty_15 = 0b11110000

command_lamp_test = 0b11000011
lamp_test = 0b11111111
lamp_off  = 0b00000000

#初期設定
spi = spidev.SpiDev()
spi.open(0,0)
spi.mode = 3  #このデバイスはSPI mode3で動作
#spi.max_speed_hz = 1000000
# OKI MSC7128 indicates Max OSC Frequency as 270kHz
#spi.max_speed_hz = 100000
spi.max_speed_hz = 1000
#spi.max_speed_hz = 250000

spi.xfer2([command_address_set, address_0, command_character_code_set] + [ reverse(conv_msc(x)) for x in "SONY TA-AV670   " ] ,0,1000,8)
time.sleep(1)
spi.xfer2([command_number_of_display, com_displayed_0, command_display_duty, display_duty_15],0,1000,8)
time.sleep(1)

spi.xfer2([command_address_set, address_0, command_character_code_set] + [ reverse(conv_msc(x)) for x in "←↑→↓[]()+-_:;" ] ,0,1000,8)
time.sleep(1)
spi.xfer2([command_number_of_display, com_displayed_0, command_display_duty, display_duty_15],0,1000,8)
time.sleep(1)


spi.close()
