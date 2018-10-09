# Maap

This is a messy application.
We wrote it as an example for a weird application that we put in a container and deploy to the cloud using gcp.
It reads data and processes it.
Most of the code doesn't even exist before the compilation.
First the .proto file is compiled into an .cc and a .h file.
Than everything is compiled into object files and finally into a single binary.
To make things even more difficult we use protobuf from a conda environment which has to be created beforehand.
And the binary only works when linked against the libprotobuf.so, which we do using an environment variable.

The built docker image can be obtained like this:

```
$ docker pull nicolasholland/maap
```

More info on our [blog](https://somefunwithdata.blogspot.com/)
