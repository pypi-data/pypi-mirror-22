EGCG-Core
===========
[![PyPI](https://img.shields.io/pypi/v/EGCG-Core.svg)](https://pypi.python.org/pypi/EGCG-Core)
[![PyPI](https://img.shields.io/pypi/pyversions/EGCG-Core.svg)](https://pypi.python.org/pypi/EGCG-Core)
[![travis](https://img.shields.io/travis/EdinburghGenomics/EGCG-Core/master.svg)](https://travis-ci.org/EdinburghGenomics/EGCG-Core)
[![landscape](https://landscape.io/github/EdinburghGenomics/EGCG-Core/master/landscape.svg)](https://landscape.io/github/EdinburghGenomics/EGCG-Core)
[![GitHub issues](https://img.shields.io/github/issues/EdinburghGenomics/EGCG-Core.svg)](https://github.com/EdinburghGenomics/EGCG-Core/issues)  
This is a core module for Edinburgh Genomics' clinical processing. It contains common modules for use across
EGCG's various projects, including logging, configuration, exceptions and random utility functions. There are
also modules for interfacing with EGCG\'s reporting app and Clarity LIMS instance.

Modules
----------

### executor
This module allows the execution of Bash commands from Python. Executor classes include
a non-threaded Executor, a threaded StreamExecutor that streams its stdout/stderr as it runs, and an
ArrayExecutor that combines multiple Executors into a job array. There is also ClusterExecutor, which writes
and submits a Bash script for a resource manager. All Executor classes implement a `start` method and a `join`
method, which returns an integer exit status.

- execute - Takes some string commands, decides whether or not to use cluster execution depending on the
  config, and calls either `local_execute` or `cluster_execute`.
- local_execute - Takes one or more string commands and calls Executor or StreamExecutor, depending on
  arguments. If multiple commands are given, Executor/StreamExecutors will be called via ArrayExecutor.
- cluster_execute - Takes one or more string commands and calls the appropriate ClusterExecutor depending on
  the config.
- Executor - Executes a Bash command via `subprocess.Popen`.
- StreamExecutor - Executes via `Popen` and `threading.Thread`, allowing it to output the job's stdout in real
  time. Can use `self.run` or `self.start` followed by `self.join`.
- ArrayExecutor - Takes a list of Bash commands and generates an Executor object for each. In `self.run`, it
  iterates over these and calls `start` and `join` for each one.
- ClusterExecutor - Takes one or more Bash commands. Upon creation, it calls creates a script writer and
  writes a Bash script. `prelim_cmds` may be specified to, e.g, export Java paths prior to commencing the
  job array. `self.start` and `self.join` executes a qsub/sbatch/etc. Bash command on the script.

#### script_writers
This `executor` submodule containing classes that can write scripts executable by the shell or by a resource manager.
Each ScriptWriter writes a header giving arguments to the resource manager, including `walltime`, `cpus`,
`mem`, job name, stdout file and queue id, and also allows the writing of job arrays specific to the manager.

- ScriptWriter - Base class that can open a file for writing, write commands to it and save.
- PBSWriter
- SlurmWriter


### util
Contains convenience functions:
- find_files - Convenience function combining `glob.glob` and `os.path.join`. If any files are found for the
  given pattern, returns them.
- find_file - Returns the first result from find_files.
- str_join - Convenience function for calling str.join using `*args`.


### app_logging
Contains AppLogger, which can be subclassed to implement logging methods within a class, and
LoggingConfiguration, which contains all relevant loggers, handlers and formatters and provides `get_logger`,
which generates a logger registered with all active handlers.

- LoggingConfiguration - Contains handlers, loggers, and methods for adding/configuring them.
  - get_logger - Adds a logger with a given name and adds all active handlers to it.
  - add_handler - Adds a created handler and adds it to all active loggers.
  - set_log_level - Sets the log level for all active loggers and handlers.
  - set_formatter - Sets the format for all active handlers.
  - configure_handlers_from_config - Adds handlers using a dict config (example below). Uses
    `BaseConfigurator.convert` to allow the use of, e.g, `ext://sys.stdout`. Passes all args from the dict to
    the relevant object's constructor. Currently allows `StreamHandler`, `FileHandler` and
    `TimedRotatingFileHandler`.

```
log_cfg.configure_handlers_from_config(
    {
        'stream_handlers': [
            {'stream': 'ext://sys.stdout', 'level': 'DEBUG'},
            {'stream': 'ext://sys.stderr', 'level': 'ERROR'}
        ],
        'file_handlers': [{'filename': 'test.log'}],
        'timed_rotating_file_handlers': [{'filename': 'test2.log', 'when': 'midnight'}]
    }
)
```

- AppLogger - Mixin class containing a logger object created through LoggingConfiguration by @property, and
  named using `self.__class__.__name__`.


### config
Contains config classes able to scan possible file locations for Yaml config files, then uses `yaml` to read
it into a Python dict contained in `self.content`.

#### Configuration
Config class. Implements `__getitem__` for dict-style square bracket querying; `__contains__` to allow
the use of, e.g, `if x in cfg`; `get` as in `dict.get`; and `query` for drilling down into the dict, returning
`None` if nothing is found.

Uses `_find_config_file` to locate a file to read. Is constructed with a `cfg_search_path`, allowing it to
search for config files in multiple possible locations, e.g. in the user's home or in a path specified in an
environment variable. The first config file found gets used.


It can also read config files containing multiple environments. For example:

```
default:
    this: 1
    that: 2
    other: 3

testing:
    this: 1337

production:
    this: 1338
    that: 4
```
Upon construction, or loading of a new config file, the class can read an environment variable telling it which 
environment to use. It merges the `default` environment if it exists and the specified environment if it exists
For example, a Configuration set to 'testing' will have `{'this': 1337, 'that': 2, 'other': 3}` in `self.content` 
and one set to 'production' will have `{'this': 1338, 'that': 4, 'other': 3}`.

#### EnvConfiguration
This class is an alias for Configuration for backward compatibility

### constants
Contains constants used in EGCG's reporting app. Includes dataset statuses and database keys/column names.


### exceptions
Custom exceptions raised by the pipeline: EGCGError, LimsCommunicationError and ConfigError.


### rest_communication
Contains functions for interacting with the external Rest API. Uses the `requests` module.

- get_documents
- get_document
- post_entry
- put_entry
- patch_entry
- patch_entries - Iterates through payloads and patches each one. Only runs get_documents once.
- post_or_patch - Tries to post an entry and if unsuccessful, prepares the payload and patches instead.
