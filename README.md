# This is the implemetation of paper "Generating Long-form Story Using Dynamic Hierarchical Outlining with Memory-Enhancement"
## Prepare directories
After entering the main directory of our project,make directory for storing story and information about knowledge graph.
```
makdir data
```
 
And then, make directory for storying log to record the generation process.
```
makdir log

```
Do not forget to fill your own path of data and log in DHO.py and MEM.py:

```
your path="your path for data"
your path="your path for log"

```

## Prepare for MEM module
### Ready for knowledge graph database
We apply neo4j to store and access knowledge graph.You can depoly neo4j(version 4).For quick start,you can create a Blank Sandbox on [https://sandbox.neo4j.com/](https://sandbox.neo4j.com/), click "connect via drivers", find your url and user password. Then replace the following parts in MEM.py:
```
uri = "Your_url"
username = "Your_user"     
password = "Your_password"
```

### Ready for LLM api and its key
Our work need the inference ability of LLM.Don't forget to replace your api_key in MEM.py and replace the following parts in MEM.py:
```
client = OpenAI(
        base_url='your url',
        api_key='your key',
    )
```

### Ready for data path
Don't forget to replace the data path(storing the quadruples  of story) in MEM.py and replace the following parts in MEM.py:
```
path="your path to store quadruples"
```

## Prepare for DHO module
make a new directory data to store your story and other intermidiate 



## Generation process
To generate story with input information(setting, character introduction and plot requirements), you need to firstly run 1storyline.py to generate the rough outline for every story.
```
python 1storyline.py
```
