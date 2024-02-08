# Handle git configuration and repository cloning
import os
import json
import re
import ipywidgets as iw
import subprocess
from IPython.display import Markdown
from IPython.display import Javascript, HTML

error = None
output = None

email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
save_file_path = '.gitdata.json'
ssh_key_file = '/home/jovyan/work/.id_rsa.pub'

def md(text):
    display(Markdown(text))

def load():
    if os.path.exists(save_file_path):
        with open(save_file_path, 'r') as f:
            saved_data = json.load(f)
        git_repo_text.value = saved_data['repo']
        git_name_text.value = saved_data['name']
        git_email_text.value = saved_data['email']

def save():
    with open(save_file_path, 'w') as f:
        data = {
            'repo': git_repo_text.value,
            'name': git_name_text.value,
            'email': git_email_text.value
        }
        json.dump(data, f)


def clone_repository(*args, **kwargs):
    if not git_repo_text.value.strip():
        messages_text.value = 'Git repo is missing!'
        return
    if not git_name_text.value.strip():
        messages_text.value = 'Git name is missing!'
        return
    if not re.fullmatch(email_pattern, git_email_text.value.strip()):
        messages_text.value = 'Git email is not valid!'
        return
    
    process = subprocess.Popen(['git', 'clone', git_repo_text.value], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    # Capturar la salida y el error (si lo hay)
    output, error = process.communicate()

    if error:
        messages_text.value = error.decode()
    else:
        messages_text.value = 'Repository cloned!'
    
    folder_name = git_name_text.value.split('/')[-1].replace('.git', '')
    name = git_name_text.value
    email = git_email_text.value
    path = '/home/jovyan/work/{folder_name}'
    os.system(f'git -C {repo_name} config user.name "{name}"')
    os.system(f'git -C {repo_name} config user.email "{email}"')
    save()

subprocess.run(['bash', '.keygen.sh'])

width_layout = iw.Layout(width='500px')
text_area_layout = iw.Layout(width='500px', height='160px')

with open(ssh_key_file, 'r') as id_rsa_file:
    id_rsa_pub = id_rsa_file.read()

ssh_key_text = iw.Textarea(layout=text_area_layout)
ssh_key_text.disabled = True
ssh_key_text.value = id_rsa_pub

git_repo_text = iw.Text(layout=width_layout)
git_name_text = iw.Text(layout=width_layout)
git_email_text = iw.Text(layout=width_layout)
git_clone_button = iw.Button(description='Clone!')
messages_text = iw.Text(layout=width_layout)
git_clone_button.on_click(clone_repository)

md("""
# Configure git for synchronization
Configure a git repository to sync files with a remote repository.
Remote repository shouldn't be operated manually to avoid conflicts.
Jupyterlab is configured to trigger a git push when a file is saved
automatically when the repository is configured.

## SSH Key
Copy following ssh public key and paste into your repository access settings:
""")
display(ssh_key_text)

md("""
## Repository url
Paste the url of the repository to be used. For the first time, the repository will be cloned into local jupyter directory.
""")
display(git_repo_text)

md("""
## Repository user
Introduce a name to identify user actions in repository:
""")
display(git_name_text)

md("""
## Repository email
Introduce an email which to identify the current user:
""")
display(git_email_text)

md("""
## Clone repository
Press to clone repository:
""")

display(iw.HBox([git_clone_button, messages_text]))

# Load data
load()