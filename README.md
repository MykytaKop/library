# Library Api

Api service for library management written on DRF   

# Features:
- JWT authenticated
- Admin panel /admin/
- Documentation is located at api/schema/documentation/
- Managing books
- Creating borrowings
- Filtering borrowings by user ids and is active field

# Installing using GitGub

Install PostgresSQL and create db
``` 
1. git clone https://github.com/MykytaKop/library.git
2. cd library
3. python - venv venv
4. For wondows: venv\Scripts\activate
   For macOS: source venv/bin/activate
5. pip install -r requirements.txt
6. set DB_HOST=<your db hostname>
7. set DB_NAME=<your db name>
8. set DB_USER=<your db username>
9. set DB_PASSWORD=<your db user password>
10. set SECRET_KEY=<your secret key>
11. python manage.py migrate
12. python manage.py runserver
```

# Run with docker

Docker should be installed

```
docker-compose build
docker-compose up
```

# Getting access:

- create user via /api/user/
- get access token /api/user/token/


