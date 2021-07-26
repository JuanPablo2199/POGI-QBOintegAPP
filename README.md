# POGI-QBOintegAPP
This is a sample app used to sync data from pogi website to quickbooks 

### Getting Started

#### Install dependencies:

    cd SampleOAuth2_UsingPythonClient/
    pip install -r requirements.txt

#### Configure app

1. Enter your app's `Client ID`, `Client Secret`, `Redirect URL` found in your Intuit Developer App Portal and app `environment` (`production` or `sandbox`) in [settings.py](SampleOAuth2_UsingPythonClient/settings.py).
2. Make sure the same `Redirect URL` is entered in your Intuit developer app `Keys` tab under the right environment.
3. To test Migration API, also enter `OAuth1 credentials` in the same file.

#### Launch your app:
Using a terminal, run the following code:3

    python manage.py runserver

Launch URL `http://localhost:8000/app`
