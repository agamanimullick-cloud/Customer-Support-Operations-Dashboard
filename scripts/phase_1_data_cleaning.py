import pandas as pd

# Load dataset
df = pd.read_csv("../data/raw/dataset-tickets-multi-lang3-4k.csv")

# Keep English tickets only
data1 = df[df['language'] == 'en'].copy()

# Standardise business types
data1['business_type'] = data1['business_type'].replace({
    'IT Consulting Firm': 'IT Services',
    'IT Consulting Service': 'IT Services',
    'Tech Online Store': 'Online Store',
    'Adobe Photoshop 2024': 'IT Services'
})

# Remove empty tag column
data1 = data1.drop(columns=['tag_9'])

# Combine tag columns
tag_cols = [
    'tag_1', 'tag_2', 'tag_3', 'tag_4',
    'tag_5', 'tag_6', 'tag_7', 'tag_8'
]

data1['tags'] = data1[tag_cols].apply(
    lambda x: ', '.join(pd.unique(x.dropna().astype(str))),
    axis=1
)

# Remove original tag columns
data1 = data1.drop(columns=tag_cols)

# Lower priority where customer message is missing
data1.loc[data1['body'].isnull(), 'priority'] = 'low'

# Add ticket numbering
data1.insert(0, 'Ticket ID', range(1, len(data1) + 1))

# Rename columns
data1 = data1.rename(columns={
    'subject': 'Customer Subject',
    'body': 'Customer Message',
    'answer': 'Agent Response',
    'type': 'Ticket Type',
    'queue': 'Support Queue',
    'priority': 'Priority',
    'business_type': 'Business Type',
    'tags': 'Tags'
})

# Export cleaned dataset
data1.to_csv(
    "../data/cleaned/jira_support_tickets.csv",
    index=False
)
