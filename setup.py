"""
   Copyright 2018 Ederson Bilhante

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
"""
from setuptools import setup

VERSION = __import__('pyhappn').__version__

setup(
    name='pyhappn',
    version=VERSION,
    description='This is a python client for the Happn API.',
    author='Ederson Brilhante',
    author_email='contato@edersonbrilhante.com.br',
    install_requires=[
        'requests==2.10.0',
    ],
    url='https://bitbucket.org/edersonbrilhante/happn',
    packages=['pyhappn'],
)
