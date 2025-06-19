import time
from typing import List
from dataclasses import dataclass, field
from enum import IntEnum
import json
from dataclasses import asdict

# Constants
MAX_CLIENTS = 50
HOSTNAME_MAX_LEN = 64
IPADDR_MAX_LEN = 16
SSID_MAX_LEN = 32

class RadioType(IntEnum):
    RADIO_TYPE_2G = 0
    RADIO_TYPE_5G = 1

@dataclass
class ClientRecord:
    macaddr: List[int] = field(default_factory=lambda: [0] * 6)
    hostname: str = ""
    ipaddr: str = ""
    ssid: str = ""
    rx_bytes: int = 0
    tx_bytes: int = 0
    rssi: int = 0
    is_connected: int = 0
    duration_ms: int = 0
    radio_type: int = 0
    channel: int = 0

@dataclass
class ClientReportData:
    n_client: int = 0
    record: List[ClientRecord] = field(default_factory=list)

def ioctl80211_jedi_client_fetch_dummy() -> ClientReportData:
    """
    Generate dummy client data for WiFi network reporting.
    Equivalent to the C function ioctl80211_jedi_client_fetch_dummy().
    
    Returns:
        ClientReportData: Object containing dummy client information
        
    Returns True equivalent (success) by returning a valid object.
    """
    report = ClientReportData()
    
    # Set number of clients
    report.n_client = MAX_CLIENTS
    
    for i in range(MAX_CLIENTS):
        client = ClientRecord()
        
        # Dummy MAC address
        client.macaddr[0] = 0x00
        client.macaddr[1] = 0x11
        client.macaddr[2] = 0x22
        client.macaddr[3] = 0x33
        client.macaddr[4] = 0x44
        client.macaddr[5] = i  # Different last byte
        
        # Dummy hostname
        client.hostname = f"Client_{i}"
        
        # Dummy IP address
        client.ipaddr = f"192.168.1.{100 + i}"
        
        # Dummy SSID
        client.ssid = "Dummy_SSID"
        
        # Dummy data usage
        client.rx_bytes = 100000 + (i * 5000)
        client.tx_bytes = 50000 + (i * 2500)
        
        # Dummy RSSI
        client.rssi = -40 - i * 5
        
        # Connection status
        client.is_connected = 1
        
        # Connection duration
        client.duration_ms = 3600000 * (i + 1)  # 1 hour per client
        
        # Dummy radio type and channel
        client.radio_type = RadioType.RADIO_TYPE_5G if (i % 2 == 0) else RadioType.RADIO_TYPE_2G
        client.channel = 36 if (i % 2 == 0) else 6
        
        report.record.append(client)
    
    return report

def format_mac_address(macaddr: List[int]) -> str:
    """Convert MAC address list to standard format."""
    return ":".join([f"{b:02x}" for b in macaddr])

def format_bytes(bytes_val: int) -> str:
    """Convert bytes to human readable format."""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if bytes_val < 1024.0:
            return f"{bytes_val:.1f} {unit}"
        bytes_val /= 1024.0
    return f"{bytes_val:.1f} TB"

def format_duration(duration_ms: int) -> str:
    """Convert milliseconds to human readable duration."""
    seconds = duration_ms // 1000
    minutes = seconds // 60
    hours = minutes // 60
    days = hours // 24
    
    if days > 0:
        return f"{days}d {hours % 24}h {minutes % 60}m"
    elif hours > 0:
        return f"{hours}h {minutes % 60}m"
    elif minutes > 0:
        return f"{minutes}m {seconds % 60}s"
    else:
        return f"{seconds}s"

def get_radio_type_name(radio_type: int) -> str:
    """Get human readable radio type name."""
    if radio_type == RadioType.RADIO_TYPE_2G:
        return "2.4GHz"
    elif radio_type == RadioType.RADIO_TYPE_5G:
        return "5GHz"
    else:
        return f"Unknown ({radio_type})"

