from django.core.management.base import BaseCommand
from django.conf import settings
from transactions.models import Transaction
import csv
import os

class Command(BaseCommand):
    """
    Management command to load transaction data from a CSV file into the database.

    This script checks for duplicate `transaction_id` entries before inserting records 
    to avoid violating the unique constraint.
    """
    help = 'Load transaction data from a CSV file into the database'

    def handle(self, *args, **kwargs):
        """
        Main entry point for the command. Reads the CSV file, processes each row,
        and inserts the data into the database while ensuring no duplicates are created.
        """
        # Construct the full path to the CSV file
        csv_file_path = os.path.join(settings.BASE_DIR, 'data', 'digital_wallet_transactions.csv')

        # Verify if the file exists
        if not os.path.exists(csv_file_path):
            self.stderr.write(f"File not found: {csv_file_path}")
            return

        self.stdout.write(f"Loading data from: {csv_file_path}")

        # Open and read the CSV file
        try:
            with open(csv_file_path, mode='r') as file:
                reader = csv.DictReader(file)
                added_count = 0
                skipped_count = 0

                # Process each row in the CSV file
                for row in reader:
                    # Check for duplicates based on transaction_id
                    if not Transaction.objects.filter(transaction_id=row['transaction_id']).exists():
                        Transaction.objects.create(
                            transaction_id=row['transaction_id'],
                            user_id=row['user_id'],
                            transaction_date=row['transaction_date'],
                            product_category=row['product_category'],
                            product_name=row['product_name'],
                            merchant_name=row['merchant_name'],
                            product_amount=row['product_amount'],
                            transaction_fee=row.get('transaction_fee', None),
                            cashback=row.get('cashback', None),
                            loyalty_points=row.get('loyalty_points', None),
                            payment_method=row['payment_method'],
                            transaction_status=row['transaction_status'],
                            merchant_id=row.get('merchant_id', None),
                            device_type=row['device_type'],
                            location=row['location'],
                        )
                        added_count += 1
                    else:
                        # Log skipped entries
                        self.stdout.write(f"Skipped duplicate transaction_id: {row['transaction_id']}")
                        skipped_count += 1

                # Print a summary of the operation
                self.stdout.write(f"Data loading completed. {added_count} records added, {skipped_count} duplicates skipped.")

        except Exception as e:
            # Handle unexpected errors gracefully
            self.stderr.write(f"An error occurred: {str(e)}")
