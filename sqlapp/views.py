from django.shortcuts import render, redirect
from django import forms
from django.http import HttpResponseRedirect
from django.urls import reverse
import mysql.connector


# Create your views here.

mydb = mysql.connector.connect(
host="localhost",
user="dbadmin",
password="12345",
database="University"
)

mycursor = mydb.cursor()

def index(request):
    data_query = "SELECT * FROM Student"
    mycursor.execute(data_query)
    myresult = mycursor.fetchall()

    table_name = data_query.split()[3]

    columns = mycursor.column_names

    return render(request, "sqlapp/index.html", {
        "myresult": myresult,
        "table_name": table_name,
        "columns": columns
    })

def search(request):
    query = request.GET['q']

    #data_query = "SELECT * FROM " + query

    try:
        mycursor.execute(query)
        myresult = mycursor.fetchall()

        columns = mycursor.column_names

        table_name = query.split()[3].capitalize()

        return render(request, "sqlapp/index.html", {
            "myresult": myresult,
            "table_name": table_name,
            "columns": columns
        })
    except:
        return redirect('index')

def insert(request):
    if request.method == 'POST':
        query = request.POST.get('p')

        try:
            mycursor.execute(query)
            mydb.commit()

        except:
            return redirect('index')

    return redirect('index')


