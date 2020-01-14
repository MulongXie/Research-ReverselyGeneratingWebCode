# Researech-ReverselyGeneratingWebCode-Selenium
Attempt to generate layout code (HTML/CSS) from given web page screenshot [-ING]

<h2><b>First Stage</b></h2>
<br>
<h3>Preprocessing:</h3>
  Gather data and building the training data set <br>
  - Crawl and collect webpage + Info <br>
  - Label component on the web page w.r.t the Info gathered <br>
  - Clip the components for classification <br>
<br>

<h3>Training (Neural Network):</h3>
  Build model to recognize the tag class <br>
  - Decide and build an appropriate model <br>
  - Fine tune <br>
<br>

<h3>Transform (Image Processing):</h3>
    Transform the input component images into HTML code <br>
    - Calculate the shape and size of components <br>
    - Calculate the color theme of components <br>
    - Classify the tag of components <br>
<br>
 
