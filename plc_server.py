"""Fake PLC for the OT lab. Holds a pump speed, a tank level and a breaker state."""
import asyncio
from pymodbus.datastore import (
    ModbusDeviceContext,
    ModbusSequentialDataBlock,
    ModbusServerContext,
)
from pymodbus.server import StartAsyncTcpServer

# Holding registers: address 0 = pump speed (rpm), address 1 = tank level (%)
# Coils: address 0 = breaker (1 = closed/on, 0 = open/off)
device = ModbusDeviceContext(
    hr=ModbusSequentialDataBlock(1, [1450, 75]),
    co=ModbusSequentialDataBlock(1, [1]),
)
context = ModbusServerContext(devices=device, single=True)


async def main():
    print("Fake PLC listening on 127.0.0.1:5020 (Ctrl+C to stop)")
    await StartAsyncTcpServer(context=context, address=("127.0.0.1", 5020))


if __name__ == "__main__":
    asyncio.run(main())