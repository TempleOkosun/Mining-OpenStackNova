# Mining Software Repositories for insights - OpenStackNova

### Problem
What can we learn from commits and file changes in software repositories.

### Project Description
The goal of this tool and analysis is to help in capturing insights from the commits on a project repo. 
This tool has been designed to be very reusable. The same analysis can be carried out on different repos
provided there exists commits present for the supplied time duration. 

### Design
There are two aspects of the system: 
* A data collection script tool: responsible for automated collection of needed data. The inputs to be provided for the 
script are: GitHub access_token, GitHub username, Repo name and time duration in months. The output from the script is a
data.json file containing a list of contents of each commit.
* A jupyter notebook: for further data manipulation, analysis, visualization, and report. The data.json file outputted 
from running the script will be loaded into the notebook for analysis.

  
### Core tools, libraries and resources used:
* [PyGitHub Library](https://pygithub.readthedocs.io/en/latest/introduction.html): for interacting with GitHub API v3
* [requests](https://docs.python-requests.org/en/latest): for additional http requests to GitHub API
* [json formatter & validator](https://jsonformatter.curiousconcept.com): for validating and exploring API responses
* [Postman](https://www.postman.com): for exploring GitHub API end points
* [notepad++](https://notepad-plus-plus.org): To save json outputs, and item count operations to validate data.

