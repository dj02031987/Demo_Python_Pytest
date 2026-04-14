import os
import shutil

import pandas as rd


def readexcelfile(filepath):
    df = rd.read_excel(filepath)
    data = df.to_dict(orient='records')
    return data


def remove_file(path):
    # removing the file
    for filename in os.listdir(path):
        file_path = os.path.join(path, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))


def mobileapp_config(device_name, config):
    if device_name.startswith('a'):
        capabilities = {
            "platformName": "Android",
            "appium:app": config['androidApp_config']['app'],
            "appium:platformVersion": config['androidApp_config']['platformVersion'],
            "appium:automationName": "UiAutomator2",
            "appium:udid": config['androidApp_config']['udid'],
            "noReset": False,
            "unicodeKeyboard": False,
            "resetKeyboard": False,
            # "chromedriverExecutable": config['androidApp_config']['chrome_driver'],
            # "autoGrantPermissions": True,
        }
    else:
        capabilities = {
            "platformName": "iOS",
            "appium:app": config['isoApp_config']['app'],
            "appium:platformVersion": config['androidApp_config']['platformVersion'],
            "appium:automationName": "XCUITest",
            "appium:udid": config['isoApp_config']['udid'],
            "appium:appWaitForLaunch": False,
            "unicodeKeyboard": False,
            "resetKeyboard": False
        }
    return capabilities
