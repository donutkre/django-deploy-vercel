from django.contrib import admin
from .models import Transaction

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Transaction model.

    Provides a user-friendly interface with filtering, searching, and display options
    to easily manage transaction records.
    """
    # Fields to display in the admin list view
    list_display = ('transaction_id', 'user_id', 'transaction_date', 'product_name', 'product_amount', 'payment_method')

    # Fields that can be used for searching
    search_fields = ('transaction_id', 'user_id', 'product_name', 'merchant_name')

    # Filters available in the sidebar
    list_filter = ('transaction_date', 'product_category', 'payment_method', 'transaction_status', 'location')

    # Read-only fields to prevent accidental edits for important attributes
    readonly_fields = ('transaction_id', 'transaction_date', 'merchant_name', 'product_amount')

    # Customize the ordering of records
    ordering = ('-transaction_date',)

    # Fieldsets for organizing the edit view
    fieldsets = (
        ("Basic Information", {
            'fields': ('transaction_id', 'user_id', 'transaction_date', 'product_name', 'product_category', 'merchant_name')
        }),
        ("Financial Details", {
            'fields': ('product_amount', 'transaction_fee', 'cashback', 'loyalty_points')
        }),
        ("Transaction Details", {
            'fields': ('payment_method', 'transaction_status', 'merchant_id', 'device_type', 'location')
        }),
    )

    # Add the ability to export selected records as CSV
    actions = ['export_as_csv']

    def export_as_csv(self, request, queryset):
        """
        Custom action to export selected transactions as a CSV file.
        """
        import csv
        from django.http import HttpResponse

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="transactions.csv"'

        writer = csv.writer(response)
        writer.writerow([field.name for field in Transaction._meta.fields])  # Write headers
        for transaction in queryset:
            writer.writerow([getattr(transaction, field.name) for field in Transaction._meta.fields])  # Write rows

        self.message_user(request, f"{queryset.count()} transactions exported successfully!")
        return response

    export_as_csv.short_description = "Export selected transactions as CSV"
