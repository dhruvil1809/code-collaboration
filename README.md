
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



# User documentation

**Table of Contents**

- [Getting Started](#getting-started)
- [Project Management](#project-management)
- [Real-Time Code Editing](#real-time-code-editing)
- [Version Control](#version-control)
- [User Interface](#user-interface)
- [Troubleshooting](#troubleshooting)

## Getting Started

1. **Accessing the Platform**

- Open your web browser and navigate to the platform’s URL.
- You will be greeted with the welcome page. If you don’t have an account, click on the `Sign up` button to create one.

2. **Registering a New Account**

- Click on the `Sign up` button.
- Fill in the required fields: username, email, and password.
- Click `Sign up` to create your account.

3. **Logging In**

- Enter your username and password on the login page.
- Click `Sign in` to access home page.

4. **Logging Out**

- Logout: Click on `Logout` link in navbar for logout.

## Project Management

1. **Creating a New Project**

- Navigate to the home page: Click on `Create a Project`.
- Fill in Project Details: Enter the project name and description.
- Create Project: Click `Create` to initialize your new project.

2. **Viewing Projects**

- Navigate to home page: Click on the project name to view its details.
- Explore Files: Click on individual files to view their contents.

3. **Updating a Project**

- Select Project: Go to the project you want to update.
- Edit Details: Click "Edit" icon to modify the project name or description.
- Save Changes: Click `Update` to apply the updates.

4. **Deleting a Project**

- Select Project: Go to the project you wish to delete.
- Delete: Click "Delete" icon and confirm to remove the project permanently.

## Real-Time Code Editing

1. **Accessing the Code Editor**

- Open a Project: Navigate to the project containing the file you want to edit.
- Open File: Click on the file name to open it.
- Edit File: Click on the "Edit" icon to open it in the real-time code editor.

2. **Collaborating in Real-Time**

- Multiple Editors: Invite collaborators to edit the same file.
- Live Updates: See changes made by others in real-time.

3. **Saving Changes**

- Save File: Click the `Save` button to save your changes.

## Version Control

1. **Viewing Version History**

- Open a File: Navigate to the file within the project.
- View History: Click on the file name to open it.

2. **Reverting to a Previous Version**

- view: Go to the version you wish to view and click on `View`.
- Revert: Click `Revert` to restore the selected version.

## User Interface

1. **Navigation**

- **Home**: Access all your projects and create new ones from the Home.
- **Project View**: Manage your projects and files from the project detail page.
- **Code Editor**: Real-time code editing is available through the integrated editor.

2. **Responsive Design**

- **Desktop**: The platform is optimized for a desktop experience.
- **Tablet**: The interface adjusts for optimal use on tablet devices
- **Mobile**: The interface adapts to mobile devices for on-the-go access.

## Troubleshooting

1. **Common Issues**

- **Unable to Log In**: Ensure your username and password are correct. Reset your password if needed.
- **Real-Time Editing Not Working**: Check your internet connection and ensure WebSockets are supported by your browser.