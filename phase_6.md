# Phase 6 – Automated Ticket Confirmation Email

## Overview

Phase 6 adds an automated customer confirmation email after a new Jira ticket is created.


## Make Scenario

The scenario uses:

```text
Jira Cloud Platform → Watch Issues
```

The Jira trigger is configured using:

```text
By Created Time
```

The JQL query is:

```jql
project = P1
AND "Email ID" IS NOT EMPTY
```
The Gmail module then sends the confirmation email to the value stored in the Jira `Email ID` field.

## Email Content

The confirmation email includes:

```text
Subject: Support Ticket Created - P1-1423

Hi,

Thank you for contacting us. Your support request has been received and a ticket has been created.

Ticket Reference: P1-1423
Subject: Unable to access account

Our support team will review your request and get back to you as soon as possible.

Kind regards,
Customer Support Team
```

The Jira Key and Summary are inserted dynamically by Make.

## Scheduling

The Make scenario can be scheduled to run every 15 minutes.

For live use, the starting point is set to:

```text
From now on
```
