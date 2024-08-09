from typing_extensions import TypeVarTuple
from fastapi import FastAPI, HTTPException
import fastapi
from pydantic import BaseModel
from typing import List, Optional

from python_on_whales import docker

from libs.Port import Port
import uuid
import os
import shutil
import uvicorn

app = FastAPI()

class Container(BaseModel):
    username: str

@app.post("/container")
def create_container(data: Container):
    container_name = data.username + ":" + str(uuid.uuid4())
    user_folder = data.username.replace('@', '_at_')
    folder_location = "/opt/albatross/" + user_folder + "/App"

    os.makedirs(folder_location, exist_ok=True)
    shutil.copytree("/opt/albatross/main-file", folder_location, dirs_exist_ok=True)
    
    port = str(Port().gen())
    port_asign = "0.0.0.0:" + port
    docker.run(
        'albabatros_shinyapp',
        name=container_name,
        publish=[(port_asign,9095)],
        detach=True,
        volumes=[(folder_location, "/srv/shiny-server")]
    )

    return_data = {"url":"http://202.124.198.83" + port}

    return return_data

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info")
