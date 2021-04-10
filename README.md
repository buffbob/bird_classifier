# bird_classifier
<h2>Flask web app for human image classification</h2>
<h5>image classification tasks require lots of labeled data. This app allows administrator to scrap 
images from the web and then helps human users classify them. The app has been tailored for bird images 
but can be altered for other needs.</h5>

<h4> to run locally using flask server and a sqlite3 database</h4>
<h5>change code on line 18 of image_utils.py to be your flicker api key/value pair</h5>
<h5>add a virtual environment and install dependencies</h5>
<ol>
  <li>python3 -m venv venv</li>
  <li>source venv/bin/activate</li>
  <li>pip install -r requirements.txt</li>
  <li>export FLASK_APP=run.py</li>
  <li>flask run</li>
</ol>

<h4>Available on Docker</h4>
<h5>Pull::   sudo docker pull paddypup/bird_1.0</h5>
<h5>Run::  sudo docker run -it -p 8811:5000 paddypup/bird_1.0 </h5>

after running, on your browser visit-  localhost:8811

<h5>Visit the running site- <a href="http://birdimageclassifier.us-east-2.elasticbeanstalk.com/"> here</a></h5>
<hr>

