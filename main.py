from fastapi import FastAPI
import os
import json
import requests
from fastapi.responses import FileResponse

app = FastAPI()

deploy_dir = "test_quetz"
SERVER_URL = os.environ.get("QUETZ_SERVER_URL", " https://conda.anaconda.org")

#curl https://conda.anaconda.org/conda-forge/linux-64/current_repodata.json | jq

def get_local_repodata(channel_name, arch, filename):
    with open(
        os.path.join(deploy_dir, "channels", channel_name, arch, filename), "r"
    ) as fid:
        return json.load(fid)

def get_remote_repodata(channel_name, arch, filename):
    url = "{server_url}/{channel_name}/{arch}/{filename}".format(
        server_url=SERVER_URL,
        channel_name=channel_name,
        arch=arch,
        filename=filename)
    response = requests.get(url)
    return response.json()
    
def get_remote_package(channel_name, arch, filename):
    url = "{server_url}/{channel_name}/{arch}/{filename}".format(
        server_url=SERVER_URL,
        channel_name=channel_name,
        arch=arch,
        filename=filename,
        stream=True)
    response = requests.get(url)
    return response, response.headers.get("content-type")

@app.get("/channels/{channel_name}/{arch}/repodata.json")
def repodata(channel_name: str, arch: str):
    return get_remote_repodata(channel_name, arch, "repodata.json")


@app.get("/channels/{channel_name}/{arch}/current_repodata.json")
def current_repodata(channel_name: str, arch: str):
    return get_remote_repodata(channel_name, arch, "current_repodata.json")

@app.get("/channels/{channel_name}/{arch}/{pkgname}")
def pkgname(channel_name: str, arch: str, pkgname: str):
    package_dir = os.path.join(deploy_dir, "channels", channel_name, arch)
    path = os.path.join(package_dir, pkgname)
    if not os.path.isfile(path):
        os.makedirs(package_dir, exist_ok=True)
        print("Downloading file...")
        binary_data, content_type = get_remote_package(channel_name, arch, pkgname)
        with open(path, 'wb') as fid:
            for chunk in binary_data.iter_content(chunk_size=100000):
                fid.write(chunk)
    else:
        print("Getting file from cache")
    
    return FileResponse(path)
