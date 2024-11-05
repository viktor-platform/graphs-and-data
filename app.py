from pathlib import Path

import pandas as pd
import plotly.graph_objects as go

import viktor as vkt


def extract_data():
    parent_folder = Path(__file__).parent
    file_path = parent_folder / "car-sales.csv"
    data = pd.read_csv(file_path, sep=';')
    return data


class Parametrization(vkt.ViktorParametrization):
    introduction = vkt.Text(
        """
# 📊 Data Analysis App!

In this app you can summarise data and visualise it in a PlotlyView.  
The app will summarise some data in the DataView and allow the user to choose a column to analyse to create the Plotly chart.

        """
    )
    # Add some input field for the user

    main_column = vkt.OptionField('Choose main property', options=extract_data().columns.values.tolist())
    count_column = vkt.OptionField('Choose property to analyse', options=extract_data().columns.values.tolist())


class Controller(vkt.ViktorController):
    label = 'My Data Analysis App'
    parametrization = Parametrization

    @vkt.PlotlyAndDataView('Bar chart', duration_guess=1)
    def generate_plotly_view(self, params, **kwargs):
        # Extract and edit data to make it easy to plot
        data = extract_data()
        edited_data = data.groupby(params.main_column)[params.count_column].value_counts().unstack().fillna(0)

        # Make the bar chart
        fig = go.Figure()
        for column in edited_data.columns:
            fig.add_trace(go.Bar(x=edited_data.index, y=edited_data[column], name=column))

        # Edit the bar chart
        fig.update_layout(barmode='stack', xaxis_title=params.main_column, yaxis_title='Amount Sold')

        # Create a summary with the data
        summary = vkt.DataGroup(
            vkt.DataItem("Total Sold", len(data)),
            vkt.DataItem("Most Occurring", edited_data.sum().idxmax()),
            vkt.DataItem("Least Occurring", edited_data.sum().idxmin()),
        )

        return vkt.PlotlyAndDataResult(fig.to_json(), summary)
