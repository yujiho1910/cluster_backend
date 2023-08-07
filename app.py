from flask import Flask, request
from flask_cors import CORS
from flask_restx import Namespace, Api, Resource
import pandas as pd

from sklearn.cluster import KMeans

app = Flask(__name__)

CORS(app)

calc_ns = Namespace("cluster", description="To Cluster coordinates")


@calc_ns.route("/cluster")
class Cluster(Resource):
    def get(self):
        return "HI", 200

    def post(self):
        file = request.files.get("file", None)
        k = int(request.form.get("clusterNo", None))
        if file == None:
            return "No file found", 400
        # process csv into a dataframe
        df = pd.read_csv(file)

        k_means = KMeans(n_clusters=k, n_init="auto", max_iter=10000)
        k_means.fit(df[["Latitude", "Longitude"]])
        df["cluster"] = k_means.labels_

        to_return = {}
        values = {}
        for _, row in df.iterrows():
            values[row["Name"]] = [row["Latitude"], row["Longitude"], row["cluster"]]
        to_return["values"] = values
        to_return["centers"] = k_means.cluster_centers_.tolist()
        return to_return, 200


api = Api(app, doc="/docs")
api.add_namespace(calc_ns)

if __name__ == "__main__":
    app.run(debug=True)
