# Development Documentation

The development documentation outlines the design and implementation process of the system, breaking down its structure into three main parts:
**UI Development**, **Core Functional Classes**, and **Internationalization**.

# UI Development

The user interface is created with **PySide6**.
We use **Qt Designer** to set up the overall components and layout.
The components and content are then further customized and populated using code.

## Layout Design with Qt designer.exe

To design the layout prototype, we use **Qt Designer**, which allows you to visually construct the interface with elements such as buttons, labels, tables, etc.
You can easily drag components from the widget box and position them within the window as needed.
The **Object Inspector** and **Property Editor** enables you to adjust various attributes for each component, like the object name, tooltip, size, and other properties.
Once the design is complete, it can be saved as a `.ui` file for further use.

### Converting `.ui` Files to Python Files

After saving the layout as a `.ui` file, `pyside6-uic` is used to convert it into a Python file (`.py`).
This conversion generates Python code that can be used to instantiate classes directly within the application code.

## Actions and Icons

In a GUI application, the same action can be performed in multiple ways, such as through a menu option, a toolbar icon, or a keyboard shortcut.
PyQt uses the `QAction` class to encapsulate these actions, allowing them to be independently linked to different UI elements, which reduces code coupling and improves maintainability.
Essentially, `QAction` serves as an abstract representation of an action used across menus, toolbars, and shortcuts, ensuring flexibility and consistency.

### Converting `.qrc` File to Python Files

When icons are added to `QAction` instances, they are displayed on the toolbar for quick access.
To use icons from resource files (`*.qrc`) in code, you need to convert the resource file into a Python file (`*.py`) using the `pyside6-rcc` tool. 


### Icon Resources and License

The toolbar uses icons from [Huge Icons](https://icon-sets.iconify.design/hugeicons/),
which are licensed under the [MIT License](../src/resources/license/MIT LICENSE.txt). 

To show the keyfile status in both disk and database, we use icons from
[Material Symbols Light](https://icon-sets.iconify.design/material-symbols-light/),
which are licensed under the
[Apache License 2.0](../src/resources/license/Apache%20LICENSE.txt).

## Automatic build
We provide a script to automate the conversion of `.ui` and `.qrc` files into `.py` files, streamlining the development process.
To use it, simply run the script `convertpyfile.py` in the terminal.
Then it will generate the corresponding `.py` files under the project path `src/frontend/ui`.

# Core Functional Classes

The core functional code has two main parts: backend and  frontend. Below is an introduction of each class.

## Backend

**`keyhandler.py`**: Handles keyfile-related operations on disk, such as toggling activation 
 and performing soft deletion by moving files between directories.

**`foldercontent.py`**: Reads the content within keyfiles on disk, specifically the `userProperties.json` and `gageSegment.json` files,
and handles operations on the `metadata.json` file.


## Frontend

**`keystatus.py`**:  Enumeration class that defines activation statuses. 
  
- **ACTIVATED**: The keyfile is activated and located in the activated directory on disk.  
- **DEACTIVATED**: The keyfile is deactivated and located in the deactivated directory on disk.

**`mainwindow.py`**: The main application window class that coordinates various UI components and connects actions to their corresponding behaviors.

**`configmanager.py`**: Manage the loading, saving, and validation of configuration settings for directories paths.

**`hoverinfo.py`**: Display explanatory information when the mouse hovers over a table cell, providing details about the cell's content as well as its state.

**`tableoperator.py`**: Handle operations on the table, filtering based on various criteria (hidden some rows), and table checkbox selections (check all/uncheck all).
This class performs UI-level changes only and does not modify the database. 

**`metadataeditor.py`**: Add, edit, and delete metadata fields in keyfiles.  

**`renamesensor.py`**: Rename the sensor name in the `userProperties.json` file.  

**`trashmanager.py`**: Manage the deletion and restoration of keyfiles.


# Internationalization (i18n)

In the `.ui` files, any widget property marked as translatable, or strings enclosed within the `tr()`  in the code,
will be flagged for translation.  We use **Qt Linguist** to implement the internationalization of the application.

## Generate Translation Files 

To do transaltion, a `.pro` file needs to be created to include all relevant `.ui` and `.py` files that contain translatable content.
The `pyside6-lupdate` will scan the files listed in the `.pro` file and generates the corresponding translation files (`.ts`) for the target language.
These `.ts` files can then be opened with **Qt Linguist** to review and translate the extracted content.

## Release and Use with QTranslator

After translation, you can release the translations in **Qt Linguist**, which generates `.qm` files.
Then in the code, you can use `QTranslator` to load these `.qm` files, allowing the application to switch languages dynamically.


# CI/CD

## Gitlab CI/CD
GitLab CI/CD is an automation tool that allows you to execute workflows (such as build, test, deploy) whenever changes occur in a repository. 
CI/CD pipelines are defined in a .gitlab-ci.yml file and include various stages and jobs. 
Below are the main keywords we have used in GitLab CI/CD and their explanations.

### Runner
In GitLab CI/CD, you need to set up and connect your own runner to execute jobs in the pipeline.  
Runners can be configured on various operating systems, including Linux, Windows, and macOS.

### Syntax

- **stages**: `Stages` are used to define the different phases of the pipeline (e.g., build, test, deploy). 
GitLab CI/CD will execute jobs in the specified order, and jobs within the same stage can run in parallel.

- **stage**: Use `stage` within each job definition to specify the phase to which the job belongs.

- **tags**: `Tags` are used to select a specific runner from the list of available runners for the project. 

- **image**: The `image` keyword specifies a Docker image that the job runs in, ensuring consistent environments across jobs.

- **before_script**: Use `before_script` to define an array of commands that should run before each job’s script commands. 
It is commonly used to set up environments or install dependencies.

- **script**: The `script` keyword specifies commands for the runner to execute. 
It is the core part of each job, defining the tasks the job will perform.

- **artifacts**: Artifacts specify which files to save as job artifacts, typically used for build outputs, logs, or test results.

- **only**: Use `only` to define conditions for when a job should run, such as specific branches.


### GitLab Pages

Use `pages` to define a GitLab Pages job that uploads static content to GitLab.  
The content is stored in the `public` directory and is then published as a website, making it accessible via a GitLab-generated URL.  
Here, we use it to host the Doxygen-generated documentation for our code.

## GitHub CI/CD

In GitHub, GitHub Actions is used as a CI/CD platform.

Similar to GitLab, GitHub Actions uses YAML files to define workflows.  
These workflows are defined within the `.github/workflows` directory in the repository.  
A repository can contain multiple workflows, each performing different tasks such as building, testing, and deploying.  
GitHub also provides pre-created actions that can be used to create your own workflows.

### Runner
GitHub provides Ubuntu Linux, Microsoft Windows, and macOS runners to run your workflows.
You can also use your own runner.

### Syntax

- **name**: Define a name for the workflow.
- **run-on**: Specify the type of runner that the workflow will use, such as `ubuntu-latest`, `windows-latest`, or `macos-latest`.
- **steps**: Defines individual steps in the workflow. Steps are executed sequentially within a job.
- **run**: Specifies a command to execute directly within a step.
- **uses**: This can be an action from the GitHub Marketplace.
- **with**: Used with `uses` to pass input parameters to an action.

### GitHub Pages

Similar to GitLab Pages, GitHub Pages is a feature for hosting static websites. 
However, for free accounts, GitHub Pages can only be used with public repositories. 
Only with a **GitHub Enterprise** account, you can restrict access to your GitHub Pages site by publishing it privately.  

To set up GitHub Pages for hosting static content, navigate to **Settings** -> **Pages** in your repository.