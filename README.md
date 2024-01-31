# Hello Quix template

This basic template contains:

A real time data processing pipeline with these services:

 - CSV data source - A continuously looping data source containing timestamp, number and name.
 - Name counter - In this stateful service we count the number of times we encounter each name from the CSV data.
 - Console logger - This destination service simply logs the data being recieved to the console. Adapt it to suit your needs.

We have also included a `docker-compose.yml` file so you can run the whole pipeline locally, including the message broker.
