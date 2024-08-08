# AccuKnox_assignment
This is assignment work for Accuknox

Using Docker
1. install Docker 
2. Clone the Repository:
   git clone https://github.com/tripathiashwani/AccuKnox_assignment.git
   cd AccuKnox_assignment
3. use git bash or any ubuntu terminal
4. do pwd and copy the current directory path
5. Run the command:
   export DIRR={copied path from pwd}
6. Build the Docker Image:
   docker-compose build
7. Run the Docker Container:
   docker-compose up -d
8. Access the Application:
   Open your web browser and go to http://localhost:8000.

Without Docker
1. Install Python
2. clone this repo
3. Create and Activate a Virtual Environment
   python3 -m venv env
   source env/bin/activate  # On Windows, use `env\Scripts\activate`
4. Install Dependencies:
   pip install -r requirements.txt
5. python manage.py migrate
   python manage.py migrate
6. Run the Development Server:
   python manage.py runserver
7. Access the Application:
   Open your web browser and go to http://localhost:8000.


#Please find API collections here 
https://api.postman.com/collections/30746322-b49c8abe-a8b8-45c8-a597-3e55acdb5ecf?access_key=PMAT-01J4R8EJZT0QH0NRJ5M878GQ4W

