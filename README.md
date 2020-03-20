# bird_classifier
<h2>Flask web app for human image classification</h2>
<h5>image classification tasks require lots of labeled data. This app scraps images from the web and then helps humans classify them. The app has been tailored for bird images but can be altered for other images.</h5>

<h4> to run locally using flask server </h4>
<h5>change code on line 18 of image_utils.py to be a flicker api (user:key value) pair</h5>
<p>add a virtual environment and install dependencies and ...</p>
<ol>
  <li>python3 -m venv venv</li>
  <li>source venv/bin/activate</li>
  <li>pip install -r requirements.txt</li>
  <li>export FLASK_APP=run.py</li>
  <li>flask run</li>
</ol>

<h1>Available on Docker</h1>
<h4>Pull::   sudo docker pull paddypup/bird_1.0</h4>
<h4>Run::  sudo docker run -it -p 8811:5000 paddypup/bird_1.0 </h4>

after running, on your browser visit-  localhost:8811



<h5>Visit running site- <a href="http://birdimageclassifier.us-east-2.elasticbeanstalk.com/"> here</a></h5>
<hr>

