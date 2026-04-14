import datetime
import os
import shutil
import subprocess
import shlex
from pathlib import Path
from time import sleep
import pytest
import webbrowser

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


def _find_allure_executable():
    global ALLURE_HOME
    if ALLURE_HOME and os.path.exists(ALLURE_HOME):
        return ALLURE_HOME
    cmd = shutil.which('allure')
    if cmd:
        ALLURE_HOME = cmd
        return cmd
    return None

def _run_allure(cmd_args, check=True):
    allure_exec = _find_allure_executable()
    if not allure_exec:
        raise FileNotFoundError("Allure executable not found in PATH. Please install Allure CLI and ensure it's on PATH.")
    if os.name == 'nt' and not allure_exec.lower().endswith('.exe'):
        # Build a quoted command string to run via shell
        quoted = ' '.join([f'"{allure_exec}"'] + [f'"{arg}"' for arg in cmd_args])
        return subprocess.run(quoted, check=check, shell=True)
    cmd = [allure_exec] + cmd_args
    return subprocess.run(cmd, check=check)


def main():
    # allure_file_html_name_old = f'{allure_reports}/html{get_value_from_prop("allure_file_html_name")}'
    allure_result_file = f'{allure_reports}/allure_results-{date_time}'
    allure_html_file = f'{allure_reports}/html/allure_report-html-{date_time}'
    pytest.main([project_dir, '--P=Tenforce', '--html=report.html', f'--alluredir={ALLURE_RESULTS_DIR}'])
    try:
        _run_allure(['generate', ALLURE_RESULTS_DIR, '-o', ALLURE_REPORT, '--clean'])
    except FileNotFoundError as e:
        print(f"Allure not found: {e}")
    except subprocess.CalledProcessError as e:
        print(f"Allure generate failed: {e}")
    single_file_html = os.path.join(allure_reports, f"allure_report_single_{date_time}.html")
    tried_sources = [ALLURE_RESULTS_DIR, allure_result_file]
    generated_single = False
    for src in tried_sources:
        if not os.path.exists(src):
            continue
        try:
            _run_allure(['generate', src, '--clean', '--single-file', '-o', single_file_html, '--plugins', 'branding'])
            generated_single = True
            break
        except subprocess.CalledProcessError:
            try:
                _run_allure(['generate', src, '--clean', '--single-file', '-o', single_file_html])
                generated_single = True
                break
            except Exception as e:
                print(f"Failed to create single-file Allure report from {src}: {e}")
        except FileNotFoundError:
            break

    if not generated_single:
        print("Single-file Allure report was not created. Check that Allure CLI >=2.20 is installed and the results folder contains test results.")

    sleep(2)
    try:
        _run_allure(['open', allure_html_file, '--host', '--port', '4444'])
    except Exception:

        html_path = allure_html_file
        if os.path.isdir(allure_html_file):
            # If a directory was generated, point to index.html inside
            index_path = os.path.join(allure_html_file, 'index.html')
            if os.path.exists(index_path):
                html_path = index_path
        if os.path.exists(html_path):
            try:
                if os.name == 'nt':
                    os.startfile(html_path)
                else:
                    webbrowser.open_new_tab(f'file://{os.path.abspath(html_path)}')
            except Exception as e:
                print(f"Failed to open report automatically: {e}")
        else:
            print(f"Allure report not found at {html_path}")


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
        print(f"Error removing {data}: {e}")
    main()
