import random
from typing import List, Dict, Any
from dataclasses import dataclass
import json
from dataclasses import asdict

# Constants (you may need to adjust these based on your actual constants)
MAX_CLIENTS = 50
HOSTNAME_MAX_LEN = 64
IPADDR_MAX_LEN = 16
SSID_MAX_LEN = 32
MAX_NUM_VIF = 8
MAX_NUM_RADIO = 2

@dataclass
class ClientRecord:
    macaddr: List[int]
    hostname: str
    ipaddr: str
    ssid: str

@dataclass
class ClientReportData:
    n_client: int
    record: List[ClientRecord]

@dataclass
class VifData:
    radio: str
    ssid: str
    num_sta: int
    uplink_mb: int
    downlink_mb: int

@dataclass
class RadioData:
    band: str
    channel: int
    txpower: int
    channel_utilization: int

@dataclass
class VifReportData:
    n_vif: int
    vif: List[VifData]
    n_radio: int
    radio: List[RadioData]

def ioctl80211_jedi_client_fetch_dummy() -> ClientReportData:
    """
    Generate dummy client data for WiFi network reporting.
    
    Returns:
        ClientReportData: Object containing dummy client information
    """
    report = ClientReportData(n_client=MAX_CLIENTS, record=[])
    
    for i in range(MAX_CLIENTS):
        # Dummy MAC address
        macaddr = [0x00, 0x11, 0x22, 0x33, 0x44, i]
        
        # Dummy hostname
        hostname = f"Client_{i}"
        
        # Dummy IP address
        ipaddr = f"192.168.1.{100 + i}"
        
        # Dummy SSID (the original code was truncated, so I'm making an assumption)
        ssid = f"WiFi_Network_{i % 4}"  # Cycle through 4 different SSIDs
        
        client_record = ClientRecord(
            macaddr=macaddr,
            hostname=hostname,
            ipaddr=ipaddr,
            ssid=ssid
        )
        
        report.record.append(client_record)
    
    return report

def dummy_get_vif_report_data() -> VifReportData:
    """
    Generate dummy VIF (Virtual Interface) report data for WiFi network.
    
    Returns:
        VifReportData: Object containing dummy VIF and radio information
    """
    report_ctx = VifReportData(n_vif=MAX_NUM_VIF, vif=[], n_radio=MAX_NUM_RADIO, radio=[])
    
    # VIF configurations
    vif_configs = [
        ("BAND2G", "AirPro-2G-1", 0),
        ("BAND5G", "AirPro-5G-1", 20),
        ("BAND2G", "AirPro-2G-2", 0),
        ("BAND5G", "AirPro-5G-2", 0),
        ("BAND2G", "AirPro-2G-3", 0),
        ("BAND5G", "AirPro-5G-3", 0),
        ("BAND2G", "AirPro-2G-4", 0),
        ("BAND5G", "AirPro-5G-4", 0),
    ]
    
    # Generate VIF data
    for i, (radio, ssid, num_sta) in enumerate(vif_configs):
        vif_data = VifData(
            radio=radio,
            ssid=ssid,
            num_sta=num_sta,
            uplink_mb=random.randint(500, 1499),    # rand() % 1000 + 500
            downlink_mb=random.randint(1000, 2999)  # rand() % 2000 + 1000
        )
        report_ctx.vif.append(vif_data)
    
    # Generate radio data
    radio_configs = [
        ("BAND2G", 6, 25, 20),
        ("BAND5G", 36, 25, 20),
    ]
    
    for band, channel, txpower, channel_util in radio_configs:
        radio_data = RadioData(
            band=band,
            channel=channel,
            txpower=txpower,
            channel_utilization=channel_util
        )
        report_ctx.radio.append(radio_data)
    
    return report_ctx

# Example usage and helper functions
def print_client_report(report: ClientReportData):
    """Print client report data in a readable format."""
    print(f"Number of clients: {report.n_client}")
    print("\nClient Records:")
    for i, record in enumerate(report.record[:5]):  # Show first 5 for brevity
        mac_str = ":".join([f"{b:02x}" for b in record.macaddr])
        print(f"  Client {i}: MAC={mac_str}, Hostname={record.hostname}, IP={record.ipaddr}, SSID={record.ssid}")
    if len(report.record) > 5:
        print(f"  ... and {len(report.record) - 5} more clients")

def print_vif_report(report: VifReportData):
    """Print VIF report data in a readable format."""
    print(f"Number of VIFs: {report.n_vif}")
    print("\nVIF Data:")
    for i, vif in enumerate(report.vif):
        print(f"  VIF {i}: Radio={vif.radio}, SSID={vif.ssid}, Stations={vif.num_sta}, "
              f"Uplink={vif.uplink_mb}Mb, Downlink={vif.downlink_mb}Mb")
    
    print(f"\nNumber of Radios: {report.n_radio}")
    print("Radio Data:")
    for i, radio in enumerate(report.radio):
        print(f"  Radio {i}: Band={radio.band}, Channel={radio.channel}, "
              f"TxPower={radio.txpower}dBm, Utilization={radio.channel_utilization}%")

if __name__ == "__main__":
    # Test the functions
    print("=== Client Report Data ===")
    client_data = ioctl80211_jedi_client_fetch_dummy()
    print_client_report(client_data)
    
    print("\n=== VIF Report Data ===")
    vif_data = dummy_get_vif_report_data()
    print_vif_report(vif_data)


    # json format

    print("\n=== Client Report in JSON Format ===")
    client_json = json.dumps(asdict(client_data), indent=4)
    print(client_json)
    
    print("\n=== VIF Report in JSON Format ===")
    vif_json = json.dumps(asdict(vif_data), indent=4)
    print(vif_json)