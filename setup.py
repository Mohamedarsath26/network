from setuptools import find_packages,setup
from typing import List

def get_requirements()->List[str]:
    '''
    This function returns list of requiremensts
    '''
    requirement_ls:list[str] = [] 
    try:
        with open('requirements.txt','r') as file:
            #read lines from the txt file
            lines = file.readlines()

            for line in lines:
                requirement = line.strip()
                
                ##ignore empty line and '-e .'
                if requirement and requirement!='-e .':
                    requirement_ls.append(requirement)

    except FileNotFoundError:
        print("Requirements.txt file not found")


    return requirement_ls


setup(
    name='Network-Security',
    version="0.0.1",
    author="Mohamed Arsath",
    author_email="mdarsath2606@gmail.com",
    packages=find_packages(),
    install_requires=get_requirements()
)