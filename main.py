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
import uuid
import os
import subprocess
# Master Config

master_folder = "/home/albatross/simple-docker-spawner"
master_url = "https://dgx-a100-mf.gunadarma.ac.id/"

app = FastAPI()

class Container(BaseModel):
    username: str

class Container_update(BaseModel):
    container_name: Optional[str] = None
    state: str
    lst_container: Optional[List[str]] = None

def generate_url(docker_url, username):
    random_path = str(uuid.uuid4())
    template_file = "template/nginx-config-template"
    site_enable = "/etc/nginx/site-enabled"

    replacements= {
        'GEN_PATH' : random_path,
        'DOCKER_URL': docker_url
    }
    # Open the file, read its contents, replace the strings, and save the file
    with open(template_file, 'r') as file:
        content = file.read()

    # Replace each old string with its corresponding new string
    for old_string, new_string in replacements.items():
        content = content.replace(old_string, new_string)

    # Write the updated content back to the file
    target_path = master_folder + "/site-available/" + username
    nginx_path = site_enable + "/" + username
    with open(target_path, 'w') as file:
        file.write(content)

    os.symlink(target_path, nginx_path)

    link = master_url + random_path

    return link

def restart_nginx():
    sudo_password = 'merdeka100persen'
    command = f'echo {sudo_password} | sudo -S nginx -s reload'
    subprocess.run(command, shell=True, check=True, text=True)

    return True

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
    
    docker_url = 'http://127.0.0.1:' + port + "/"
    link = generate_url(docker_url, user_folder)
    restart_nginx()
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
