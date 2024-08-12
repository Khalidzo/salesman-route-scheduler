from main import app
from fastapi import File, UploadFile
from fastapi.responses import JSONResponse
import pandas as pd
import shutil
from services.visting_plan import create_visiting_table, filter_visting_table
from services.path_builder import (
    initialize_kmeans,
    assign_nodes_to_clusters,
    create_distance_matrix,
    optimize_routes,
)
from core.config import validate_key


@app.post("/get_route_plan")
async def get_route_plan(
    file: UploadFile = File(...), key: str = None, n_clusters: int = 0
):
    try:
        # Validate key
        if not validate_key(key) or type(key) != str:
            return JSONResponse(
                status_code=401, content={"message": "Unauthorized: Invalid key value."}
            )

        # Validate number of clusters
        if type(n_clusters) != int or n_clusters < 2 or n_clusters > 24:
            return JSONResponse(
                status_code=400,
                content={"message": "Bad Request: Invalid number of clusters."},
            )

        # Validate file
        if (
            file.content_type
            != "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        ):
            return JSONResponse(
                status_code=400, content={"message": "Bad Request: Invalid file type."}
            )

        with open(f"{file.filename}", "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

            # Create a dataframe
            df = pd.read_excel(f"{file.filename}")

            # Validate columns
            if "Location" not in df.columns:
                return JSONResponse(
                    status_code=400,
                    content={"message": "Bad Request: Missing 'Location' column."},
                )

            # Filter the visiting table
            visiting_table = filter_visting_table(df)

            # Create the visiting table
            visiting_table = create_visiting_table(visiting_table)

            # Create KMeans
            kmeans, cluster_labels = initialize_kmeans(visiting_table, n_clusters)

            # Assign nodes to clusters
            distance_matrix = create_distance_matrix(
                visiting_table, kmeans.cluster_centers_
            )
            clusters = assign_nodes_to_clusters(
                visiting_table.shape[0], n_clusters, distance_matrix
            )

            # Optimize routes within the clusters
            optimized_clusters = optimize_routes(visiting_table, clusters)

            print(optimized_clusters)

            return {"message": "File uploaded successfully!"}
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": str(e)})
