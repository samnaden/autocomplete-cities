# autocomplete-cities

### local development
This project uses poetry. On your system execute `pip3 install poetry==1.3.2`.  
Also, you'll need python >= 3.12.  
Then, from this directory, execute `poetry install`. This will create a virtual environment for you.  
Now run `poetry run uvicorn autocomplete_cities.app:app --host 0.0.0.0 --port 5000 --workers 4`.  This launches the API.  
You can now execute something like `curl 'localhost:5000/api/v1.0/suggestions?q=london'` and get a response back.  
Now you can make code changes locally and test how they work out. Tip: use PyCharm and run the file `./autocomplete_cities/app.py` in debug mode in order to debug your code.

### tests
Run `poetry shell` to enter the venv for this project, then run `pytest` from this directory.

### deployment
From this directory execute `docker build -t autocomplete-cities-0 .`. You can then push this image to your favorite registry (e.g. AWS ECR) and use it however you wish (e.g. AWS ECS).  
If you want to run the containerized application locally and interact with it...
- `docker run autocomplete-cities-0`
- Get the container ID via `docker container ls`
- `docker exec -it {container_id} bash`
- Now that you're in the image, you could do something like `curl localhost:5000/api/v1.0/suggestions?q=madison`

### scalability
There are two levers you can pull to make this more scalable. One would be to increase the number of uvicorn workers (see ./Dockerfile).  
Another would be to deploy this image to your favorite cloud provider and run it on a container service, which usually scale with load automatically.
