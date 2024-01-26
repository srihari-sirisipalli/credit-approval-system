
# Credit Approval System

This is a Django application for managing credit approvals.

## Getting Started

These instructions will guide you on how to set up and run the project using Docker.

### Prerequisites

Make sure you have Docker and Docker Compose installed on your machine.

- [Docker Installation Guide](https://docs.docker.com/get-docker/)
- [Docker Compose Installation Guide](https://docs.docker.com/compose/install/)

### Running the Application

1. Clone the repository:

   ```bash
   git clone https://github.com/srihari-sirisipalli/credit-approval-system.git
   cd credit-approval-system
   ```

2. Configure DATABASES in setting.py in credit-approval_system for docker
   ``` bash
   'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'credit_approval_db',
        'USER': 'sri',
        'PASSWORD': '123',
        'HOST': 'postgres_db',
        'PORT': '5432',
    }
   ```

3. Build and start the Docker containers:

   ```bash
   docker-compose up --build
   ```

   This will start the PostgreSQL database and the Django application.



4. Run  in Docker shell:

   ```bash
   docker-compose exec django_app /bin/bash
   ```
   Note : Use new terminal for shell
5. Access APIs
```bash
http://0.0.0.0:8000
```

6. Test in Docker Shell
    ```bash
   python manage.py test credit_app.tests
   ```
    


### Cleanup

To stop and remove the Docker containers, run:

```bash
docker-compose down
```

## Contributing

Feel free to contribute to the project by opening issues or creating pull requests.


## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
