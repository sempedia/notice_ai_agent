
# NoticeAI - AI Agent for Email Extraction

## Overview

**NoticeAI** is an AI agent built using **LangChain** and **LangGraph** to process incoming emails from regulatory bodies, such as safety violations or compliance notices, and extract critical information. The extracted data can then be used to notify internal teams in a Django-based e-commerce platform, based on microservices and orchestrated with **Terraform** in the **AWS** cloud.

## Key Features

- **Email Parsing**: Extracts essential fields from regulatory notice emails, including project ID, violation type, entity name, contact information, required changes, compliance deadlines, and potential fines.
- **Date Parsing**: Extracted dates are converted into proper date objects using **Pydantic** computed fields.
- **Modular Design**: Designed to be easily extendable for additional fields and email formats.
- **Integration**: Intended for integration with a growing e-commerce platform.

## Technology Stack

- **LangChain**: Used to create a language model pipeline for email parsing.
- **LangGraph**: For orchestrating the chain and handling the flow of extracted information.
- **Pydantic**: Data validation and settings management.
- **Python**: The primary programming language used for the implementation.
- **AWS**: For deployment and cloud infrastructure.
- **Django**: Backend for the e-commerce platform.
- **Terraform**: Infrastructure as code to manage AWS resources.
- **Poetry**: Dependency management and packaging for Python projects.
- **Pytest**: Testing framework for unit tests and integration testing.
- **pytest-cov**: Test coverage reporting for ensuring code quality.

## Project Structure

### `chains/notice_email_extraction.py`

This file contains the `NoticeEmailExtract` class, which defines the fields to be extracted from the email, such as:

- `entity_name`
- `entity_phone`
- `entity_email`
- `project_id`
- `violation_type`
- `site_location`
- `compliance_deadline`
- `max_potential_fine`

The class includes methods to convert string dates to `datetime.date` objects.

## Installation

To install the dependencies for this project, use **Poetry**:

```bash
poetry install

Make sure you have a valid OpenAI API key and the necessary AWS credentials set up for deployment.

## Tests
The project includes unit tests for the following:

Model Tests: Ensuring that the data fields are properly extracted and converted.

Validation Tests: Ensuring correct handling of edge cases like missing fields or invalid dates.

Numeric and Text Validations: Ensuring the agent handles invalid numeric inputs and extra spaces in text fields.

To run the tests, use:
```
pytest --cov=chains --cov-report=term-missing
```

## Test Coverage
To generate a test coverage report, you can use pytest-cov with the following command:

```
pytest --cov=chains --cov-report=htmlcov
```

This will generate an HTML test coverage report that can be shared with your team.

## Future Work
As the project grows, I plan to integrate additional features, such as:

Expanding the types of emails parsed (e.g., notifications for other types of regulatory issues).

Integrating with the larger Django e-commerce system for automated notifications and actions based on the parsed data.

Scaling the solution using AWS Lambda and AWS SQS for handling large volumes of incoming emails.

## License
This project is licensed under the terms of the MIT License.

## Author 
#Alina Bazavan
#Email: sempedia@gmail.com
