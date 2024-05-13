# Setting Up Environment Using Miniconda

This repository utilizes Miniconda to manage its Python environment. The `environment.yml` file specifies all the dependencies required to recreate the environment.

To set up the environment, follow these steps:

1. **Install Miniconda**: If you haven't already installed Miniconda, download and install it from the [Miniconda website](https://docs.conda.io/en/latest/miniconda.html).

2. **Clone the Repository**: Clone this repository to your local machine using Git:
```bash
git clone https://github.com/JJeshua/ddsm-backend-testing-tool.git
```
3. **Navigate to the Repository Directory**: Move into the directory of the cloned repository:
```bash
cd ddsm-backend-testing-tool
```
4. **Create the Conda Environment**: Create a new Conda environment using the environment.yml file:
```bash
conda env create -f environment.yml
pip install -e .
```
This will create a new environment named APITesting with all the required dependencies installed.

5. **Activate the Environment**: Activate the newly created environment:
```bash
conda activate APITesting
```
6. **Verify Installation**: You can verify that the environment was installed correctly by running:
```bash
conda env list
```
7. **Start Working**: You're all set! You can now start working within this environment. Remember to activate the environment whenever you're working on this project.
8. **Deactivate the Environment**: When you're done working in the environment, you can deactivate it:
```bash
conda deactivate
```
# Running Tests with Pytest

This repository uses Pytest for testing. You can run all tests easily using the `pytest` command.

To run all tests, follow these steps:

1. **Activate the Conda Environment**: Before running the tests, ensure that you have activated the Conda environment created for this project. If you haven't activated it yet, you can do so by running:
```bash
conda activate APITesting
```
2. **Navigate to the Project Root Directory**: CD to the root directory **ddsm-backend-testing-tool**.
3. **Run Pytest**: Once you're in the tests directory, simply run the following command to execute all tests:
  ```bash
  pytest
  ```
# Using the DB Tools
## Usage
1. **Navigate to the root directory**: CD the root directory of ddsm-backend-testing-tool
2. **Run the Script**: Execute the script using Python:
```bash
python db_tools.py [action]
```
3. **Available Actions**:
* populate: This action populates the database with sample data.
* clear: This action clears the entire database.
