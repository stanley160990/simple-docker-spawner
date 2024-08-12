from typing_extensions import TypeVarTuple
from fastapi import FastAPI, HTTPException

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

class Container_update(BaseModel):
    container_name: Optional[str] = None
    state: str
    lst_container: Optional[List[str]] = None

@app.post("/container")
def create_container(data: Container):
    
    user_folder = data.username.replace('@', '_at_')
    container_name = "albatross_" + user_folder + "_" + str(uuid.uuid4())
    folder_location = "/raid/albatross/" + user_folder + "/App"

    os.makedirs(folder_location, exist_ok=True)
    shutil.copytree("/raid/albatross/main-file", folder_location, dirs_exist_ok=True)
    
    port = str(Port().gen())
    port_asign = "0.0.0.0:" + port
    docker.run(
        'albabatros_shinyapp',
        name=container_name,
        publish=[(port_asign,9095)],
        detach=True,
        volumes=[(folder_location, "/srv/shiny-server")]
    )

    return_data = {"url":"hpc-a100-mf.gunadarma.ac.id:" + port, "container_name": container_name, "error": False}

    return return_data

@app.put("/container")
def update_container(data: Container_update):
    if data.state == "shutdown":
        docker.container.stop(data.container_name, time=None)
    elif data.state == "shutdown-all":
        docker.container.stop(data.lst_container)
    elif data.state == "restart":
        docker.container.restart(data.container_name, time=None)
    elif data.state == "restart-all":
        docker.container.restart(data.lst_container)
    elif data.state == "remove":
        docker.container.stop(data.container_name)
        docker.container.remove(data.container_name)
    elif data.state == "remove-all":
        docker.container.remove(data.lst_container)
    
    return_data = {"message": "Container berhasil di" + data.state}

    return return_data

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
