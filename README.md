ENV ORM
---------------

Build status: [![CircleCI](https://circleci.com/gh/winkidney/envorm.svg?style=svg)](https://circleci.com/gh/winkidney/envorm)

**Environment-variables as config made easy.** 

An utility library that helps you 
to use environment-variables from an orm-like interface.

It helps a lot especially you prefers to use docker as your app runner. 

## Feature

+ ORM-like interface(or wtforms-like)
+ validation included
+ Auto type-conversion
+ Doc/Example config for ORM object

## ChangeLog

+ Wed May  2 01:56:54 PDT 2018 - Add doc/example config env output 


## Install

```
pip install envorm 
```

or 

```
git clone https://github.com/winkidney/envorm.git
cd envorm
python setup.py install
```

## Usage

```python
import envorm as orm

class Model(orm.EnvModel):
    example = orm.StringField(
        "IP_ADDR",
        default="0.0.0.0",
        required=False,
    )

# initialize
settings = Model()

# validation
settings.is_valid()

# Use the value
settings.example.value

# update if env changed
settings.update()

# list settings field in command line
# if you want to provide an interface to show
# what config is needed and show its default value
settings.list_names()

# Print config doc (or just copy it as example config file)
print(settings.doc())

```
