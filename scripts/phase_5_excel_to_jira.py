JIRA_URL = "https://practisejira.atlassian.net"
JIRA_EMAIL = "agamanimullick@gmail.com"
JIRA_API_TOKEN = "ATATT3xFfGF0e2uei5m2bzAFWQywhKoRJWbSUdDzvtptV0LVPjc3v1-PkGacQTaoheT6jul-TMnXJGXFDrJbdypXH6z2BRE06vyjas5xSejY4mNwcZUb3d7gO32kqRCXCEUuHOctFuBrAXPjRNszeU9PVAa6srxwgLjBSqPqBO1FTpBFK2INWOw=1D23C98F"

import requests
import pandas as pd
from requests.auth import HTTPBasicAuth

url = f"{JIRA_URL}/rest/api/3/issue"

auth = HTTPBasicAuth(JIRA_EMAIL, JIRA_API_TOKEN)

headers = {
    "Accept": "application/json",
    "Content-Type": "application/json"
}

payload = {
    "fields": {
        "project": {
            "key": "P1"
        },
        "summary": "Python API test ticket",
        "issuetype": {
            "name": "Task"
        }
    }
}

response = requests.post(
    url,
    headers=headers,
    auth=auth,
    json=payload
)

print(response.status_code)
print(response.text)

df = pd.read_csv("live_customer_enquiries.csv")
df.head()


new_rows = df[df['Ticket ID'] > 1391]

#Some Jira fields are built-in, so we usually don’t need to look up a custom-field ID for them:

#Summary → Jira summary
#Customer Message → Jira description
#Priority → Jira priority
#Tags → usually Jira labels if we want them there
#work item type → Jira issuetype
#project → Jira project

#The fields we need to look up are the custom fields you created


fields_url = f"{JIRA_URL}/rest/api/3/field"

response = requests.get(
    fields_url,
    auth=HTTPBasicAuth(JIRA_EMAIL, JIRA_API_TOKEN),
    headers={"Accept": "application/json"}
)

fields = response.json()

wanted_fields = [
    "Ticket ID",
    "Customer Subject",
    "Agent Response",
    "Ticket Type",
    "Support Queue",
    "Business Type",
    "Email ID"
]

for field in fields:
    if field["name"] in wanted_fields:
        print(field["name"], "->", field["id"])


custom_ids = [
    "customfield_10050",  # Ticket ID
    "customfield_10051",  # Business Type
    "customfield_10081",  # Agent Response
    "customfield_10049",  # Customer Subject
    "customfield_10080",  # Email ID
    "customfield_10047",  # Ticket Type
    "customfield_10048"   # Support Queue
]

for field in fields:
    if field["id"] in custom_ids:
        print(
            field["name"],
            "->",
            field["id"],
            "->",
            field.get("schema")
        )

df = pd.read_csv("live_customer_enquiries.csv")
df.head()

if "Jira Key" not in df.columns:
    df["Jira Key"] = pd.NA

new_rows = df[
    (df["Ticket ID"] > 1391) &
    (df["Jira Key"].isna())
]

new_rows

def text_value(value):
    if pd.isna(value):
        return ""
    return str(value)


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


def make_labels(value):
    if pd.isna(value):
        return []

    return [
        tag.strip().replace(" ", "-")
        for tag in str(value).split(",")
        if tag.strip()
    ]


## 3 Run this to create jira tickets


df = pd.read_csv("live_customer_enquiries.csv")


# This line saying if the jira key is empty in the excel sheet it must be a new entry.
new_rows = df[
    df["Jira Key"].isna()
]

# This loop creates the jira tickets
url = f"{JIRA_URL}/rest/api/3/issue"

auth = HTTPBasicAuth(JIRA_EMAIL, JIRA_API_TOKEN)

headers = {
    "Accept": "application/json",
    "Content-Type": "application/json"
}

for index, row in new_rows.iterrows():

    fields_payload = {
        "project": {
            "key": "P1"
        },

        "issuetype": {
            "name": "Task"
        },

        "summary": text_value(row["Summary"]),

        "description": make_description(row["Customer Message"]),

        "priority": {
            "name": str(row["Priority"]).capitalize()
        },

        "labels": make_labels(row["Tags"]),

        "customfield_10050": int(row["Ticket ID"]),

        "customfield_10051": {
            "value": text_value(row["Business Type"])
        },

        "customfield_10081": make_description(row["Agent Response"]),

        "customfield_10049": text_value(row["Customer Subject"]),

        "customfield_10080": text_value(row["Email"]),

        "customfield_10047": {
            "value": text_value(row["Ticket Type"])
        },

        "customfield_10048": {
            "value": text_value(row["Support Queue"])
        }
    }

    payload = {
        "fields": fields_payload
    }

    response = requests.post(
        url,
        headers=headers,
        auth=auth,
        json=payload
    )

    if response.status_code == 201:
        jira_key = response.json()["key"]

        df.loc[index, "Jira Key"] = jira_key

        print(
            f"Ticket {row['Ticket ID']} created successfully: {jira_key}"
        )

    else:
        print(
            f"Failed to create Ticket {row['Ticket ID']}"
        )

        print(response.status_code)
        print(response.text)



# This updates the excel sheet with the jira_key of the new entries

df.to_csv("live_customer_enquiries.csv", index=False)
