Phase 1 - Data Preparation

# Objective

The objective of Phase 1 was to prepare a customer support dataset from Kaggle for use in Jira.The dataset was cleaned using Python and Pandas so that it could be imported into Jira in a structured and consistent format.

# Original Dataset

The original dataset contained 4,000 customer support tickets in multiple languages.

The main fields included:

Subject
Customer message
Agent response
Ticket type
Support queue
Priority
Language
Business type
Multiple tag columns
Cleaning Steps

# Cleaning

1. Filtered the Dataset to English Only

Only tickets where the language was en were retained.
This reduced the dataset from 4,000 tickets to 1,391 English-language tickets.

2. Standardised Business Type

Similar business categories were grouped together.

Examples:

IT Consulting Firm → IT Services
IT Consulting Service → IT Services
Tech Online Store → Online Store

Other inconsistent business type values were also reviewed and standardised where appropriate.

3. Reviewed Missing Values

Missing values were checked across all columns. 
Tickets were retained where the customer subject was missing, as customers may submit support requests without including a subject.
No tickets were found where both the customer subject and customer message were missing.
For the ticket where the customer message was missing, the priority was changed to low because there was insufficient information to treat it as a higher-priority ticket.

4. Cleaned Tag Fields

The original dataset contained tag columns from tag_1 to tag_9.
tag_9 was removed because it contained no values.
The remaining tag columns were combined into one Tags field to make the dataset more suitable for Jira.
Duplicate tags within the same ticket were removed when combining the fields.

5. Added Ticket Numbers

A sequential ticket number was added so that each record has a simple identifier beginning from 1.

6. Renamed Columns

The dataset columns were renamed to make them clearer and more suitable for Jira.

Examples:

subject → Customer Subject
body → Customer Message
answer → Agent Response
type → Ticket Type
queue → Support Queue
priority → Priority
business_type → Business Type
combined tag fields → Tags
Final Dataset

The cleaned dataset contains English-language customer support tickets prepared for import into Jira.

# The final fields include:

Ticket ID
Customer Subject
Customer Message
Agent Response
Ticket Type
Support Queue
Priority
Business Type
Tags
Output

The cleaned dataset was saved as a CSV file and uploaded to the GitHub repository.

The Pandas cleaning script is also stored in the repository so that the transformation process can be reproduced.
