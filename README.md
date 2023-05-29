# Home Assistante custom component for Aldes products

Simple integration to allow to select Aldes products mode from Home Assitant just providing username and password.

Check the list of [supported products](https://github.com/aalmazanarbs/hassio_aldes/blob/master/aldes/product.py#L20).

## Features

* Login in Aldes API with Oauth 2
* Configure Home Assitant Aldes entities
* Allow to change Aldes products mode
* Configure `Holidays` mode without specifying date

## Installation on Home Assistant

### Using HACS
This is not part of the default store and has to be added as a custom repository.

Setting up a custom repository is done by:

Go into HACS from the side bar.
Click into Integrations.
Click the 3-dot menu in the top right and select Custom repositories
In the UI that opens, copy and paste the url for this github repo into the Add custom repository URL field.
Set the category to Integration.
Click the Add button.
Restart your Home Assistant and add Aldes integration in Integration section.
Use your Aldesconnect credentials to login.

### Manual installation
Download all files and copy them to "config/custom_components/aldes" folder.
Restart your Home Assistant and add Aldes integration in Integration section.
Use your Aldesconnect credentials to login.
