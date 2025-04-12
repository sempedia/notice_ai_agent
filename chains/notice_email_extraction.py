# Import necessary libraries
from datetime import datetime, date  # For date manipulation and conversion
from langchain_core.prompts import ChatPromptTemplate  # LangChain for building prompt templates
from langchain_openai import ChatOpenAI  # LangChain OpenAI integration for using GPT models
from pydantic import BaseModel, Field, computed_field  # Pydantic for data validation and model creation

# NoticeEmailExtract class - is responsible for defining the structure of the data we expect to extract from notice emails
class NoticeEmailExtract(BaseModel):
    """Extracts structured information from notice emails.

    This class defines the structure for extracting key data points from notice emails,
    such as dates, entity details, project information, violation details, and potential fines.
    It uses Pydantic for data validation and model creation.
    """
    # The string representation of the notice's date but won't be included in the output
    # (set `exclude=True`) and won't be printed (set `repr=False`).
    date_of_notice_str: str | None = Field(
        default=None,  # If no value is provided, it will default to None
        exclude=True,  # Exclude this field from the output
        repr=False,  # Don't show this field in the string representation of the object
        description="""The date of the notice (if any) reformatted to match YYYY-mm-dd"""
    )
    
    # The entity name field, which will hold the name of the entity that sends the notice email
    entity_name: str | None = Field(
        default=None,  # Default is None, so it's optional
        description="""The name of the entity sending the notice (if present in the message)"""
    )
    
    # The phone number of the entity that sent the notice
    entity_phone: str | None = Field(
        default=None,
        description="""The phone number of the entity sending the notice (if present in the message)"""
    )
    
    # The email of the entity sending the notice
    entity_email: str | None = Field(
        default=None,
        description="""The email of the entity sending the notice (if present in the message)"""
    )
    
    # The project ID - is an integer that should be found in the message
    project_id: int | None = Field(
        default=None,
        description="""The project ID (if present in the message) - must be an integer"""
    )
    
    # The location of the site for the project, like the full address
    site_location: str | None = Field(
        default=None,
        description="""The site location of the project (if present in the message). Use the full address if possible."""
    )
    
    # The type of violation indicated in the notice
    violation_type: str | None = Field(
        default=None,
        description="""The type of violation (if present in the message)"""
    )
    
    # The required changes the entity is asking for
    required_changes: str | None = Field(
        default=None,
        description="""The required changes specified by the entity (if present in the message)"""
    )
    
    # The string representation of the compliance deadline date, but like `date_of_notice_str`,
    # it won't be shown in the output or string representation.
    compliance_deadline_str: str | None = Field(
        default=None,
        exclude=True,  # Exclude this field from output
        repr=False,  # Don't print this field when displaying the object
        description="""The date that the company must comply (if any) reformatted to match YYYY-mm-dd"""
    )
    
    # The maximum potential fine the entity can face due to the violation
    max_potential_fine: float | None = Field(
        default=None,
        description="""The maximum potential fine (if any)"""
    )

    # A static method that helps to convert a string date into a Python date object
    @staticmethod
    def _convert_string_to_date(date_str: str | None) -> date | None:
        if date_str is None:
            return None  # If no date string is provided, return None
        try:
            # Try to parse the date string using the format YYYY-mm-dd
            return datetime.strptime(date_str, "%Y-%m-%d").date()
        except Exception as e:
            # If there's an error during conversion, print it and return None
            print(e)
            return None

    # A computed field, which means it will calculate dynamically the date_of_notice strings into Python date objects
    @computed_field
    def date_of_notice(self) -> date | None:
        # It converts the `date_of_notice_str` to a proper date object using the static method defined above
        return self._convert_string_to_date(self.date_of_notice_str)

    # Computed field for `compliance_deadline`
    @computed_field
    def compliance_deadline(self) -> date | None:
        # It converts the `compliance_deadline_str` to a proper date object using the static method defined above
        return self._convert_string_to_date(self.compliance_deadline_str)


# Define the email parsing chain using LangChain

# Create a prompt template using LangChain's `ChatPromptTemplate`
info_parse_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
            Parse the date of notice, sending entity name, sending entity
            phone, sending entity email, project id, site location,
            violation type, required changes, compliance deadline, and
            maximum potential fine from the message. If any of the fields
            aren't present, don't populate them. Try to cast dates into
            the YYYY-mm-dd format. Don't populate fields if they're not
            present in the message.

            Here's the notice message:

            {message}
            """,
        )
    ]
)

# Instantiate the ChatOpenAI model with GPT-4o-mini as the base model
# This is the LLM (Large Language Model) that will perform the extraction task
notice_parser_model = ChatOpenAI(model="gpt-4o-mini", temperature=0)

# Define the notice parsing chain using LangChain's Expression Language (LCEL)
NOTICE_PARSER_CHAIN = (
    info_parse_prompt  # The prompt template created earlier
    | notice_parser_model.with_structured_output(NoticeEmailExtract)  # Apply the model to generate structured output using the NoticeEmailExtract model
)
