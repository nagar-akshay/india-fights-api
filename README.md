# Quick Setup Instructions
## Prerequisites
-	Docker 
-	Python
## Instructions
- Create new virtualenv `python -m venv ./venv`
- Activate venv `source venv/bin/activate` (if Linux). `venv\Scripts\activate.bat` if windows. Mac Idk
- Start a simple mariadb instance using docker `docker run --name my-mariadb -e MYSQL_ROOT_PASSWORD=admin123 -p 3306:3306 -d mariadb:latest
`
- Create ifapi DB `docker exec -it my-mariadb mysql -u root -p -e "CREATE DATABASE ifapi;"
`
- Install all project requirements `pip install -r requirements.txt`
- Start fastapi server `uvicorn main:app --reload` (change port using --port argument)
- Head over `http://localhost:8000/docs` to check API documentation 