from setuptools import find_packages, setup

setup(
    name='python-video-integration',
    description='',
    author='Diego B.',
    author_email='diegobassay@gmail.com',
    packages=find_packages(),
    install_requires=[
        'pymediainfo==2.3.0',
        'tinydb==3.12.2',
        'watchdog==0.9.0',
        'Flask==1.0.2',
        'flask_socketio==3.2.1',
        'eventlet==0.24.1',
        'gunicorn==19.9.0',
        'flask-classy==0.6.10',
        'requests==2.21.0',
        'pika==0.13.0'
    ],
    entry_points={
        'console_scripts': ['api=app.api:start', 
        					'watcher=app.watcher:start',
        					'web=app.web:start',
                            'consumer=app.consumer:start']
    })

