"""Modbus write detector: reads a capture file and alerts on unauthorized writes."""
import sys
from scapy.all import rdpcap, IP, TCP, Raw

PLC_PORT = 5020

# Modbus function codes that CHANGE something in the PLC
WRITE_CODES = {
    5: "Write Single Coil",
    6: "Write Single Register",
    15: "Write Multiple Coils",
    16: "Write Multiple Registers",
}

# IP addresses allowed to send writes (e.g. the engineering workstation).
# Empty on purpose: in this lab, nobody is approved, so every write raises an alert.
APPROVED_WRITERS = {"127.0.0.1"}


def check_capture(path):
    packets = rdpcap(path)
    alerts = 0
    for pkt in packets:
        # only requests heading TO the PLC, carrying data
        if not (pkt.haslayer(IP) and pkt.haslayer(TCP) and pkt.haslayer(Raw)):
            continue
        if pkt[TCP].dport != PLC_PORT:
            continue

        data = bytes(pkt[Raw].load)
        # Modbus/TCP: 7-byte header, then the function code
        if len(data) < 8:
            continue
        function_code = data[7]

        if function_code in WRITE_CODES and pkt[IP].src not in APPROVED_WRITERS:
            alerts += 1
            print(f"[ALERT] {WRITE_CODES[function_code]} (code {function_code}) "
                  f"from {pkt[IP].src}:{pkt[TCP].sport} to {pkt[IP].dst}:{pkt[TCP].dport}")

    print(f"\nDone. {len(packets)} packets checked, {alerts} alert(s).")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python detector.py captures/modbus-attack.pcapng")
        sys.exit(1)
    check_capture(sys.argv[1])