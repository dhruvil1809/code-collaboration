
# Code-collaboration

code collaboration platform where you and your team can work together seamlessly on the same code file. Experience instant updates, real-time changes, and stay in sync with every keystroke.

## Setup Instructions

1. **Clone the Repository**

    First, clone the repository to your local machine:
    ```
    git clone https://github.com/dhruvil1809/code-collaboration.git
    ```

2. **Create and Activate a Virtual Environment**

    Create a virtual environment using venv:
    ```
    python -m venv venv
    ```
    Activate the virtual environment:

    - **For Windows**:
        ```
        venv\Scripts\activate
        ```
    - **For macOS/Linux**:
        ```
        source venv/bin/activate
        ```

3. **Install Dependencies**

    Install the required packages listed in requirements.txt:
    ```
    pip install -r requirements.txt
    ```
    ```
    cd code_collab
    ```

4. **Apply Migrations**

    Run the migrations to set up your database schema:
    ```
    python manage.py migrate
    ```

5. **Run the Development Server**

    Start the Django development server:
    ```
    python manage.py runserver
    ```
    By default, the server will be accessible at http://127.0.0.1:8000/.


## Perform testing

1. **Run Test Cases**

    Run tests from a specific test file, use:
    ```
    python manage.py test tests.accounts_tests
    ```
    ```
    python manage.py test tests.projects_tests
    ```
    If the tests run successfully, you will see output indicating that all tests passed. For example:
    ```
    ----------------------------------------------------------------------
    Ran 9 tests in 5.152s

    OK
    Destroying test database for alias 'default'...
    ```