# Phase 5 – Automated Customer Intake: Excel to Jira Using Python

## Overview

The objective of Phase 5 was to automate the creation of new Jira customer-support tickets from a live customer enquiry file using Python and the Jira REST API.

The historical customer-support dataset containing **Ticket IDs 1–1391** had already been imported into Jira during the earlier phases of the project.

A separate live customer intake dataset was therefore created starting from **Ticket ID 1392**.

The final integration follows this process:

```text
Live Customer Enquiry File
        ↓
Python / Pandas
        ↓
Jira REST API
        ↓
Jira Ticket Created
        ↓
Jira Key Returned
        ↓
Jira Key Stored Against Customer Record
        ↓
Existing Jira Workflow & Automations
```

This allows new customer enquiries to be transferred into Jira without manually recreating each ticket.

---

## Objectives

The objectives of this phase were to:

- Simulate a live customer-support intake process
- Detect new customer enquiries
- Create Jira tickets automatically using Python
- Transfer customer information into the correct Jira fields
- Preserve the original internal Ticket ID
- Retrieve the Jira-generated issue key
- Prevent duplicate ticket creation

---

## Jira API Connection

Python was connected directly to Jira using the Jira REST API.

The Jira Cloud base URL was:

```python
JIRA_URL = "https://practisejira.atlassian.net"
```

The endpoint used to create Jira work items was:

```python
url = f"{JIRA_URL}/rest/api/3/issue"
```

Authentication was performed using the Atlassian account email and an API token.

```python
from requests.auth import HTTPBasicAuth

auth = HTTPBasicAuth(
    JIRA_EMAIL,
    JIRA_API_TOKEN
)
```

A simple test ticket was created first to confirm that the API connection was working.

A successful Jira creation request returns:

```text
HTTP 201 Created
```

---

## Loading the Live Dataset

The live customer enquiry file was loaded using Pandas.

```python
import pandas as pd

df = pd.read_csv("live_customer_enquiries.csv")
```

The dataset was inspected using:

```python
df.head()
```

A `Jira Key` column was also added if one did not already exist.

```python
if "Jira Key" not in df.columns:
    df["Jira Key"] = pd.NA
```

---

## Detecting New Customer Enquiries

Only new customer enquiries should be sent to Jira.

The historical dataset ended at Ticket ID 1391, so the following condition was used:

```python
new_rows = df[
    (df["Ticket ID"] > 1391) &
    (df["Jira Key"].isna())
]
```

A customer enquiry therefore qualifies as new when:

1. Its Ticket ID is greater than 1391
2. Its Jira Key is still empty

This also helps prevent the same enquiry from being created multiple times.

---

## Jira Custom Field Identification

Several dataset fields were stored as custom fields in Jira.

Jira's REST API requires the internal custom field ID rather than the visible field name.

The Jira field endpoint was queried using:

```python
fields_url = f"{JIRA_URL}/rest/api/3/field"

response = requests.get(
    fields_url,
    auth=HTTPBasicAuth(JIRA_EMAIL, JIRA_API_TOKEN),
    headers={"Accept": "application/json"}
)

fields = response.json()
```

The relevant field IDs were identified as:

| Jira Field | API Field ID |
|---|---|
| Ticket ID | `customfield_10050` |
| Business Type | `customfield_10051` |
| Customer Subject | `customfield_10049` |
| Email ID | `customfield_10080` |
| Ticket Type | `customfield_10047` |
| Support Queue | `customfield_10048` |
| Agent Response | `customfield_10081` |

---

## Jira Field Types

The Jira field schemas were also checked because different field types require different JSON structures.

### Number Field

Ticket ID was stored as a numeric field:

```python
"customfield_10050": int(row["Ticket ID"])
```

### Single-Select Fields

Business Type:

```python
"customfield_10051": {
    "value": text_value(row["Business Type"])
}
```

Ticket Type:

```python
"customfield_10047": {
    "value": text_value(row["Ticket Type"])
}
```

Support Queue:

```python
"customfield_10048": {
    "value": text_value(row["Support Queue"])
}
```

### Standard Text Fields

Customer Subject:

```python
"customfield_10049": text_value(
    row["Customer Subject"]
)
```

Customer Email:

```python
"customfield_10080": text_value(
    row["Email"]
)
```

---

## Handling Missing Values

Some fields in customer-support data can be blank.

A helper function was created to prevent Pandas `NaN` values from being passed directly to Jira.

```python
def text_value(value):
    if pd.isna(value):
        return ""
    return str(value)
```

This converts missing values into empty strings while leaving valid values unchanged.

---

## Atlassian Document Format

Jira REST API v3 requires rich-text fields such as Description and paragraph fields to use **Atlassian Document Format (ADF)**.

A helper function was created to convert normal text into the required format.

```python
def make_description(value):
    return {
        "type": "doc",
        "version": 1,
        "content": [
            {
                "type": "paragraph",
                "content": [
                    {
                        "type": "text",
                        "text": text_value(value)
                    }
                ]
            }
        ]
    }
```

The customer message was then sent to Jira using:

```python
"description": make_description(
    row["Customer Message"]
)
```

The same conversion was used for the long-text Agent Response field:

