import spidev
import time

command_address_set = 0b10000001
address_0 = 0b00000000
address_1 = 0b00000001
address_2 = 0b00000000
address_7 = 0b00000000
address_f = 0b00001111

command_character_code_set = 0b10011001
char_code_0 = 0b00000000
char_code_1 = 0b00000001
char_code_0_c = 0b10000000
char_code_1_c = 0b10000001
char_code_f = 0b11111110

command_number_of_display = 0b10111101
com_displayed_0 = 0b00000000

command_display_duty = 0b10100101
display_duty_15 = 0b11111111

command_lamp_test = 0b11000011
lamp_test = 0b11111111
lamp_off = 0b00000000

#初期設定
spi = spidev.SpiDev()
spi.open(0,0)
spi.mode = 3  #このデバイスはSPI mode3で動作
#spi.max_speed_hz = 1000000
# OKI MSC7128 indicates Max OSC Frequency as 270kHz
#spi.max_speed_hz = 100000
spi.max_speed_hz = 1000
#spi.max_speed_hz = 250000

#アドレス"write_addr "に対してwrite_dataを書き込む
spi.xfer2([command_lamp_test, lamp_test],0,1000,8)
time.sleep(1)
spi.xfer2([command_number_of_display, com_displayed_0, command_display_duty, display_duty_15],0,1000,8)
time.sleep(1)

spi.xfer2([command_lamp_test, lamp_off],0,1000,8)
time.sleep(1)
#spi.xfer2([command_number_of_display, com_displayed_0, command_display_duty, display_duty_15],0,1000,8)

time.sleep(1)

spi.close()
