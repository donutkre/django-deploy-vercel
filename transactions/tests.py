from django.urls import reverse
from django.utils.timezone import now
from transactions.models import Transaction
from rest_framework import status
from rest_framework.test import APITestCase


class TransactionAPITest(APITestCase):
    def setUp(self):
        """Set up initial test data."""
        self.transaction1 = Transaction.objects.create(
            transaction_id="tx1",
            user_id="user1",
            transaction_date=now(),
            product_category="Electronics",
            product_name="Laptop",
            merchant_name="BestBuy",
            product_amount=1200.50,
            transaction_fee=10.50,
            cashback=20.00,
            loyalty_points=100,
            payment_method="Credit Card",
            transaction_status="Successful",
            merchant_id="m1",
            device_type="iOS",
            location="Urban",
        )

    def test_get_transactions(self):
        """Test retrieving all transactions."""
        url = reverse('transaction-list')  # Ensure the URL name matches 'transaction-list'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_transaction(self):
        """Test creating a new transaction."""
        url = reverse('transaction-list')  # Ensure the URL name matches 'transaction-list'
        payload = {
            "transaction_id": "tx2",
            "user_id": "user2",
            "transaction_date": now().isoformat(),
            "product_category": "Books",
            "product_name": "Fiction Novel",
            "merchant_name": "Amazon",
            "product_amount": 50.00,
            "transaction_fee": 1.50,
            "cashback": 0.50,
            "loyalty_points": 10,
            "payment_method": "UPI",
            "transaction_status": "Successful",
            "merchant_id": "m2",
            "device_type": "Web",
            "location": "Rural",
        }
        response = self.client.post(url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Transaction.objects.count(), 2)

    def test_get_transaction_detail(self):
        """Test retrieving a single transaction by ID."""
        url = reverse('transaction-detail', args=[self.transaction1.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['transaction_id'], "tx1")

    def test_update_transaction(self):
        """Test updating an existing transaction."""
        url = reverse('transaction-detail', args=[self.transaction1.id])
        payload = {
            "transaction_id": "tx1",
            "user_id": "user1",
            "transaction_date": self.transaction1.transaction_date.isoformat(),
            "product_category": "Electronics",
            "product_name": "Updated Laptop",
            "merchant_name": "BestBuy",
            "product_amount": 1500.00,
            "transaction_fee": 10.50,
            "cashback": 20.00,
            "loyalty_points": 150,
            "payment_method": "Credit Card",
            "transaction_status": "Successful",
            "merchant_id": "m1",
            "device_type": "iOS",
            "location": "Urban",
        }
        response = self.client.put(url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_transaction(self):
        """Test deleting a transaction by ID."""
        url = reverse('transaction-detail', args=[self.transaction1.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_filter_transactions(self):
        """Test filtering transactions."""
        url = reverse('filter-transactions')  # Ensure the URL name matches 'filter-transactions'
        response = self.client.get(url, {'product_category': 'Electronics'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_aggregate_by_user(self):
        """Test aggregating transactions."""
        url = reverse('aggregate-by-user')  # Ensure the URL name matches 'aggregate-by-user'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_export_transactions(self):
        """Test exporting transactions."""
        url = reverse('export-transactions')  # Ensure the URL name matches 'export-transactions'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('text/csv', response['Content-Type'])
