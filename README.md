# Bird Image Scrapper and Classifier
<h5>Image classification tasks require lots of labeled data. This app allows administrator to scrap 
images from the web and then helps users classify them. The app has been tailored for bird images 
but can be altered for other needs. This app is currently running at <a href="http:birdimageclassifier.us-east-2.elasticbeanstalk.com/">BirdApp</a>.</h5>

<h3>The classification page</h3>
<img src="admin.png">

<hr>
<h3>Adminstration Page (ie The Flicker Scrapper)
<img src="classifing.png">
     
<h4>To run locally using a flask development server and a sqlite3 database</h4>
<ol>
  <li>clone this repo and enter its directory</li>
  <li><span>create and activate a new environment---</span> python3 -m venv venv</li>
  <li><span>activate environment---</span> source venv/bin/activate</li>
  <li><span>add dependencies---</span> pip install -r requirements.txt</li>
  <li><span>create FLASK_APP variable---</span>export FLASK_APP=run.py</li>
  <li>change code on line 115 of image_utils.py to be your flicker api key/value pair</li>
  <li>run the app--- flask run</li>
  <li>to access admin privileges sign-in with admin credentials found on line 11 in init_db.py</li>
</ol>
     

<h4>Available on Docker</h4>
<h5>Pull::   sudo docker pull paddypup/bird_1.0</h5>
<h5>Run::  sudo docker run -it -p 8811:5000 paddypup/bird_1.0 </h5>

after running, on your browser visit-  localhost:8811

<h5>Visit the running site- <a href="http:birdimageclassifier.us-east-2.elasticbeanstalk.com/"> here</a></h5>
<h5>contact me for administration privileges on this site!</h5>
