# FLIGHT COMBINATIONS
<!-- FALTA REQUIREMENTS.TXT, GITIGNORE -->
Find all the possible combinations of flights with different bags allowed per passenger.

<br />

## SETUP

Run the following commands to setup environment:

``` 
git clone https://github.com/FranMacedo/flight_combinations.git
cd flight_combinations
python -m venv venv
.\venv\scripts\activate
pip install -r requirements.txt
```
<br />

## RUN IN COMMAND LINE

### Input
The expected input should be a csv file with the correct column names (see [this sample file](input.csv) for details)

### Run

Linux/Mac:
    ```
    cat <FILE_NAME.CSV> | python3 find_combinations.py          
    ```

Windows:
    ```
    type <FILE_NAME.CSV> | py find_combinations.py          
    ```

### Output
The expected outupt is a nested dictionary where the "parent keys" correspond to the number of bags allowed per passanger and the  "parent values" are lists of trips (each trip is a dictionary). For example:

```python
    {
        0: [
                {
                    'number_of_bags': 0,
                    'source': 'USM',
                    'destination': 'HKT',
                    ...
                },
                {
                    'number_of_bags': 0,
                    'source': 'HKT',
                    'destination': 'DPS',
                    ...
                }
            ],
        1: [
                {
                    'number_of_bags': 1,
                    'source': 'USM',
                    'destination': 'BWN',
                    ...
                },
                {
                    'number_of_bags': 1,
                    'source': 'HKT',
                    'destination': 'USM',
                    ...
                }
            ],
        ...
    }
```
Each trip has the following information:
```python
 trip = {
    'number_of_bags': int - 'number of bags this passenger wants to carry',
    'source': str - 'source airport code',
    'destination': str - 'destination airport code',
    'flights': list - 'all flights details that are included in this trip',
    'total_price': float - 'total price of the trip, including bags prices',
    'flight_time': float - 'total time in the air', 
    'transfer_time': float - 'total time in transfers',
    'number_of_transfers': int - 'number of transfers for this trip',
}

```

<br />

## RUN APP
There's a small app that allows the user to see flights (and respective details) per number of bags and to download all the trips data in `json` format.

### Input
The expected input should be a csv file named 'input.csv', located in the base/main directory, with the correct column names (see [this sample file](input.csv) for details)

### Run

Linux/Mac:
    ```
    python3 app.py          
    ```

Windows:
    ```
    py app.py                   
    ```

Open http://127.0.0.1:5000/ on your browser and enjoy :wink: