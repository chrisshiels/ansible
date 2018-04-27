import os
import re

import pytest
import testinfra.utils.ansible_runner


testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
                    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


@pytest.mark.parametrize('name',
                         [ 'device-mapper-persistent-data',
                           'lvm2',
                           'yum-utils' ])
def test_package_dependency(host, name):
  package = host.package(name)
  assert package.is_installed


def test_yum_repository(host):
  f = host.file('/etc/yum.repos.d/docker-ce.repo')
  assert f.exists
  assert f.is_file
  assert f.user == 'root'
  assert f.group == 'root'
  assert f.mode == 0644
  assert f.contains('\[docker-ce\]')
  assert f.contains('name = Docker CE Stable')
  assert f.contains('baseurl = https://download.docker.com/linux/centos/7/$basearch/stable')
  assert f.contains('gpgcheck = 1')
  assert f.contains('gpgkey = https://download.docker.com/linux/centos/gpg')


def test_package(host):
  package = host.package('docker-ce')
  assert package.is_installed


def test_service(host):
  service = host.service('docker')
  assert service.is_running


def test_helloworld(host):
  command = host.command('docker run --rm hello-world')
  assert re.match('\nHello from Docker!\n', command.stdout)
  assert command.rc == 0
