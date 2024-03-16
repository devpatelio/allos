from flask import Flask, render_template, abort, url_for, json, jsonify
from flask_restful import Api, Resource, reqparse
from flask_api_handler import ApiHandler
from flask_cors import CORS
import pandas as pd

app = Flask(__name__)

class GraphDataset():
    def __init__ (self, path):
        self.path = path
        self.data = pd.read_json(path)
        self.nodes = self.data['nodes']
        self.edges = self.data['edges']

    def get_all_edges(self, id):
        self.node = self.nodes[id]
        self.node_edges = {'incoming': [], 'outgoing': []}
        for idx, edge in enumerate(self.edges):
            if edge['source'] == id:
                self.node_edges['outgoing'].append(edge['target'])
            elif edge['target'] == id:
                self.node_edges['incoming'].append(edge['source'])
        return {id: self.node_edges}
    
    def get_data(self):
        dic_data = self.data.to_dict()
        return dic_data
    
    #Clean Data rough outline
    def clean_data(self): 
         #Drop NA rows 
        self.data.dropna(inplace=True)
        #Drop duplicate rows 
        self.data.drop_duplicates(inplace = True)
        #Impute with mean for numerical columns
        numeric_columns = self.data.select_dtypes(include='number').columns
        self.data[numeric_columns] = self.data[numeric_columns].fillna(self.data[numeric_columns].mean())
        #Impute with mode for non-numerical columns
        non_numeric_columns = self.data.select_dtypes(include='object').columns
        self.data[non_numeric_columns] = self.data[non_numeric_columns].fillna(self.data[non_numeric_columns].mode().iloc[0])
        #Reset index after cleaning
        self.data.reset_index(drop=True, inplace=True)

graph_objects = {1: GraphDataset('server/data.json')}
print(graph_objects[1].get_data())

    
@app.route('/', methods=['GET'])
def index():
    data_fetch = graph_objects[1].get_data()
    return render_template('index.html', jsonfile=json.dumps(data_fetch))

if __name__ == "__main__":
    app.run(debug=True)
