![Python 3.5](https://img.shields.io/badge/Python-3.5-blue.svg)
![License](https://img.shields.io/badge/License-BSD%202--Clause-orange.svg)

![logo](https://s3.eu-central-1.amazonaws.com/camo-bucket/logo_small.svg)

# Why SuperSight ?

A few months ago I set up a data pipeline within the AWS ecosystem. The final step was to refresh dashboards regularly on QuickSight. Coming from Matplotlib and its unlimited power it was quite frustrating not to be able to design the very plot I had in mind. Notebooks are great for low level work but perhaps not for showing off results to top managers. SuperSight is designed to fill the gap between notebooks and commercial business intelligence tools.

# Install

`pip install supersight`  
`pip install https://s3.eu-central-1.amazonaws.com/releases-55/supersight/dist/supersight-latest.tar.gz`

# Quickstart

Check the live demo [here](http://supersight-demo.s3-website.eu-central-1.amazonaws.com/index.html).

Check the notebook used to generate this demo [here](https://nbviewer.jupyter.org/github/CamilleMo/SuperSight/blob/master/SuperSight_Intro.ipynb)

# Customizable

Everything you see in the demo can easily be overridden to let you build a white-labeled website.  
You can also build your own template starting from the plain vanilla Bootstrap 4 included by default.  
  
MathJax.js and Gutenberg CSS are included by default via CDN. You can also remove these libraries and add libraries you may need using a custom template.

# Changelog

2017-04-22 : A Documentation is now available.  
2017-04-22 : Plots open in modal on click.