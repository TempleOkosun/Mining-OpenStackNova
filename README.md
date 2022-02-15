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
* [Python](https://www.python.org): Python programming language
* [PyGitHub Library](https://pygithub.readthedocs.io/en/latest/introduction.html): Python library for interacting with GitHub API v3
* [requests](https://docs.python-requests.org/en/latest): Python library for additional http requests to GitHub API
* [pandas library](https://pandas.pydata.org): Python data analysis library.
* [jupyter notebook](https://jupyter.org): For organizing analysis, visualization and report
* [json formatter & validator](https://jsonformatter.curiousconcept.com): for validating and exploring API responses
* [Postman](https://www.postman.com): for exploring GitHub API end points
* [notepad++](https://notepad-plus-plus.org): To save json outputs, and item count operations to validate data.

### Approach
In coming up with this solution, the first step was to research and explore GitHub to find out how I could get the data 
required. The 2 possible options were to: scrape or use the API. The GitHub API had very generous limits for
authenticated requests that would be sufficient for this project and the commits' endpoint would provide all the data.

The next step was to determine, how to interact with the API. The GitHub API can be well interacted with via octokit a
javascript based library but due to previous experience in data analysis with python and pandas, my preference was to 
utilize what the python ecosystem provides. While I could use requests library for all the interactions, I found 
PyGitHub had a very friendly interface to interact with GitHub API. After using PyGitHub to connect with the API and 
retrieve all commits, I discovered access to file attributes for each commit were abstracted away and eventually had to 
use requests library to retrieve individual commit.

### Challenges
The two key areas of challenge were:
* Extracting the data points to form a row: The commit data is a semi-structured json with files as a list of file 
objects. Initially tried using nested for loops to get a flat row but later discovered a more efficient method provided 
in pandas for json normalization.

* Storing the collected data temporarily as a json file to be read in later for analysis. Pandas method to read json
file did not provide sufficient error details to help understand why the json file was not being decoded properly.

Also, PyGitHub documentation was not so robust.

### How to use the tool
Data collection script:
1. clone the project repo
2. cd into the project root directory
3. you need to create a .env file at the project root directory and provide (ACCESS_TOKEN and GITHUB_USERNAME) <br>
   ACCESS_TOKEN='token' <br>
   GITHUB_USERNAME='user' <br>
   Alternatively, you can also specify it directly in the main.py file and ignore the use of .env file
4. You can change the target repo or time also in the main.py
5. Run the main.py file. 
       ```
       python main.py 
       ```
   when it is done a data.json file is created. <br>


![Script in action](images/script_in_action.gif)