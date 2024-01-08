This repositiory is for the Computer Networks course.

The goal of this project is to design and implement a robust Peer-to-Peer Multi-User Chatting
Application using Python and sockets. The application aims to emulate features similar to popular
platforms like Clubhouse, but with a focus on text-based communication. The project will be divided
into four phases, each building on the previous one, to demonstrate proficiency in network
application protocol design, client-server and peer-to-peer architecture, and the proper use of TCP
and UDP protocols.

One of our main goals was to make this application with the users ease in mind. The user 
only needs to install a few libraries to run the application, all of which will be listed below. 
All you have to do is copy these commands into your terminal. 
 pip install colorama
 pip install simpleaudio
 pip install bcrypt
There are two ways to install MongoDB to be able to successfully use out chat app, both will 
be provided below (These steps are taking into consideration the users that do not know what 
MongoDB is. Users who have MongoDB can skip some steps if necessary)
i) Install MongoDB for Python
(1) Visit the official MongoDB website 
(https://www.mongodb.com/try/download/community) and download the MongoDB 
Community Server for your operating system.
(2) After installation, start the MongoDB server. The process may vary depending on your 
operating system:
(a) On Windows, you can start MongoDB by running “mongod.exe”.
(b) On macOS or Linux, you might use a command like “sudo service mongod start” or 
“mongod”.
(3) Open a terminal or command prompt and paste this command “pip install pymongo”
ii) Run MongoDB as a docker container
(1) Visit the official docker website (https://docs.docker.com/get-docker/) and choose the 
section that is for your operating system
(2) Pull MongoDB docker image using this command “docker pull mongo:latest” which will 
provide you with the latest image of MongoDB
(3) Run the MongoDB image on docker using this command “docker run -d --name 
mongodb -p 27017:27017 mongo”
(4) Verify that the container is running using this command “docker ps”
(5) Connect the MongoDB to the Docker container using this command “docker exec –it 
mongodb mongosh”
After successfully completing these steps you can finally run the chat app. Below are some 
very simple steps to run the chat app:
1. Run docker image/connect to MongoDB
2. Run server.py using the command “python Server.py”
3. The server.py will show you the registry IP address and the registry port number
4. Run Peer.py using the command “python “Peer.py”
5. The peer.py will request an input from you
6. Enter IP address that appeared after running server.py in the terminal that is running the 
peer.py file
After successfully following these simple steps you will now be shown the home screen and 
you can start using the application
