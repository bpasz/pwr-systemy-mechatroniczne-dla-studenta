from glob import glob

from setuptools import find_packages, setup

package_name = 'l3_regulator'

setup(
    name=package_name,
    version='1.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages', ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        ('share/' + package_name + '/launch', glob('launch/*.launch.py')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Prowadzący kurs',
    maintainer_email='prowadzacy@pwr.edu.pl',
    description='L3: wirtualny czujnik odległości i regulator dla turtlesim',
    license='MIT',
    entry_points={
        'console_scripts': [
            'czujnik = l3_regulator.czujnik:main',
            'regulator = l3_regulator.regulator:main',
        ],
    },
)
