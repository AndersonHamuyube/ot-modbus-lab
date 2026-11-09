"""Read the PLC values (a normal, harmless operator action)."""
from pymodbus.client import ModbusTcpClient

client = ModbusTcpClient("127.0.0.1", port=5020)
client.connect()

regs = client.read_holding_registers(0, count=2)
coil = client.read_coils(0, count=1)
print("Pump speed (rpm):", regs.registers[0])
print("Tank level (%):  ", regs.registers[1])
print("Breaker closed:  ", coil.bits[0])

client.close()