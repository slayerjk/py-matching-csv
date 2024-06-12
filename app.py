# IMPORT PROJECTS PARTS
from time import perf_counter

from project_static import appname, start_date_n_time, logging, logs_dir, logs_to_keep, data_files, result_dir
from project_static import file_old, file_new

from app_scripts.project_helper import files_rotate, check_create_dir, func_decor, check_file

from app_scripts.app_functions import parse_csv, matching_data, write_csv

# MAILING IMPORTS(IF YOU NEED)
# from app_scripts.project_static import mailing_data, smtp_server, smtp_port, smtp_login, smtp_pass, smtp_from_addr,\
#     mail_list_admins, mail_list_users
# from app_scripts.project_mailing import send_mail_report, send_mail


# SCRIPT STARTED ALERT
logging.info(f'SCRIPT WORK STARTEDED: {appname}')
logging.info(f'Script Starting Date&Time is: {str(start_date_n_time)}')
logging.info('----------------------------\n')

# START PERF COUNTER
start_time_counter = perf_counter()

# CHECKING DATA DIRS & FILES

# CHECK DATA FILES EXIST
func_decor('Cheking file exist', 'crit')(check_file(file_old))
func_decor('Cheking file exist', 'crit')(check_file(file_new))

# CHECK DATA DIR EXIST/CREATE
func_decor(f'checking {data_files} dir exists and create if not')(check_create_dir)(data_files)
func_decor(f'checking {result_dir} dir exists and create if not')(check_create_dir)(result_dir)

# CHECK MAILING DATA EXIST(IF YOU NEED MAILING)
# func_decor(f'checking {mailing_data} exists', 'crit')(check_file)(mailing_data)


# MAIN CODE

# PARSING DATA
old_data = func_decor(f'Parsing csv: {file_old}')(parse_csv)(file_old)
# PRINT old_data example
# print(old_data[0])

new_data = func_decor(f'Parsing csv: {file_new}')(parse_csv)(file_new)
# PRINT old_data example
# print(new_data[0])


# MATCHING DATA
new_hosts, excluded_hosts, changed_hosts = func_decor('Matching data', 'crit')(matching_data)(old_data, new_data)

if len(new_hosts) > 0:
    logging.info(f'\nNew Hosts Found: {len(new_hosts)}')
    [logging.info(host) for host in new_hosts]
    func_decor('Writing NEW hosts to file', 'crit')(write_csv)(new_hosts, f'{result_dir}/RESULT-NEW.csv')
else:
    logging.info(f'No New hosts found in NEW Scope list!')

if len(excluded_hosts) > 0:
    logging.info(f'\nExcluded Hosts Found: {len(excluded_hosts)}')
    [logging.info(host) for host in excluded_hosts]
    func_decor('Writing EXCLUDED hosts to file', 'crit')(write_csv)(excluded_hosts, f'{result_dir}/RESULT-EXCLUDED.csv')
else:
    logging.info(f'No Excluded hosts found in OLD Scope list!')

if len(changed_hosts) > 0:
    logging.info(f'\nChanged Hosts Found: {len(changed_hosts)}')
    [logging.info(host) for host in changed_hosts]
    func_decor('Writing CHANGED hosts to file', 'crit')(write_csv)(changed_hosts, f'{result_dir}/RESULT-CHANGED.csv')
else:
    logging.info(f'No Changed hosts found while matching Old & New scopes!')

# POST-WORK PROCEDURES

# FINISH JOBS
logging.info('#########################')
logging.info('SUCCEEDED: Script job done!')
logging.info(f'Estimated time is: {perf_counter() - start_time_counter}')
logging.info('----------------------------\n')
files_rotate(logs_dir, logs_to_keep)


# MAIL REPORT(IF YOU NEED)
# send_mail_report(appname, mail_list_admins, smtp_from_addr, smtp_server, smtp_port, app_log_name, login=None,
