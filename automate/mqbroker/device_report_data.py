import time
from typing import List
from dataclasses import dataclass, field
import json
from dataclasses import asdict

@dataclass
class MemoryUtilization:
    mem_total: int = 0
    mem_used: int = 0
    swap_total: int = 0
    swap_used: int = 0

@dataclass
class CpuUtilization:
    cpu_util: int = 0

@dataclass
class FilesystemUtilization:
    fs_type: int = 0
    fs_total: int = 0
    fs_used: int = 0

@dataclass
class DeviceRecord:
    load: List[float] = field(default_factory=lambda: [0.0, 0.0, 0.0])
    uptime: int = 0
    mem_util: MemoryUtilization = field(default_factory=MemoryUtilization)
    cpu_util: CpuUtilization = field(default_factory=CpuUtilization)
    fs_util: List[FilesystemUtilization] = field(default_factory=lambda: [FilesystemUtilization(), FilesystemUtilization()])

@dataclass
class DeviceReportData:
    timestamp_ms: int = 0
    record: DeviceRecord = field(default_factory=DeviceRecord)

def fill_dummy_device_report() -> DeviceReportData:
    """
    Generate dummy device report data including system metrics.
    Equivalent to the C function fill_dummy_device_report().
    
    Returns:
        DeviceReportData: Object containing dummy device information
        
    Returns True equivalent (success) by returning a valid object.
    In case of error (equivalent to C's null check), returns None.
    """
    # Initialize report (equivalent to memset in C)
    report = DeviceReportData()
    
    # Fill timestamp (equivalent to commented clock_gettime code)
    report.timestamp_ms = int(time.time() * 1000)
    
    # Dummy Load averages 
    report.record.load[0] = 0.5
    report.record.load[1] = 1.2
    report.record.load[2] = 2.3
    
    # Dummy Uptime
    report.record.uptime = 123456  # Example uptime in seconds
    
    # Dummy Memory utilization
    report.record.mem_util.mem_total = 2048000  # 2 GB
    report.record.mem_util.mem_used = 1024000   # 1 GB
    report.record.mem_util.swap_total = 102400  # 100 MB
    report.record.mem_util.swap_used = 51200    # 50 MB
    
    # Dummy CPU utilization
    report.record.cpu_util.cpu_util = 25  # 25%
    
    # Dummy Filesystem utilization
    report.record.fs_util[0].fs_type = 0      # Root FS
    report.record.fs_util[0].fs_total = 512000 # 500 MB
    report.record.fs_util[0].fs_used = 256000  # 250 MB
    
    report.record.fs_util[1].fs_type = 1      # Temp FS
    report.record.fs_util[1].fs_total = 102400 # 100 MB
    report.record.fs_util[1].fs_used = 51200   # 50 MB
    
    return report

def print_device_report(report: DeviceReportData):
    """Print device report data in a readable format."""
    if not report:
        print("No report data available")
        return
        
    print(f"Device Report - Timestamp: {report.timestamp_ms} ms")
    print(f"Load Averages: {report.record.load[0]}, {report.record.load[1]}, {report.record.load[2]}")
    print(f"Uptime: {report.record.uptime} seconds ({report.record.uptime // 3600:.1f} hours)")
    
    print("\nMemory Utilization:")
    mem = report.record.mem_util
    mem_percent = (mem.mem_used / mem.mem_total * 100) if mem.mem_total > 0 else 0
    swap_percent = (mem.swap_used / mem.swap_total * 100) if mem.swap_total > 0 else 0
    print(f"  RAM: {mem.mem_used:,}/{mem.mem_total:,} KB ({mem_percent:.1f}%)")
    print(f"  Swap: {mem.swap_used:,}/{mem.swap_total:,} KB ({swap_percent:.1f}%)")
    
    print(f"\nCPU Utilization: {report.record.cpu_util.cpu_util}%")
    
    print("\nFilesystem Utilization:")
    fs_type_names = {0: "Root FS", 1: "Temp FS"}
    for i, fs in enumerate(report.record.fs_util):
        fs_name = fs_type_names.get(fs.fs_type, f"FS Type {fs.fs_type}")
        fs_percent = (fs.fs_used / fs.fs_total * 100) if fs.fs_total > 0 else 0
        print(f"  {fs_name}: {fs.fs_used:,}/{fs.fs_total:,} KB ({fs_percent:.1f}%)")

def convert_bytes_to_human_readable(bytes_val: int) -> str:
    """Convert bytes to human readable format."""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if bytes_val < 1024.0:
            return f"{bytes_val:.1f} {unit}"
        bytes_val /= 1024.0
    return f"{bytes_val:.1f} PB"

def print_device_report_detailed(report: DeviceReportData):
    """Print device report with human-readable sizes."""
    if not report:
        print("No report data available")
        return
        
    # Convert timestamp to readable format
    timestamp_sec = report.timestamp_ms / 1000
    time_str = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(timestamp_sec))
    
    print(f"=== Device System Report ===")
    print(f"Timestamp: {time_str} ({report.timestamp_ms} ms)")
    print(f"Load Averages: 1min={report.record.load[0]}, 5min={report.record.load[1]}, 15min={report.record.load[2]}")
    
    # Convert uptime to readable format
    uptime_days = report.record.uptime // 86400
    uptime_hours = (report.record.uptime % 86400) // 3600
    uptime_minutes = (report.record.uptime % 3600) // 60
    print(f"Uptime: {uptime_days}d {uptime_hours}h {uptime_minutes}m ({report.record.uptime} seconds)")
    
    print("\n--- Memory Information ---")
    mem = report.record.mem_util
    mem_percent = (mem.mem_used / mem.mem_total * 100) if mem.mem_total > 0 else 0
    swap_percent = (mem.swap_used / mem.swap_total * 100) if mem.swap_total > 0 else 0
    
    print(f"RAM:  {convert_bytes_to_human_readable(mem.mem_used * 1024)} / {convert_bytes_to_human_readable(mem.mem_total * 1024)} ({mem_percent:.1f}% used)")
    print(f"Swap: {convert_bytes_to_human_readable(mem.swap_used * 1024)} / {convert_bytes_to_human_readable(mem.swap_total * 1024)} ({swap_percent:.1f}% used)")
    
    print(f"\n--- CPU Information ---")
    print(f"CPU Utilization: {report.record.cpu_util.cpu_util}%")
    
    print(f"\n--- Filesystem Information ---")
    fs_type_names = {0: "Root Filesystem", 1: "Temporary Filesystem"}
    for fs in report.record.fs_util:
        fs_name = fs_type_names.get(fs.fs_type, f"Filesystem Type {fs.fs_type}")
        fs_percent = (fs.fs_used / fs.fs_total * 100) if fs.fs_total > 0 else 0
        print(f"{fs_name}: {convert_bytes_to_human_readable(fs.fs_used * 1024)} / {convert_bytes_to_human_readable(fs.fs_total * 1024)} ({fs_percent:.1f}% used)")

if __name__ == "__main__":
    # Test the function
    print("Testing fill_dummy_device_report()...\n")
    
    # Generate dummy device report
    device_data = fill_dummy_device_report()
    
    # Print basic report
    print_device_report(device_data)
    
    print("\n" + "="*50 + "\n")
    
    # Print detailed report
    print_device_report_detailed(device_data)
    
    print("\n" + "="*50 + "\n")
    
    
    # Convert to JSON and print
    device_data_json = json.dumps(asdict(device_data), indent=4)
    print("Device Report in JSON format:")
    print(device_data_json)