from django.db import models

class Transaction(models.Model):
    """
    Represents a financial transaction in the wallet application.

    Attributes:
        transaction_id (str): Unique identifier for the transaction.
        user_id (str): Identifier for the user who performed the transaction.
        transaction_date (datetime): The date and time of the transaction.
        product_category (str): Category of the product involved in the transaction (e.g., "Food", "Travel").
        product_name (str): Name of the product or service purchased.
        merchant_name (str): Name of the merchant providing the product/service.
        product_amount (decimal): Total cost of the product/service.
        transaction_fee (decimal, optional): Any fees associated with the transaction.
        cashback (decimal, optional): Cashback received for the transaction.
        loyalty_points (int, optional): Loyalty points earned from the transaction.
        payment_method (str): The method used for payment (e.g., "Credit Card", "UPI").
        transaction_status (str): Status of the transaction (e.g., "Successful", "Pending").
        merchant_id (str, optional): Identifier for the merchant.
        device_type (str): Type of device used for the transaction (e.g., "iOS", "Android").
        location (str): Location where the transaction occurred.
    """
        
    transaction_id = models.CharField(max_length=100, unique=True)
    user_id = models.CharField(max_length=100)
    transaction_date = models.DateTimeField()
    product_category = models.CharField(max_length=100)
    product_name = models.CharField(max_length=200)
    merchant_name = models.CharField(max_length=200)
    product_amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_fee = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    cashback = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    loyalty_points = models.IntegerField(null=True, blank=True)
    payment_method = models.CharField(max_length=50)
    transaction_status = models.CharField(max_length=50)
    merchant_id = models.CharField(max_length=100, null=True, blank=True)
    device_type = models.CharField(max_length=50)
    location = models.CharField(max_length=200)

    def __str__(self):
        return self.transaction_id
