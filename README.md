# Darkweb Scraper

This project is a Python-based web scraper for .onion sites on the darkweb. It uses BeautifulSoup for web scraping, PyMongo for MongoDB interaction, and routes requests through the Tor network for .onion site access. The project is structured as a Docker stack with three containers: a web application, a scraper, and a MongoDB database.

## Setup

1. Install Docker and Docker Compose on your machine.
2. Tor installed on your machine. The scraper uses Tor to access .onion sites, so it's necessary to have Tor installed and correctly configured.
3. Build the Docker images and start the services: `docker-compose up --build`

## Project Structure

- `docker-compose.yml`: Defines the services, networks, and volumes for the Docker stack.
- `webapp/`: Directory for the web application container. Contains a Dockerfile and the web application code.
- `scraper/`: Directory for the scraper container. Contains a Dockerfile and the scraper code.
- `db/`: Directory for the MongoDB container. Contains a Dockerfile and the database setup scripts.

## Usage

Once the Docker stack is running, you can access the web application at `localhost:5000`. From there, you can add more .onion links to the scrape table and view the information from each individual table.

The scraper will automatically start and begin scraping the .onion sites listed in the MongoDB database. It will store the product information it finds in a new table in the database.

## Database Structure

The MongoDB database contains three tables:

1. `onion_links`: Stores the .onion links to be scraped.
2. `template`: A template table for .onion links.
3. `scraped_data`: Stores the data scraped from the .onion sites.


##ROugh plan
okay so here is the plan: 

i am going to build out a docker stack. 

container 1: 
    - webapp where the user can go and add more links to the scrape table and be able to look at all the information from each individual table.

Container 2: 
- the main container. hosts the scraper connection to tor as well as the socks5 proxy and any other needed information (Database conecctions etc )

container 3: 
- the database(mongo db)
- will have three seperate tables
    1. the table that has all the .onion links 
    2. the template table for .onion links 
    3. x amount of tables that pulls from the tempalte table to populate the scraped info 