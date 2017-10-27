#Change the NAME variable with the name of your script
NAME=coralreefs
docker build -t $NAME --build-arg NAME=$NAME .
docker run -v $(pwd)/data:/opt/$NAME/data --env-file .env --rm $NAME