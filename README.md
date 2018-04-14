# ansible

Ansible roles with Molecule.


## Usage

    host$ # Configure virtualenv.
    host$ virtualenv virtualenv
    host$ . virtualenv/bin/activate
    (virtualenv) host$ pip install -r requirements.txt

    (virtualenv) host$ # Workaround CentOS / RHEL / Fedora SELinux vs. Ansible snafu.
    (virtualenv) host$ rpm -q -l libselinux-python
    /usr/lib64/python2.7/site-packages/_selinux.so
    /usr/lib64/python2.7/site-packages/selinux
    /usr/lib64/python2.7/site-packages/selinux/__init__.py
    /usr/lib64/python2.7/site-packages/selinux/__init__.pyc
    /usr/lib64/python2.7/site-packages/selinux/__init__.pyo
    /usr/lib64/python2.7/site-packages/selinux/audit2why.so
    (virtualenv) host$ cp -a \
            /usr/lib64/python2.7/site-packages/_selinux.so \
            /usr/lib64/python2.7/site-packages/selinux/ \
            virtualenv/lib64/python2.7/site-packages/

    (virtualenv) host$ # Run tests.
    (virtualenv) host$ ( cd ./roles/common/ ; molecule test )
    (virtualenv) host$ ( cd ./roles/docker/ ; molecule test )


## Adding new roles

    (virtualenv) host$ cd roles
    (virtualenv) host$ molecule init role -r rolename -d docker
    (virtualenv) host$ cd rolename
    (virtualenv) host$ molecule test
