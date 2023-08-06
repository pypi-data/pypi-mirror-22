OSS CMD
-------
simple command line tool for oss


## Commands
- [x] ocp `scp-like copy tool`


### Options
```
--access_key [OSS_ACCESS_KEY]
--secret_key [OSS_SECRET_KEY]
--endpoint   [OSS_ENDPOINT]
```

### OCP
#### Extra Options
```
-r/--recursive   upload folders too
-v/--verbose     verbose output
```

#### Sample
```
ocp -rv src bucket:/remote-path
```
