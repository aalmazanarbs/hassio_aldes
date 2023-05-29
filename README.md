# Home Assistante custom component for Aldes products

Simple integration to allow to select Aldes products mode from Home Assitant just providing username and password.

Check the list of [supported products](https://github.com/aalmazanarbs/hassio_aldes/blob/master/aldes/product.py#L20).

## Features

* Login in Aldes API with Oauth 2
* Configure Home Assitant Aldes entities
* Allow to change Aldes products mode
* Configure `Holidays` mode without specifying date

## Installation on Home Assistant

Download all files and copy them to "config/custom_components/aldes".
Restart your Home Assistant and add Aldes integration in Integration section.
Use your Aldesconnect credentials to login.
