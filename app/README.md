# Study Interval Application

This project is a study interval web application designed to help users manage their study sessions more effectively. It allows users to set study intervals, receive prompts for breaks, and summarise what they've learned in each interval. The application utilises a React frontend with TypeScript and a Flask backend, offering a robust and user-friendly study tool.

## Features

- **Study Session Management**: Start and stop study sessions.
- **Interval Timing**: Set the duration of study intervals.
- **Summarisation**: Summarise what you've studied in each interval.
- **Review**: Review summaries of past study sessions.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

- Node.js and npm
- Python 3 and pip

### Setting Up the Backend

1. Navigate to the `backend` directory:

    ```bash
    cd backend
    ```

2. Install the required Python dependencies:

    ```bash
    pip install -r requirements.txt
    ```

3. Start the Flask server:

    ```bash
    flask run
    ```

### Setting Up the Frontend

1. Navigate to the `frontend` directory:

    ```bash
    cd ../frontend
    ```

2. Install the required npm packages:

    ```bash
    npm install
    ```

3. Start the React development server:

    ```bash
    npm start
    ```

The React application should now be running on [http://localhost:3000](http://localhost:3000).

## Development

### Backend

The Flask backend handles API requests for managing study sessions, intervals, and summarisations. It is structured to support easy addition of new features and integrations.

### Frontend

The React frontend provides a user-friendly interface for interacting with the study interval application. TypeScript is used for better code quality and developer experience.

## Contributing

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct, and the process for submitting pull requests to us.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.

## Acknowledgments