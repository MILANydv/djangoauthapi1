from finance.serializers import ExpenditureSerializer, IncomeSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .models import Expenditure, Income
from django.http import Http404

class IncomeListCreateAPIView(APIView):
    def get(self, request):
        incomes = Income.objects.all()
        serializer = IncomeSerializer(incomes, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = IncomeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class IncomeRetrieveUpdateDestroyAPIView(APIView):
    def get_object(self, pk):
        try:
            return Income.objects.get(pk=pk)
        except Income.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        income = self.get_object(pk)
        serializer = IncomeSerializer(income)
        return Response(serializer.data)

    def put(self, request, pk):
        income = self.get_object(pk)
        serializer = IncomeSerializer(income, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        income = self.get_object(pk)
        income.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ExpenditureListCreateAPIView(APIView):
    def get(self, request):
        expenditures = Expenditure.objects.all()
        serializer = ExpenditureSerializer(expenditures, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ExpenditureSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ExpenditureRetrieveUpdateDestroyAPIView(APIView):
    def get_object(self, pk):
        try:
            return Expenditure.objects.get(pk=pk)
        except Expenditure.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        expenditure = self.get_object(pk)
        serializer = ExpenditureSerializer(expenditure)
        return Response(serializer.data)

    def put(self, request, pk):
        expenditure = self.get_object(pk)
        serializer = ExpenditureSerializer(expenditure, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        expenditure = self.get_object(pk)
        expenditure.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)