# Text Planner takes data as input and produces text plans

import re
from typing import List
import pandas as pd
from project.data import Message, TextPlan


def generate_textplans(data: pd.DataFrame) -> List[TextPlan]:
    # Start with an empty list
    textplans: List[TextPlan] = list()

    # Append weather condition messages
    for cond in ['thunderstorms', 'snow', 'rain']:
        newplan = generate_forecast_condition_periods(data, cond)
        if newplan.messages:
            textplans.append(newplan)

    # Winds above 12mph are computed differently
    newplan = generate_wind_periods(data)
    if newplan.messages:
        textplans.append(newplan)

    # Sort text plans according to the start date of the first message
    textplans.sort(key=lambda x: x.messages[0].arguments['period_start_id'])

    # Generate the temperature range and put it first
    newplan = generate_temp_range(data)
    if newplan.messages:
        textplans.insert(0, newplan)

    # Return the list of text plans
    return textplans


# Generate textplan for temperature range
def generate_temp_range(data: pd.DataFrame) -> TextPlan:
    min_temp = min(data['temperature'])
    max_temp = max(data['temperature'])
    args = {'value': 'temperature', 'minimum': min_temp, 'maximum': max_temp}
    message = Message(relation='value-in-range', arguments=args)
    textplan = TextPlan(messages=[message])
    return textplan


# Generate textplan for forecast condition periods (e.g. 'rain', 'snow')
def generate_forecast_condition_periods(data: pd.DataFrame, condition: str) -> TextPlan:
    condition = condition.lower()

    # Keep track of whether the condition is active or not
    condition_active = False

    # Keep track of when the condition starts and ends
    condition_starts = []
    condition_ends = []

    # Iterate through rows in the dataset,
    # looking for the condition to appear in shortForecast
    for row in range(len(data)):
        if condition in data.loc[row]['shortForecast'].lower():
            if not condition_active:
                # Condition range starts here
                condition_active = True
                condition_starts.append(row)
        else:
            if condition_active:
                # Condition range ends one row above
                condition_active = False
                condition_ends.append(row-1)

    # If condition is still active at the end of the iteration,
    # close the open range at the last period
    if condition_active:
        condition_ends.append(len(data)-1)

    # Create empty textplan
    textplan = TextPlan(messages=[])

    # Iterate through condition periods, adding messages to the textplan
    for id_start, id_end in zip(condition_starts, condition_ends):
        period_start = data.loc[id_start]['name']
        period_end = data.loc[id_end]['name']
        args = {'condition': condition,
                'period_start_id': id_start, 'period_start': period_start,
                'period_end_id': id_end, 'period_end': period_end}
        message = Message(relation='condition-in-period', arguments=args)
        textplan.messages.append(message)

    # Return textplan
    return textplan


# Generate textplan for periods with wind over 12mph
def generate_wind_periods(data: pd.DataFrame) -> TextPlan:
    # This involves some wrangling of source data, so work from a copy
    data_copy = data.copy()

    # Replace windSpeed string with the numeric value of the max wind speed listed
    data_copy['windSpeed'] = [
        int(re.search(pattern=r'\d+(?= mph$)', string=row['windSpeed'])[0])
        for row in data.iloc
    ]

    # Replace shortForecast with 'winds above 12mph' if windSpeed exceeds 12
    data_copy['shortForecast'] = [
        'winds above 12mph' if wind > 12 else ''
        for wind in data_copy['windSpeed']
    ]

    # Call the general generating method on the wrangled data & return its result
    return generate_forecast_condition_periods(data_copy, 'winds above 12mph')
