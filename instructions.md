# Instructions

These are the instructions to be followed before running the sentence deconstructor. 

1. Clone the repository
2. It is advised to create a virtual environment. The Anaconda command for the same is ```conda create --prefix "prefix path to your venv" --name <name of venv>```
3. Activate the virtual environment using the command ```conda activate <path to your venv>```
4. Once activated, all the required libraries need to be installed. 

    - Ensure that [PyTorch](https://pytorch.org/) is installed before pip installing the requirements file.
    
    - After installing PyTorch, install the other required libraries using the command ```pip install -r requirements.txt```

5. After all the libraries have been installed, the deconstructor can be run with the command ```python3 sentence-deconstructor.py```
6. Each individual component can also be run by navigating to the **src** directory and running ```python3 <name of file>.py```


