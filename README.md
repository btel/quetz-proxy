# quetz-proxy

Caching proxy for quetz.

It implements the protocol described in the [Proposal 1](https://hackmd.io/kgifxnZ7SFupZkWjwsUxnw?view#Proposal-1-Lazy-proxy)

## Installing

```
pip install fastapi requests
```

## Usage

Follow the instructions in quetz [README](https://github.com/TheSnakePit/quetz/blob/master/README.md) to install and configure quetz. Run the server with the command (from quetz directory):

```
> quetz start test_quetz
```

Start the proxy (from the quetz-proxy directory):

```
export QUETZ_SERVER_URL=http://localhost:8000/channels
uvicorn main:app --port 8002 --reload
```

The proxy is now running. Now you can install packages from the proxy, lets try it in a new enviornment:

```
conda create -n quetz-proxy-test python=3.8
conda activate quetz-proxy-test
```

Then install the `xtensor` package using the proxy server as the channel:

```
conda install --strict-channel-priority xtensor -c http://localhost:8002/channels/channel0 -c conda-forge
```
