ssh 2xA100 -L 5000:localhost:5000 -N -f

curl localhost:5000/check