```python
"customfield_10081": make_description(
    row["Agent Response"]
)
```

---

## Converting Tags into Jira Labels

The dataset contained multiple tags stored as comma-separated values.

For example:

```text
login issue, password reset, account access
```

A helper function was created to convert them into valid Jira labels.

```python
def make_labels(value):

    if pd.isna(value):
        return []

    return [
        tag.strip().replace(" ", "-")
        for tag in str(value).split(",")
        if tag.strip()
    ]
```

For example:

```text
login issue, password reset
```

becomes:

```python
[
    "login-issue",
    "password-reset"
]
```

---

## Dataset to Jira Mapping

The live dataset was mapped into Jira as follows:

| Dataset Field | Jira Field |
|---|---|
| Summary | Summary |
| Customer Message | Description |
| Priority | Priority |
| Tags | Labels |
| Ticket ID | Ticket ID |
| Customer Subject | Customer Subject |
| Agent Response | Agent Response |
| Ticket Type | Ticket Type |
| Support Queue | Support Queue |
| Business Type | Business Type |
| Email | Email ID |

All customer enquiries were created as Jira:

```text
Task
```

inside project:

```text
P1
```

The Jira workflow automatically placed new tickets into:

```text
New Ticket
```

---

## Creating Jira Tickets

The script loops through every new customer enquiry.

```python
for index, row in new_rows.iterrows():
```

A Jira payload is created for each row.

```python
fields_payload = {

    "project": {
        "key": "P1"
    },

    "issuetype": {
        "name": "Task"
    },

    "summary": text_value(
        row["Summary"]
    ),

    "description": make_description(
        row["Customer Message"]
    ),

    "priority": {
        "name": str(
            row["Priority"]
        ).capitalize()
    },

    "labels": make_labels(
        row["Tags"]
    ),

    "customfield_10050":
        int(row["Ticket ID"]),

    "customfield_10051": {
        "value": text_value(
            row["Business Type"]
        )
    },

    "customfield_10081":
        make_description(
            row["Agent Response"]
        ),

    "customfield_10049":
        text_value(
            row["Customer Subject"]
        ),

    "customfield_10080":
        text_value(
            row["Email"]
        ),

    "customfield_10047": {
        "value": text_value(
            row["Ticket Type"]
        )
    },

    "customfield_10048": {
        "value": text_value(
            row["Support Queue"]
        )
    }
}
```

The payload is then submitted to Jira.

```python
response = requests.post(
    url,
    headers=headers,
    auth=auth,
    json={"fields": fields_payload}
)
```

---

## Recording the Jira Key

When Jira successfully creates a ticket, the API returns status code:

```text
201
```

The Jira-generated issue key is retrieved using:

```python
jira_key = response.json()["key"]
```

The Jira Key is then stored against the original customer record.

```python
df.loc[index, "Jira Key"] = jira_key
```

Example:

| Ticket ID | Jira Key |
|---:|---|
| 1392 | P1-1395 |
| 1393 | P1-1396 |
| 1394 | P1-1397 |
| 1395 | P1-1398 |

The Ticket ID and Jira Key do not need to contain the same number.

The Ticket ID is the identifier used by the intake dataset, while the Jira Key is generated independently by Jira.

---

## Duplicate Prevention

The `Jira Key` field also provides a simple duplicate-prevention mechanism.

Only rows where:

```python
df["Jira Key"].isna()
```

are selected.

Once a Jira ticket is successfully created, its Jira Key is stored in the live dataset.

When the script runs again, records that already contain Jira Keys are ignored.

---

## Saving the Updated Dataset

After ticket creation, the updated dataset is saved.

```python
df.to_csv(
    "live_customer_enquiries.csv",
    index=False
)
```

This means that the relationship between the original customer enquiry and the Jira ticket is retained.

---

## Error Handling

The Jira API response is checked after every request.

For successful requests:

```python
if response.status_code == 201:

    jira_key = response.json()["key"]

    df.loc[index, "Jira Key"] = jira_key

    print(
        f"Ticket {row['Ticket ID']} "
        f"created successfully: {jira_key}"
    )
```

For unsuccessful requests:

```python
else:

    print(
        f"Failed to create Ticket "
        f"{row['Ticket ID']}"
    )

    print(response.status_code)
    print(response.text)
```

This made it possible to identify configuration and field-formatting problems directly from Jira.

---

## Final Test Result

The final Python integration successfully created all new customer enquiries.

Live dataset:

```text
Ticket ID 1392 – 1419
```

Total tickets created:

```text
28
```

Generated Jira keys:

```text
P1-1395 – P1-1422
```

Example output:

```text
Ticket 1392 created successfully: P1-1395
Ticket 1393 created successfully: P1-1396
Ticket 1394 created successfully: P1-1397
...
Ticket 1418 created successfully: P1-1421
Ticket 1419 created successfully: P1-1422
```

This confirmed that the complete Python-to-Jira integration was working successfully.

---

## Future Improvements

Potential future improvements include:

- Schedule the Python script twice daily using GitHub Actions
- Automatically generate ticket summaries using an AI API
- Send automatic customer confirmation emails when tickets are created

---
