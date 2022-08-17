# Live Demo: Get forecasts for US cities

from requests import HTTPError
from project.data import get_forecast_data_at, get_emergency_data, test_coordinates
from project.textplanner import generate_textplans
from project.sentenceplanner import generate_sentenceplans
from project.linguisticrealiser import generate_sentences


def run_pipeline():
    # Iterate through names of locations
    locations = test_coordinates.keys()
    for location in locations:

        # Get the coordinates for this location
        lat, lon = test_coordinates[location]

        # Execute each method in the NLG pipeline
        try:
            # Get data from API
            fc_data = get_forecast_data_at(lat, lon)
            # fc_data = get_emergency_data()  # Use this if the NWS API is down

            # Data -> Text Planner -> Sentence Planner -> Linguistic Realiser -> Output
            fc_textplans = generate_textplans(fc_data)
            fc_sentenceplans = generate_sentenceplans(fc_textplans)
            fc = generate_sentences(fc_sentenceplans)

        except HTTPError as e:
            # Handle errors during API access
            fc = f'Data Not Available\n{str(e)}'

        # Print the pipeline output
        print(f'Forecast for {location}:\n{fc}\n')


if __name__ == '__main__':
    run_pipeline()
