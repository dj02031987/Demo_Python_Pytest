Demo_PythonPytest_Fremwork
#Prerequisites Python 3.x installed

Google Chrome / Firefox installed

WebDriver (managed automatically using webdriver-manager or pre-configured)

#Folder structure

-APP_ObjectRepo: POM files of any project
    -Project Folder
        - Module Folder
            - POM files ( .py file)
-Test ObjectRepo: Testcase files
    -Project Folder
        -Module Folder
            - Testcase files (.py)
-Utils
    -commonlip.py: For common function use for logic  like delete folder and files , app configuration.
    -config.py For set config method from  Config.yml file
    -global_driver_utility.py For selenium locator's methods like send key , click . element list , Select , Action, Scroll, windows list, etc
-Config
    -Config.yml : for set configuration parameter like project url, mobile os version, UDID, username,password, etc.
-Data
    -For additional data files for testcase logic. like Excel file , Json file, etc.
-Reports
    -For Allure reports flies
-Download
    -For set download path and any file download from logic
-conftest.py
    -Base class file for testcase, it has browser selection method , parser.addoption parameter, @pytest.fixture setup and tear down methods, screenshot  and video file attached with report
-pytest.ini
    -For Pytest configuration
-runner.py
    -Automation run configuration file.
#How to Run Testcases

For testcase run ,the need to run runner file.

- configuration of runner file

    run main method from runner.py file. in main method there are pytest parameters set with below list.            
          -parent_dir : os.getcwd()  current directory of  
          -project_dir = os.path.join(parent_dir, 'Test_ObjectRepo', <set for ypu project testcase folder name)
          -pytest.main([project_dir, '--P=Tenforce', '--html=report.html', f'--alluredir={ALLURE_RESULTS_DIR}'])
              --P=<you project name same yml file configuration>
run comand : python3 runner.py

#Justification for choice of framework

Python + Selenium + Pytest based on the following advantages:

1.Simplicity & Readability Python offers clean, readable syntax which reduces maintenance effort. Easy onboarding for new team members.

Powerful Test Execution with Pytest Supports fixtures for reusable setup/teardown. Parametrization enables data-driven testing. Rich plugin ecosystem (HTML reports, parallel execution, retries).
3.Selenium for Cross-Browser Automation Industry-standard tool for UI automation. Supports multiple browsers and platforms.

Scalability & Maintainability Pytest + Page Object Model (POM) enables modular design. Easy integration with CI/CD tools like Jenkins/GitHub Actions.
#Architecture Overview The framework follows a Page Object Model (POM) design pattern with a layered architecture:

  project/
  │
  ├── tests/                # Test cases
  ├── pages/                # Page Object classes (UI locators + actions)
  ├── utils/                # Utilities (helpers, config, logger)
  ├── config/               # Environment & test configuration
  ├── conftest.py           # Pytest fixtures (driver setup, hooks)
  ├── requirements.txt      # Dependencies
  └── README.md             # Documentation
  

1. Page Layer (pages/)
Contains all web element locators and page-specific actions.
Promotes reusability and separation of concerns.

2. Test Layer (tests/)
Contains test scenarios using Pytest.
Uses page methods instead of direct Selenium calls.

3. Fixtures (conftest.py)
Centralized WebDriver setup & teardown.
Supports browser configuration and reuse across tests.

4. Utilities (utils/)
Logging, configuration reader, common helpers.
Keeps core logic clean and reusable.
