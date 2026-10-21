from fastmcp import FastMCP # This is the MCP Library
import pyfirmata2 # This is the library to control arduino with python 

# Name of the MCP server
ArduinoMCP = FastMCP('Arduino Servers')

# Config
PORT = 'COM3' # Change to your COM port
WHITE_LED_PIN = 12 # Change to your White LED pin (D12 PWM)
RED_LED_PIN = 11 # Change to your Red LED pin (D11 PWM)

_arduino = None

def get_arduino():
    """
    Lazily initialize connection to Arduino board to prevent MCP startup crash when port is busy.

    For example, if the Serial Monitor of the Arduino IDE is open when we start the MCP server, 
    the MCP server will be prevented from accessing the Arduino board.
    """
    global _arduino

    if _arduino is None:

        try:
            _arduino = pyfirmata2.Arduino(PORT)

        except Exception as e:
            raise RuntimeError(
                f"Could not connect to Arduino on {PORT}: {e}. "
                "Please close Arduino IDE Serial Monitor or any other app using this port."
            )

    return _arduino

# @ArduinoMCP.tool is a python decorator which is wrapping our functions to be exposed to the MCP Client
@ArduinoMCP.tool
def white_led_ON():
    '''Turns on white LED in the Arduino'''
    arduino = get_arduino()
    arduino.digital[WHITE_LED_PIN].write(1)
    return 'White LED ON'

@ArduinoMCP.tool
def red_led_ON():
    '''Turns on red LED in the Arduino'''
    arduino = get_arduino()
    arduino.digital[RED_LED_PIN].write(1)
    return 'Red LED ON'

@ArduinoMCP.tool
def led_OFF():
    '''Turns off all LEDs in the Arduino'''
    arduino = get_arduino()
    arduino.digital[RED_LED_PIN].write(0)
    arduino.digital[WHITE_LED_PIN].write(0)
    return 'All LEDs OFF'


if __name__ == "__main__":
    ArduinoMCP.run() # Lets run our MCP server :)
  