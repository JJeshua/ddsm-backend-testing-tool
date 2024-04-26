# Setting Up Environment Using Miniconda

This repository utilizes Miniconda to manage its Python environment. The `environment.yml` file specifies all the dependencies required to recreate the environment.

To set up the environment, follow these steps:

1. **Install Miniconda**: If you haven't already installed Miniconda, download and install it from the [Miniconda website](https://docs.conda.io/en/latest/miniconda.html).

2. **Clone the Repository**: Clone this repository to your local machine using Git:
```bash
git clone https://github.com/your-username/your-repository.git
```
3. **Navigate to the Repository Directory**: Move into the directory of the cloned repository:
```bash
cd your-repository
```
4. **Create the Conda Environment**: Create a new Conda environment using the environment.yml file:
```bash
conda env create -f environment.yml
```
  This will create a new environment named your-environment-name with all the required dependencies installed.
5. **Activate the Environment**: Activate the newly created environment:
```bash
conda activate your-environment-name
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
