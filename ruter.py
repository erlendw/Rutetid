import RPi.GPIO as GPIO
import lcdlib
import time
import requests
import json
import datetime
from dateutil.parser import parse


print(requests)

# Define GPIO to LCD mapping
LCD_RS = 26
LCD_E = 19
LCD_D4 = 13
LCD_D5 = 6
LCD_D6 = 5
LCD_D7 = 11
LED_ON = 15

# Define some device constants
LCD_WIDTH = 20  # Maximum characters per line
LCD_CHR = True
LCD_CMD = False

LCD_LINE_1 = 0x80  # LCD RAM address for the 1st line
LCD_LINE_2 = 0xC0  # LCD RAM address for the 2nd line
LCD_LINE_3 = 0x94  # LCD RAM address for the 3rd line
LCD_LINE_4 = 0xD4  # LCD RAM address for the 4th line

# Timing constants
E_PULSE = 0.0005
E_DELAY = 0.0005

def getTime():

    #frudenlund stop 3010307
    #helsfyr 3011442
    #jbt 3010370
    r = requests.get('http://reisapi.ruter.no/StopVisit/GetDepartures/3010012')

    result = json.loads(r.text)


    for obj in result:

        ruteTid = parse(obj['MonitoredVehicleJourney']['MonitoredCall']['ExpectedDepartureTime']).replace(tzinfo=None)
        tid = datetime.datetime.now().replace(tzinfo=None)

        diff = ruteTid - tid
        print(diff)

        lcdlib.lcd_string(obj['MonitoredVehicleJourney']['PublishedLineName'], LCD_LINE_1, 1)
        lcdlib.lcd_string(obj['MonitoredVehicleJourney']['DestinationName'], LCD_LINE_2, 1)
        lcdlib.lcd_string(str(round(diff.total_seconds()/60,1)) + " min", LCD_LINE_3, 1)
        lcdlib.lcd_string("--------------------", LCD_LINE_4, 2)

        time.sleep(5)  # 20 second delay

        # Blank display
        lcdlib.lcd_byte(0x01, LCD_CMD)


    #print(json.dumps(json.loads(r.text), indent=4, sort_keys=True))


def main():
    # Main program block

    GPIO.setmode(GPIO.BCM)  # Use BCM GPIO numbers
    GPIO.setup(LCD_E, GPIO.OUT)  # E
    GPIO.setup(LCD_RS, GPIO.OUT)  # RS
    GPIO.setup(LCD_D4, GPIO.OUT)  # DB4
    GPIO.setup(LCD_D5, GPIO.OUT)  # DB5
    GPIO.setup(LCD_D6, GPIO.OUT)  # DB6
    GPIO.setup(LCD_D7, GPIO.OUT)  # DB7
    GPIO.setup(LED_ON, GPIO.OUT)  # Backlight enable

    # Initialise display
    lcdlib.lcd_init()

    getTime()

if __name__ == '__main__':
  try:
    main()
  except KeyboardInterrupt:
    pass
  finally:
    lcdlib.lcd_byte(0x01, LCD_CMD)
    lcdlib.lcd_string("Goodbye!",LCD_LINE_1,2)
    GPIO.cleanup()