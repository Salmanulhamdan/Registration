# Registration

## Requirements

- Python 3.10.12

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/Salmanulhamdan/Registration.git
    ```

2. Navigate to the project directory:

    ```bash
    cd registration
    ```

3. Create and activate a virtual environment (optional but recommended):

    ```bash
    python3 -m venv env
    # On Windows: env\Scripts\activate
    # On macOS/Linux: source env/bin/activate
    ```

4. Install project dependencies:

    ```bash
    pip install -r requirements.txt
    ```

5. Apply database migrations:

    ```bash
    python3 manage.py migrate
    ```



6. Run the development server:

    ```bash
    python3 manage.py runserver
    ```

7. Access the application at [http://127.0.0.1:8000/](http://127.0.0.1:8000/)