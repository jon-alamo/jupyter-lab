import os
import stat
import subprocess

from jupyter_core.paths import jupyter_data_dir

c = get_config()  # noqa: F821
c.ServerApp.ip = "0.0.0.0"
c.ServerApp.open_browser = False

# to output both image/svg+xml and application/pdf plot formats in the notebook file
c.InlineBackend.figure_formats = {"png", "jpeg", "svg", "pdf"}

# https://github.com/jupyter/notebook/issues/3130
c.FileContentsManager.delete_to_trash = False


def git_sync_after_save(model, os_path, contents_manager, **kwargs):
    try:
        old_dir = os.getcwd()
        directory = os.path.dirname(os_path)
        os.chdir(os.path.dirname(os_path))
        os.system(f'git commit -a -m "[AUTO] Changes to: {os_path}"')
        os.system('git add .')
        os.system(f'git commit -a -m "[AUTO] New files in {directory}."')
        os.system(f'git push -f')
        os.chdir(old_dir)

    except Exception as e:
        pass


c.FileContentsManager.post_save_hook = git_sync_after_save
