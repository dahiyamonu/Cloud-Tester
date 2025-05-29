from import_export import resources, fields
from import_export.widgets import CharWidget
from .models import Device

class DeviceResource(resources.ModelResource):
    serial_number = fields.Field(
        column_name='SN',  # Match Excel header exactly
        attribute='serial_number',
        widget=CharWidget()
    )
    alias = fields.Field(
        column_name='Alias',  # Match Excel header exactly
        attribute='alias',
        widget=CharWidget()
    )

    class Meta:
        model = Device
        import_id_fields = ['serial_number']
        fields = ('serial_number', 'alias',)
        skip_unchanged = True
        report_skipped = True

    # def skip_row(self, instance, original):
    #     # Skip if serial number exists and no change needed
    #     if original and instance.alias == original.alias:
    #         return True
    #     return False
