# Customer Support Automation Project

## Project Overview

This project shows how a customer support system can work from start to finish.

First, customer support data is cleaned using Python and imported into Jira. Jira is then used to manage the tickets through different stages, with automations for things like routing, due dates and overdue tickets.

For new customer enquiries, the details are added to an Excel file. Python reads the new rows and creates Jira tickets automatically. Once a ticket is created, Make sends the customer a confirmation email through Gmail.

Finally, Jira data is exported into Tableau to create a dashboard showing things like ticket status, priority, support queues and ticket types.


## Project Phases

### [Phase 1](phase_1.md) – Dataset Preparation
Clean and prepare the customer support dataset using Python and Pandas.

### Phase 2 – Jira Project Setup
Import the historical customer support tickets into Jira and set up the required fields.

### Phase 3 – Jira Workflow Design
Create a structured workflow to manage tickets through each stage of the support process.

### Phase 4 – Jira Internal Automation
Create automations for triage, routing, workload management, due dates, overdue tickets and closure.

### Phase 5 – Excel to Jira Automation Using Python
Use Python and the Jira REST API to create new Jira tickets from a live customer intake file.

### Phase 6 – Jira and Gmail Integration Using Make
Connect Jira with Gmail through Make and automatically send ticket creation confirmation emails to customers.

### Phase 7 – Tableau Dashboard
Build a Tableau dashboard to analyse ticket status, priority, support queues, ticket types and overall support activity.


## Final Dashboard


<img width="1381" height="762" alt="Screenshot 2026-08-31 at 10 17 34 PM" src="https://github.com/user-attachments/assets/1d180a2a-6ddc-4243-a201-51e34ddb6c0e" />

