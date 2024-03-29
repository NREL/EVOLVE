## :key: Create a Login

After you open a browser window and type `http://localhost:5001` in the adress bar, you will be directed to the Evolve Login Page. Select the <mark style="background-color: #FFFFFF"><span style="color:blue"><u>Sign up as new user</u></span></mark> link. Fill out a username, passwork, and email address. Once your account is created, the user can login and will be directed to the EVOLVE home page.


![](images/login.JPG)

## :house: EVOLVE Home Page
The homepage has several main features, explained in detail below. 
1. Toolbar
2. Manage Your Data
3. Create Scenarios
4. Manage Scenarios
5. Manage Labels

## :wrench: Toolbar
The first feature to note, is the blue toolbar at the top of your browser window:

![](images/homepage.JPG)

- The <mark style="background-color: #1565c0">Home</mark> button will return the user to the Home Page at any time. 
- The <mark style="background-color: #1565c0">Docs</mark> button will direct the user to the following page with user instructions for installing docker, navigating the EVOLVE UI, downloading and editing the source code, using the legacy dashboard, and explanations of EVOLVE metrics. One can navigate these catgegories using the toolbar on the left of your window or the Next button in the bottom right. 
- The <mark style="background-color: #1565c0">Repo</mark> will direct the user to the EVOLVE github repository, where contributors can clone the repository, make pull requests, or raise issues. 


## :chart: Manage Your Data
The Manage Your Data tab is where the user will upload and manage timeseries data for load and/or irradiance values. 

![](images/manage_your_data_button.JPG)

The page will initially be blank until the user has uploaded datasets. To do so, first click on the blue <mark style="background-color: #1565c0">Upload Data</mark> button. 

![](images/manage_blank.JPG)

The user must first have a csv file prepared with the desired data to upload. The csv file should have two columns: a timestamp and the kw or irradiance values. The example below shows both types of data in the correct format for use in EVOLVE. The user must fill out the required fields, select the desired csv file, and click the blue <mark style="background-color: #1565c0">Submit</mark> button.

![](images/load_example_data.JPG)

![](imagesupload_data.JPG)

![](images/irradiance_example.JPG)

![](images/upload_irradiance.JPG)

Done correctly, and one should see their two datasets displayed as shown below. 

![](images/datasets.JPG)


## :sunny: :battery: :bus: :zap: Create Scenarios


After uploading data, the user must create scenarios they wish to model. This can be done by clicking the Create Scenarios tab. 

![](images/create_scenarios_button.JPG)

The user should pick a name for their scenario and select the desired technologies they wish to model.
The Basic Settings window is for adding information regarding the circuit's load profile. Select the load profile, a start and end date, and a data resolution. Note: if the user selects a data resolution that is smaller than that of the selected load profile, one will need to also select the data filling strategy. 

![](images/basic_settings.JPG)

For the selected technologies, fill out the required fields. One can add additional solar, EV, or energy storage systems (up to 5) using the blue button above each technology window. 

![](images/solar.JPG)

Once complete, click the blue <mark style="background-color: #1565c0">Submit</mark> button at the bottom of the page. 

## :bar_chart: Manage Scenarios
The next step is to run your scenario and produce results. This can be done on the Manage Scenarios tab. 

![](images/manage_scenarios_button.JPG)

![](images/manage_scenarios.JPG)

To run a scenario, click on the scenario and then select the grey play button on the right tool bar. One will be prompted to name the report and add a description. Once can also use this toolbar to delete, view, edit, or clone a given scenario as well as view any reports.

![](images/run_scenario.JPG)

![](images/name_report.JPG)


Once completed, the user should see an orange Completed under the report name. To view the results, click on the eye symbol on the report. 

![](images/completed_report.JPG)

One can visualize report results on this page or use the orange <mark style="background-color: orange" >Download Results!</mark> button to download csv files containing all data. 

![](images/download_results.JPG)


## :pushpin: Manage Labels
Lastly, users can use the Manage Labels tab to create labels to help organize and search for scenarios.  

![](images/manage_labels_button.JPG)


Use the create label button, add a name and description, and then one can add this label to scenarios using the grey plus icon on the report toolbar. These labels can be used to filter a large number of scenarios.

![](images/create_label.JPG)

![](images/sample_label.JPG)

![](images/labels.JPG)

![](images/add_label.JPG)

The user can filter their scenarios with the label buttons at the top of the Manage Scenarios Page.

![](images/filter_by_label.JPG)
