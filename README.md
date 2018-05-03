A quick project to test out the usage of the City of Melbourne data API

## Parking

Find out about parking signs in the city of Melbourne.

Browse a map to see what the parking restrictions are for an area, and optionally filter on meters, disabilities and time limits.

Uses the city of melbourne data api to process requests.

#### API usage

retrieve parking bay information

GET /api/v1/bays

params

    latitude: str                latitude of search area
    longitude: str               longitude of search area
    radius: int                  radius of search area (metres)

##### todo

 - Build front end
 - React to Date/Time of input
 - React to disability input
