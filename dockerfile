#Build + Test React Front End

#Download Python from DockerHub and use it
FROM python:3.6

#Set the working directory in the Docker container
#WORKDIR /HealXPaperSearchApp


#Copy the API
COPY search_api/ /search_api/

#Copy the prod env file
COPY /docker_deployment/.prod_env .env


# #Copy the latest React Build
COPY search_app/build /search_app/build/

#Copy the start_script
COPY /docker_deployment/start_script.sh start_script.sh

# #Install API dependencies
RUN pip install -r /search_api/requirements.txt

# Setup required Flask environment variables + expose the 5000 port to host running docker container
ENV FLASK_ENV production

EXPOSE 5000

#Execute the start script
CMD ["bash","/start_script.sh"]
