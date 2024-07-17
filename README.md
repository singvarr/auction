# Auction

Django server for management of auctions.

## Features

- An admin can create, start and finish an auction.
- An authenticated user can participate in auction and make a bid.
- A guest user can view list of auctions and auction details.

## Tech functionality

- JWT auth
- File upload
- WebSocket notifications (via Pusher)

## Setup and running of application

Make sure that Docker installed prior the setup of application

1. Create `.env` file in the root of the project
2. Build containers using `docker-compose up --build`
3. Run migrations inside container if necessary - `docker-compose exec auction-api pipenv run python manage.py migrate`.
4. Open the server on http://localhost:8000.
