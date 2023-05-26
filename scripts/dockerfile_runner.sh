#!/bin/bash

cd outputs
docker build -t testing-ubuntu-image .
docker run -it testing-ubuntu-image 