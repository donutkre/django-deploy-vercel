from django.db.models import Sum
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework import status
from .models import Transaction
from .serializers import TransactionSerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
import csv
from django.http import HttpResponse


class TransactionList(APIView):
    @swagger_auto_schema(
        operation_description="Retrieve a list of all transactions",
        responses={200: TransactionSerializer(many=True)}
    )
    def get(self, request):
        transactions = Transaction.objects.all()
        serializer = TransactionSerializer(transactions, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_description="Create a new transaction",
        request_body=TransactionSerializer,
        responses={201: TransactionSerializer, 400: "Invalid Data"}
    )
    def post(self, request):
        serializer = TransactionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TransactionDetail(APIView):
    @swagger_auto_schema(
        operation_description="Retrieve a single transaction by ID",
        responses={200: TransactionSerializer}
    )
    def get(self, request, pk):
        transaction = Transaction.objects.get(pk=pk)
        serializer = TransactionSerializer(transaction)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_description="Update a transaction by ID",
        request_body=TransactionSerializer,
        responses={200: TransactionSerializer, 400: "Invalid Data"}
    )
    def put(self, request, pk):
        transaction = Transaction.objects.get(pk=pk)
        serializer = TransactionSerializer(transaction, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description="Delete a transaction by ID",
        responses={204: "No Content"}
    )
    def delete(self, request, pk):
        transaction = Transaction.objects.get(pk=pk)
        transaction.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class FilterTransactionsView(APIView):
    @swagger_auto_schema(
        operation_description="Filter transactions by date range, category, merchant, or payment method",
        manual_parameters=[
            openapi.Parameter('start_date', openapi.IN_QUERY, description="Start date (YYYY-MM-DD)", type=openapi.TYPE_STRING),
            openapi.Parameter('end_date', openapi.IN_QUERY, description="End date (YYYY-MM-DD)", type=openapi.TYPE_STRING),
            openapi.Parameter('product_category', openapi.IN_QUERY, description="Product category", type=openapi.TYPE_STRING),
            openapi.Parameter('merchant_name', openapi.IN_QUERY, description="Merchant name (partial matches allowed)", type=openapi.TYPE_STRING),
            openapi.Parameter('payment_method', openapi.IN_QUERY, description="Payment method", type=openapi.TYPE_STRING),
        ],
        responses={200: TransactionSerializer(many=True)}
    )
    def get(self, request):
        queryset = Transaction.objects.all()
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')
        product_category = request.query_params.get('product_category')
        merchant_name = request.query_params.get('merchant_name')
        payment_method = request.query_params.get('payment_method')

        if start_date and end_date:
            queryset = queryset.filter(transaction_date__range=[start_date, end_date])
        if product_category:
            queryset = queryset.filter(product_category=product_category)
        if merchant_name:
            queryset = queryset.filter(merchant_name__icontains=merchant_name)
        if payment_method:
            queryset = queryset.filter(payment_method=payment_method)

        serializer = TransactionSerializer(queryset, many=True)
        return Response(serializer.data)


class AggregateByUserView(APIView):
    @swagger_auto_schema(
        operation_description="Aggregate total spending by each user",
        responses={200: "Aggregated data showing user_id and total spending"}
    )
    def get(self, request):
        aggregated_data = Transaction.objects.values('user_id').annotate(
            total_spent=Sum('product_amount')
        ).order_by('-total_spent')
        return Response(aggregated_data)


class GroupedTransactionsView(APIView):
    @swagger_auto_schema(
        operation_description="Group transactions by location and merchant, with total spending",
        responses={200: openapi.Schema(
            type=openapi.TYPE_ARRAY,
            items=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'location': openapi.Schema(type=openapi.TYPE_STRING, description="Location of transaction"),
                    'merchant_name': openapi.Schema(type=openapi.TYPE_STRING, description="Merchant name"),
                    'total_spent': openapi.Schema(type=openapi.TYPE_NUMBER, description="Total amount spent"),
                }
            )
        )}
    )
    def get(self, request):
        grouped_data = Transaction.objects.values('location', 'merchant_name').annotate(
            total_spent=Sum('product_amount')
        ).order_by('-total_spent')
        return Response(grouped_data)
    

class PaginatedTransactionsView(ListAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    pagination_class = PageNumberPagination

    @swagger_auto_schema(
        operation_description="Retrieve paginated transactions",
        responses={200: TransactionSerializer(many=True)}
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class ExportTransactionsView(APIView):
    @swagger_auto_schema(
        operation_description="Export all transactions to a CSV file",
        responses={200: "CSV file containing transaction data"},
        security=[{"Bearer": []}]  # Add security schema for token-based authentication
    )
    def get(self, request):
        # Set content type and headers for CSV response
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="transactions.csv"'

        # Write the CSV data
        writer = csv.writer(response)
        writer.writerow(['Transaction ID', 'User ID', 'Product Category', 'Amount', 'Date'])
        for transaction in Transaction.objects.all():
            writer.writerow([
                transaction.transaction_id,
                transaction.user_id,
                transaction.product_category,
                transaction.product_amount,
                transaction.transaction_date
            ])

        return response
