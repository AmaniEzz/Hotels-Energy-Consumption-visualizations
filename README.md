## Setup

The first thing to do is to clone the repository:

```sh
$ git clone https://github.com/AmaniEzz/Hotels-Energy-Consumption-visualizations.git
$ cd Hotels-Energy-Consumption-visualizations
$ python manage.py migrate
$ python manage.py runserver
```

And navigate to `http://127.0.0.1:8000/`.

## Walkthrough


### Step 1: Upload all csv files

<img src="https://github.com/AmaniEzz/Hotels-Energy-Consumption-visualizations/blob/main/media/upload.png" width="400" />

#### Inserting 93000 rows into the database took only 2 minutes (thanks to bulk creation)
---------------

### Step 2: A table with all hotels show up

<img src="https://github.com/AmaniEzz/Hotels-Energy-Consumption-visualizations/blob/main/media/table.png" width="400" />

----
# Step 2: Navigate to the desired Hotel to explore it's data

<img src="https://github.com/AmaniEzz/Hotels-Energy-Consumption-visualizations/blob/main/media/chart.png" width="400" />

#### Chart Explanation

#### For each Hotel, I calculated the total sum of consumption for each electricity supply meter, this gives us insights about which electricity supply do each hotel consume the most.


----------
