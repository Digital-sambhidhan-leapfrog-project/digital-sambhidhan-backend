# Smart-Laywer Backend

Backend for Smart-Laywer.

## How to run:



1. Rename `.env.example` -> `.env`

2. In `.env`:
    - Insert your email address in `MAIL_USERNAME` and `MAIL_FROM`
    - Insert your email password in `MAIL_PASSWORD`.

    This will setup mail service that will be used to send verification token to registered and unverified users.

3. For the initial setup, you need to build the image which can be done using

    **Note: You need docker installed in your system.**
    ```bash
    docker-compose build
    ```

4. To run the project
    ```bash
    docker-compose up
    ```

The API endpoints will be available on <a href=http://localhost:8000>http://localhost:8000</a>. To check all the endpoints, you can see at <a href="http://localhost:8000/docs">http://localhost:8000/docs</a>.