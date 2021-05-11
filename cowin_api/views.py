from django.shortcuts import render
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view
import requests
import json
import copy
from rest_framework.views import APIView
# Create your views here.c
class GetBeneficiaries(APIView):
    def get(self, request, id=None, date=None):

        url = f"https://cdn-api.co-vin.in/api/v2/appointment/beneficiaries"
        base_request_header = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36',
            }
        token="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX25hbWUiOiJhZTRjZDAwYS02ZGI4LTQ2NzUtYjgxOS01ZmIxYzBmNWJjYTYiLCJ1c2VyX2lkIjoiYWU0Y2QwMGEtNmRiOC00Njc1LWI4MTktNWZiMWMwZjViY2E2IiwidXNlcl90eXBlIjoiQkVORUZJQ0lBUlkiLCJtb2JpbGVfbnVtYmVyIjo5MzcwNjY3OTg4LCJiZW5lZmljaWFyeV9yZWZlcmVuY2VfaWQiOjgwMjk3OTk2MzY5NzAwLCJzZWNyZXRfa2V5IjoiYjVjYWIxNjctNzk3Ny00ZGYxLTgwMjctYTYzYWExNDRmMDRlIiwidWEiOiJNb3ppbGxhLzUuMCAoTWFjaW50b3NoOyBJbnRlbCBNYWMgT1MgWCAxMF8xMF8xKSBBcHBsZVdlYktpdC81MzcuMzYgKEtIVE1MLCBsaWtlIEdlY2tvKSBDaHJvbWUvMzkuMC4yMTcxLjk1IFNhZmFyaS81MzcuMzYiLCJkYXRlX21vZGlmaWVkIjoiMjAyMS0wNS0wOVQxNTozODo0Mi4yMDBaIiwiaWF0IjoxNjIwNTc0NzIyLCJleHAiOjE2MjA1NzU2MjJ9.l1cT1Xp-vOwbmjdCJAjhgKyLfQXxYefh4rhaetn8Tyg"
        headers = copy.deepcopy(base_request_header)
        #headers["Accept"] = "application/json"
        headers["Authorization"] = f"Bearer {token}"
        r = json.loads(requests.get(url, headers=headers).content)
        print(r)
        return Response(r)

