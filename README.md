# This is the implemetation of paper "Generating Long-form Story Using Dynamic Hierarchical Outlining with Memory-Enhancement"
## Prepare environment
After clone the code, state in the home directory and run the following instruction in the terminal
```
conda create -n dome python=3.10
conda activate dome
pip install -r requirements.txt

```

## Prepare directories
After entering the main directory of our project,make directory for storing story and information about knowledge graph.
```
makdir data
```

Do not forget to fill your own path of data and log in DHO.py and MEM.py:

```
your path="your path for data"

```


### Ready for knowledge graph database
We apply neo4j to store and access knowledge graph.You can depoly neo4j(version 4).For quick start,you can create a Blank Sandbox on [https://sandbox.neo4j.com/](https://sandbox.neo4j.com/), click "connect via drivers", find your url and user password. Then replace the following parts in MEM.py:
```
uri = "Your_url"
username = "Your_user"     
password = "Your_password"
```

### Ready for LLM api and its key
Our work need the inference ability of LLM.Don't forget to replace your api_key in MEM.py and replace the following parts in MEM.py and DHO.py:
```
client = OpenAI(
        base_url='your url',
        api_key='your key',
    )
```
## Input data preparation
We follow the setting of DOC and RE3, you can refer to their repository on on [https://github.com/yangkevin2/doc-story-generation](https://github.com/yangkevin2/doc-story-generation) to get the input data.


## Generation process
To generate story with input information(setting, character introduction and plot requirements), you need to firstly run 1storyline.py to generate the rough outline for every story.
```
python 1storyline.py
```
Before you run the 1storyline.py you need to replace the input path with your own path to store input data in csv type.

Then you can run the DOME.py to get stories with your generated rough outline.
Before you run this file, please replace the path of the rough outline and the input data.
```
python DOME.py
```
