import pandas as pd
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Device
from .forms import UploadFileForm

def import_devices(request):
    """Handles importing devices from an uploaded Excel file."""
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES["file"]

            try:
                df = pd.read_excel(file)

                # Validate required columns
                required_columns = {"Serial Number", "Device Name"}
                if not required_columns.issubset(df.columns):
                    return HttpResponse("Invalid file format. Required columns: Serial Number, Device Name", status=400)

                for _, row in df.iterrows():
                    Device.objects.update_or_create(
                        serial_number=row["Serial Number"],
                        defaults={"name": row["Device Name"]}
                    )

                return redirect("device_list")

            except Exception as e:
                return HttpResponse(f"Error processing file: {e}", status=400)
    
    else:
        form = UploadFileForm()

    return render(request, "imp_exp/import_devices.html", {"form": form})  # Fixed indentation
def export_devices(request):
    """Handles exporting devices to an Excel file."""
    devices = Device.objects.all().values("name", "serial_number")
    
    if not devices.exists():
        return HttpResponse("No devices to export.", status=204)

    df = pd.DataFrame(devices)

    response = HttpResponse(
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    response["Content-Disposition"] = 'attachment; filename="devices.xlsx"'

    with pd.ExcelWriter(response, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="Devices")

        # Adjust column width (optional)
        worksheet = writer.sheets["Devices"]
        for col in worksheet.columns:
            max_length = max([len(str(cell.value)) if cell.value else 0 for cell in col])
            col_letter = col[0].column_letter
            worksheet.column_dimensions[col_letter].width = max_length + 2

    return response