def print_client_report(report: ClientReportData, show_all: bool = False):
    """Print client report data in a readable format."""
    if not report:
        print("No client report data available")
        return
    
    print(f"=== WiFi Client Report ===")
    print(f"Total Clients: {report.n_client}")
    print()
    
    # Show first 10 clients by default, or all if requested
    clients_to_show = report.record if show_all else report.record[:10]
    
    for i, client in enumerate(clients_to_show):
        mac_str = format_mac_address(client.macaddr)
        rx_formatted = format_bytes(client.rx_bytes)
        tx_formatted = format_bytes(client.tx_bytes)
        duration_formatted = format_duration(client.duration_ms)
        radio_name = get_radio_type_name(client.radio_type)
        status = "Connected" if client.is_connected else "Disconnected"
        
        print(f"Client {i}:")
        print(f"  MAC Address: {mac_str}")
        print(f"  Hostname: {client.hostname}")
        print(f"  IP Address: {client.ipaddr}")
        print(f"  SSID: {client.ssid}")
        print(f"  Data Usage: RX {rx_formatted}, TX {tx_formatted}")
        print(f"  Signal Strength: {client.rssi} dBm")
        print(f"  Status: {status}")
        print(f"  Connection Duration: {duration_formatted}")
        print(f"  Radio: {radio_name} (Channel {client.channel})")
        print()
    
    if not show_all and len(report.record) > 10:
        print(f"... and {len(report.record) - 10} more clients")
        print("Use print_client_report(report, show_all=True) to see all clients")

def print_client_summary(report: ClientReportData):
    """Print a summary of client statistics."""
    if not report or not report.record:
        print("No client data available for summary")
        return
    
    total_rx = sum(client.rx_bytes for client in report.record)
    total_tx = sum(client.tx_bytes for client in report.record)
    connected_clients = sum(1 for client in report.record if client.is_connected)
    
    # Radio type distribution
    radio_2g_count = sum(1 for client in report.record if client.radio_type == RadioType.RADIO_TYPE_2G)
    radio_5g_count = sum(1 for client in report.record if client.radio_type == RadioType.RADIO_TYPE_5G)
    
    # RSSI statistics
    rssi_values = [client.rssi for client in report.record]
    avg_rssi = sum(rssi_values) / len(rssi_values) if rssi_values else 0
    min_rssi = min(rssi_values) if rssi_values else 0
    max_rssi = max(rssi_values) if rssi_values else 0
    
    print(f"=== Client Summary ===")
    print(f"Total Clients: {report.n_client}")
    print(f"Connected Clients: {connected_clients}")
    print(f"Total Data Transfer: RX {format_bytes(total_rx)}, TX {format_bytes(total_tx)}")
    print(f"Radio Distribution: 2.4GHz: {radio_2g_count}, 5GHz: {radio_5g_count}")
    print(f"Signal Strength: Avg {avg_rssi:.1f} dBm, Range {max_rssi} to {min_rssi} dBm")

def export_client_data_csv(report: ClientReportData, filename: str = "client_report.csv"):
    """Export client data to CSV format."""
    if not report or not report.record:
        print("No client data to export")
        return
    
    try:
        with open(filename, 'w') as f:
            # CSV header
            f.write("Index,MAC_Address,Hostname,IP_Address,SSID,RX_Bytes,TX_Bytes,RSSI_dBm,Connected,Duration_ms,Radio_Type,Channel\n")
            
            # CSV data
            for i, client in enumerate(report.record):
                mac_str = format_mac_address(client.macaddr)
                radio_name = get_radio_type_name(client.radio_type)
                f.write(f"{i},{mac_str},{client.hostname},{client.ipaddr},{client.ssid},"
                       f"{client.rx_bytes},{client.tx_bytes},{client.rssi},{client.is_connected},"
                       f"{client.duration_ms},{radio_name},{client.channel}\n")
        
        print(f"Client data exported to {filename}")
    except Exception as e:
        print(f"Error exporting data: {e}")

if __name__ == "__main__":
    # Test the function
    print("Testing ioctl80211_jedi_client_fetch_dummy()...\n")
    
    # Generate dummy client report
    client_data = ioctl80211_jedi_client_fetch_dummy()
    
    # Print summary
    print_client_summary(client_data)
    
    print("\n" + "="*60 + "\n")
    
    # Print first 10 clients
    print_client_report(client_data)

    print("\n" + "="*60 + "\n")
    
    
    # Convert to JSON and print
    client_data_json = json.dumps(asdict(client_data), indent=4)
    print("Client Report in JSON format:")
    print(client_data_json)