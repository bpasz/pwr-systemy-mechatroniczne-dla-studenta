from setuptools import find_packages, setup

package_name = 'l4_sterowanie'

setup(
    name=package_name,
    version='1.0.0',
    packages=find_packages(),
    data_files=[
        ('share/ament_index/resource_index/packages', ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Prowadzący kurs',
    maintainer_email='prowadzacy@pwr.edu.pl',
    description='L4: trzy sposoby sterowania robotem UR5e w Gazebo',
    license='MIT',
    entry_points={
        'console_scripts': [
            'pozycja_wprost = l4_sterowanie.pozycja_wprost:main',
            'trajektoria = l4_sterowanie.trajektoria:main',
            'ik_trajektoria = l4_sterowanie.ik_trajektoria:main',
            'rejestrator = l4_sterowanie.rejestrator:main',
        ],
    },
)
