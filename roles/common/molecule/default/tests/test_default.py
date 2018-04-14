import os

import pytest
import testinfra.utils.ansible_runner


testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
                    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


@pytest.mark.parametrize('name',
                         [ 'lsscsi',
                           'ltrace',
                           'strace' ])
def test_package(host, name):
  package = host.package(name)
  assert package.is_installed


def test_prompt_root(host):
  command = host.command('bash -l -c "printenv PS1"')
  assert command.stdout == '\\h# '
  assert command.rc == 0


@pytest.mark.parametrize('name',
                         [ 'docker',
                           'libvirt',
                           'wheel' ])
def test_usersgroups_secondary_groups(host, name):
  group = host.group(name)
  assert group.exists


@pytest.mark.parametrize(str.join(',',
                                  [
                                    'name',
                                    'state',
                                    'uid',
                                    'gid',
                                    'groups',
                                    'comment',
                                    'home',
                                    'shell',
                                    'password'
                                  ]),
                         [
                           (
                             'user1000',
                             'present',
                             1000,
                             1000,
                             [ 'wheel', 'libvirt', 'user1000' ],
                             'User 1000',
                             '/home/user1000',
                             '/bin/bash',
                             '*'
                           ),
                           (
                             'user1001',
                             'present',
                             1001,
                             1001,
                             [ 'wheel', 'docker', 'user1001' ],
                             'User 1001',
                             '/home/user1001',
                             '/bin/bash',
                             '*'
                           ),
                           (
                             'user1002',
                             'absent',
                             1002,
                             1002,
                             [ 'user1002' ],
                             'User 1002',
                             '/home/user1002',
                             '/bin/bash',
                             '*'
                           )
                         ])
def test_usersgroups(host,
                     name,
                     state,
                     uid,
                     gid,
                     groups,
                     comment,
                     home,
                     shell,
                     password):
  group = host.group(name)
  if state == 'present':
    assert group.exists
    assert group.gid == gid
  else:
    assert not group.exists

  user = host.user(name)
  if state == 'present':
    assert user.exists
    assert user.uid == uid
    assert user.gid == gid
    assert user.group == name
    assert sorted(user.groups) == sorted(groups)
    assert user.gecos == comment
    assert user.home == home
    assert user.shell == shell
    assert user.password == password
  else:
    assert not user.exists
