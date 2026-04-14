import datetime
import os
import shutil
import subprocess
from pathlib import Path
from time import sleep
import pytest
from pandas.core.indexes.accessors import Properties

from Utils.commonlib import remove_file

parent_dir = os.getcwd()
project_dir = os.path.join(parent_dir, "Testcases")
ALLURE_RESULTS_DIR = os.path.join(parent_dir, "allure-results")
ALLURE_REPORT = os.path.join(parent_dir, "allure-report")
date_time = datetime.datetime.now(datetime.timezone.utc).strftime('%m-%d-%y-%H%M')
date = datetime.datetime.now(datetime.timezone.utc).strftime('%m-%d')
allure_reports = os.path.join(project_dir, 'Reports')
allure_images = os.path.join(project_dir, 'Images')
download = os.path.join(parent_dir, 'Download')
data = os.path.join(parent_dir, 'Data', 'qrcode.png')
ALLURE_HOME = shutil.which("allure")
ANSIBLE_HOME = shutil.which("ansible-playbook")


def main():
    # allure_file_html_name_old = f'{allure_reports}/html{get_value_from_prop("allure_file_html_name")}'
    allure_result_file = f'{allure_reports}/allure_results-{date_time}'
    allure_html_file = f'{allure_reports}/html/allure_report-html-{date_time}'
    pytest.main([project_dir, '--P=Tenforce', '--html=report.html', f'--alluredir={ALLURE_RESULTS_DIR}'])
    subprocess.run([
        "allure", "generate", ALLURE_RESULTS_DIR, "-o", ALLURE_REPORT,
        "--clean"
    ], check=True)

    if ALLURE_HOME is None:
        # ALLURE = get_value_from_prop('allure_home')
        try:
            subprocess.call([f'{ALLURE_HOME}', 'generate', allure_result_file, '-o', allure_html_file, '--clean'])
        except FileNotFoundError as e:
            print(e)
    else:
        try:
            subprocess.call([f'{ALLURE_HOME}', 'generate', allure_result_file, '-o', allure_html_file, '--clean'])
        except FileNotFoundError as e:
            print(e)
    single_file_html = os.path.join(allure_reports, f"allure_report_single_{date_time}.html")

    try:
        # If Allure CLI 2.20+ (supports --single-file)
        subprocess.run([
            f'{ALLURE_HOME}', "generate", allure_result_file,
            "--clean", "--single-file",
            "-o", single_file_html,
            "--plugins", "branding"
        ], check=True)
    except Exception:
        subprocess.run([
            f'{ALLURE_HOME}',
            "generate", allure_result_file,
            "--clean", "--single-file",
            "-o", single_file_html,
            "--plugins", "branding"
        ], check=True)
    sleep(2)
    # allure_misc_config(allure_html_file)
    subprocess.run([f'{ALLURE_HOME}', 'open', allure_html_file, '--host', '--port', '4444'])


def update_prop_file(key, val):
    CONFIG_FILE_PATH_PROP = os.path.join('Utils', 'allure.properties')

    prop_config = Properties()
    with open(CONFIG_FILE_PATH_PROP, 'rb') as r_file:
        prop_config.load(r_file)

        data = prop_config.get(key).data
        print(f'Current Data in the {key}:: {data} ===')
    prop_config[key] = val
    with open(CONFIG_FILE_PATH_PROP, 'wb') as w_file:
        prop_config.store(w_file)
        data = prop_config.get(key).data
        print(f'New value of {key}:: {data}')


if __name__ == '__main__':
    if not os.path.exists(allure_reports):
        os.makedirs(allure_reports)
    if not os.path.exists(allure_images):
        os.makedirs(allure_images)
    remove_file(allure_reports)
    remove_file(allure_images)
    try:
        if os.path.isfile(data):
            os.remove(data)
        elif os.path.isdir(data):
            for file in Path(data).glob("*"):
                if file.is_file():
                    file.unlink()
    except FileNotFoundError:
        pass  # Already gone, no problem
    except Exception as e:
        allure_reports.step(f"Error removing {data}: {e}")
    main()
