# Simple Anomaly Detection in Time Series via Optimal Baseline Subtraction (OBS)
**Anomaly detection** in time series is used to identify unexpected patterns in your time series, and it is widely applied in different fields. In **energy engineering**, a spike in power usage might signal a fault. In **finance**, sudden drops or peaks can indicate major market events. In **mechanical systems**, unusual vibrations may reveal early signs of failure. In this blogpost, we will use **weather data** as an example use case, and we will find the anomalies in temperature time series for different cities all over the world.  

## Optimal Baseline Subtraction (OBS) Description

### OBS Introduction

If you have a bank of time series and you want to understand if and in what portion of the time series you have an anomaly, a simple but very efficient metod is called **optimal baseline subtraction (OBS)**. OBS is based on comparing each time series segment to the most similar historical pattern and analyzing the difference to detect unexpected deviations. 

### OBS Algorithm

The OBS algorithm is the following:

- **Split the time series into individual segments**, where each segment represents a unit of repeated behavior (e.g., a day, a cycle, or a process run).
- **Build a library of historical segments** by collecting all previous segments in the time series bank.
- **Compare your target segment** with all other segments in the library using a similarity metric, such as Mean Absolute Error (MAE).
- **Select the most similar segment** from the library as the optimal baseline.
- **Subtract the baseline from the target segment** to isolate the residual (i.e., the difference).
- **Analyze the residual** to identify large deviations, which are flagged as potential anomalies.

![Alt text](images/Workflow.png)



## Optimal Baseline Subtraction Application

### Script folder

You can find all the code and data you need in this [public github folder](https://github.com/PieroPaialungaAI/OptimalBaselineSubtraction.git), that you can download with:

```bash
git clone https://github.com/PieroPaialungaAI/OptimalBaselineSubtraction.git
```

### Data Source

The data used for this article originally come from an Open Database on Kaggle. You can find the original source of the dataset [here](https://www.kaggle.com/datasets/selfishgene/historical-hourly-weather-data). Nonetheless, note that **you don't need to download it again, as everything you need is in the ```OBS_Data``` folder.**

### Preprocessed Data

The "preprocessing" part of the data is handled by the ```data.py``` code, so we can just deal with the fun stuff here. 

A table with the attributes for the cities can be found in the ```.city_attribute_data```:

```python
from data import *
data = TimeSeriesData()
data.city_attribute_data.head()
```

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>City</th>
      <th>Country</th>
      <th>Latitude</th>
      <th>Longitude</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>Vancouver</td>
      <td>Canada</td>
      <td>49.249660</td>
      <td>-123.119339</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Portland</td>
      <td>United States</td>
      <td>45.523449</td>
      <td>-122.676208</td>
    </tr>
    <tr>
      <th>2</th>
      <td>San Francisco</td>
      <td>United States</td>
      <td>37.774929</td>
      <td>-122.419418</td>
    </tr>
    <tr>
      <th>3</th>
      <td>Seattle</td>
      <td>United States</td>
      <td>47.606209</td>
      <td>-122.332069</td>
    </tr>
    <tr>
      <th>4</th>
      <td>Los Angeles</td>
      <td>United States</td>
      <td>34.052231</td>
      <td>-118.243683</td>
    </tr>
  </tbody>
</table>
</div>



While the correspoding time series can be found in the  ```.temperature_data```, where each column represents a city, and the ```.datetime``` is the time step column. For example, the data for the city of **Vancouver** are the following:


```python
data.temperature_data[['Vancouver','datetime']].head()
```

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Vancouver</th>
      <th>datetime</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>284.630000</td>
      <td>2012-10-01 13:00:00</td>
    </tr>
    <tr>
      <th>1</th>
      <td>284.629041</td>
      <td>2012-10-01 14:00:00</td>
    </tr>
    <tr>
      <th>2</th>
      <td>284.626998</td>
      <td>2012-10-01 15:00:00</td>
    </tr>
    <tr>
      <th>3</th>
      <td>284.624955</td>
      <td>2012-10-01 16:00:00</td>
    </tr>
    <tr>
      <th>4</th>
      <td>284.622911</td>
      <td>2012-10-01 17:00:00</td>
    </tr>
  </tbody>
</table>
</div>


### Selecting the Target Segment

So let's say we have our dataset and we want to see if there is an anomaly in a specific section. The following code pulls the city of interest and allows you to pick a specific window (e.g. a day, a week or a month) for that specific city. For example, let's pick **day** number **10** for **city = New York**.


```python
city = 'New York'
segment_class = 'day'
segment_idx = 10
data.isolate_city_and_time(city = city, segment_idx = segment_idx, segment_class = segment_class)
data.plot_target_and_baseline()
```
    
![png](OBS_Notebook_files/OBS_Notebook_5_0.png)
    

### Selecting the Bank of Candidates

As we selected our city, window and index, all the remaining windows form your bank of candidates. For example, for our **day** window, our segments have 24 points (one per hour). For this reason the list of candidates will have shape ```(number of days - 1, 24)```. 


```python
data.list_of_candidates.shape
```




    (1853, 24)



Let's display some random candidates using the ```plot_target_and_candidates``` via the ```baseline_vs_candidates_plotter```.


```python
data.plot_target_and_candidates()
```


    
![png](OBS_Notebook_files/OBS_Notebook_9_0.png)
    


### Selecting the optimal baseline  
In this step, we will use the MAE metric to find the time series that is the closest to our target in the list of candidates. 
The result of the OBS algorithm can be found here:
```python
optimal_baseline_data = data.find_optimal_baseline()
optimal_baseline_data
```




    {'optimal_baseline_curve': array([283.58730199, 283.48      , 284.11087113, 283.24      ,
            283.28088357, 283.4       , 283.53025526, 283.87      ,
            284.30413177, 283.83      , 283.77051025, 283.59      ,
            283.64469697, 283.81      , 284.52073246, 284.93      ,
            285.29078699, 286.3       , 286.47010182, 286.95      ,
            287.10322709, 288.16      , 288.11346276, 287.96      ]),
     'optimal_baseline_diff': array([0.12269801, 0.22      , 0.92087113, 0.17      , 0.22088357,
            0.46      , 0.66025526, 0.49      , 0.78413177, 0.15666667,
            0.05615642, 0.39      , 0.25530303, 0.4       , 0.78926754,
            0.69      , 0.98921301, 0.95      , 0.83989818, 0.36      ,
            0.07677291, 1.69      , 0.57846276, 0.64      ]),
     'optimal_baseline_error': 0.5379408442499999,
     'target_curve': array([283.71      , 283.26      , 283.19      , 283.07      ,
            283.06      , 282.94      , 282.87      , 283.38      ,
            283.52      , 283.67333333, 283.82666667, 283.98      ,
            283.9       , 284.21      , 285.31      , 285.62      ,
            286.28      , 287.25      , 287.31      , 287.31      ,
            287.18      , 286.47      , 287.535     , 288.6       ])}



### Displaying the Optimal Baseline:
If we plot the optimal baseline vs the target curve, we see the following plot:
```python
data.plot_target_and_optimal_baseline()
``` 
![png](OBS_Notebook_files/OBS_Notebook_14_0.png)
  
```python

```
