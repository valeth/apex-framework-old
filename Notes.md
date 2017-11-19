## Setup

```python
# Discord bot with pymongo database backend

import pymongo
from apex import Apex
from apex.engine import DiscordEngine
from apex.database import MongoDatabase

client = Apex()
database = MongoDatabase(auth=False)
engine = DiscordEngine("my_secret_token").with_database(database)

client.add_engine(engine)
client.start()
``` 

## Modules Layout

```
modules +
        |- shared/{module_name}     # shared between engines
        |- {engine}/{module_name}   # engine specific
```

## Module Layout

```
{module_name} +
              |- manifest.yml   # description, etc.
              |- init.py        # entrypoint
              |- lib/           # additional scripts
              |- res/           # local resources
              |- components/    # event handlers
```