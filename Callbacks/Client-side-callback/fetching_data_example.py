# https://dash.plotly.com/clientside-callbacks#fetching-data-example
from dash import Dash, dcc, html, Input, Output, dash_table
import os

app = Dash(__name__)

file_json = os.path.join("C:",os.sep,"Users","werne","Documents","iris_data.json")
file_json = "iris_data.json"
print (file_json)

app.layout = html.Div(
    [
        dcc.Dropdown(
            options=[
                {
                    "label": "Car-sharing data",
                    "value": "https://raw.githubusercontent.com/plotly/datasets/master/carshare_data.json",
                },
                {
                    "label": "Iris data",
                    "value": "https://raw.githubusercontent.com/plotly/datasets/master/iris_data.json",
                },
                {
                    "label": "Iris local",
                    "value": file_json,
                },
            ],
            value="https://raw.githubusercontent.com/plotly/datasets/master/iris_data.json",
            id="data-select",
        ),
        html.Br(),
        html.Div(id="div_output", children='Huhu'),
        html.Br(),
        dash_table.DataTable(id="my-table-promises", page_size=10),
    ]
)

app.clientside_callback(
    """
    async function(value) {
    const response = await fetch(value);
    const data = await response.json();
    return data;
    }
    """,
    Output("my-table-promises", "data"),
    Input("data-select", "value"),
)

app.clientside_callback(
    """
    async function(value) {
    var personObject = { name: "Peter", age: 18, married: false };
    
    // Convert the person object into JSON string and save it into storage
    localStorage.setItem("personObject", JSON.stringify(personObject));
        
    // Retrieve the JSON string
    var jsonString = localStorage.getItem("personObject");
        
    // Parse the JSON string back to JS object
    var retrievedObject = JSON.parse(jsonString);
    console.log(retrievedObject);
        
    // Accessing individual values
    console.log(retrievedObject.name); // Prints: Peter
    console.log(retrievedObject.age); // Prints: 18
    console.log(retrievedObject.married); // Prints: false
   
    return 'yep '+jsonString;
    }
    """,
    Output("div_output", "children"),
    Input("data-select", "value"),
)

if __name__ == "__main__":
    app.run_server(debug=True)