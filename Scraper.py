#How to fetch data from website and store in a SQL database
#Code by Rishabh
import requests
import sqlite3
from bs4 import BeautifulSoup

#Fetch the data from the website
URL = "https://realpython.github.io/fake-jobs/"
page = requests.get(URL)

#parse the gathered data as HTML
soup = BeautifulSoup(page.content, "html.parser")

#Clear out the Soup - Find the content of job postings and store as a list named content
listings = soup.find(id="ResultsContainer")
content = listings.find_all("div", class_="card-content")

#empty lists for each column name
title = []
location = []
company = []

#fill out the initiated lists with relevant data such as job_titles and location
for item in content:
    title.append(item.find("h2", class_= "title is-5").text.strip())
    location.append(item.find("p", class_="location").text.strip())
    company.append(item.find("h3", class_ = "subtitle is-6 company").text.strip())

#SQL PART
#connect and make a new database job_data.db in SQLite3
connection = sqlite3.connect("job_data.db")
cursor = connection.cursor() #set the cursor to perform the SQL queries

#execute the SQL Query from within Python to create three columns within the job_data db - job_title, job_location and job_company
cursor.execute('''
    CREATE TABLE IF NOT EXISTS job_data (
        job_title TEXT,
        job_company TEXT,
        job_location TEXT
    )
'''
)

#fill out the columns using earlier prepared lists, use placeholders
for i in range(len(title)):
    cursor.execute('''
        INSERT INTO job_data (job_title, job_company, job_location)
        VALUES (?, ?, ?)
        ''', (title[i], company[i], location[i])
        )

#commit the changes to the DB and close the DB
connection.commit()
connection.close()

#make another connection request to the DB
connection = sqlite3.connect("job_data.db")
cursor = connection.cursor() #set the cursor

#Execute a SQL command to filter out the job titles relevant to Python Developement
cursor.execute("SELECT * FROM job_data WHERE job_title LIKE ?", ("%python%",)) #used placeholder "?" to complete the SQL Query. For such cases, need to supply the value of placeholder as a tuple with one empty value such as ("string",)

#use cursor's fetchall() method to retrive the results. The results are in the form a tuple corresponding to each row
rows = cursor.fetchall()


for row in rows:
    # Process each row as needed
    print(row)

# Close the database connection
cursor.close()
connection.close()