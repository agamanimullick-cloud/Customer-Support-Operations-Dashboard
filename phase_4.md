# Phase 4 - Jira Internal Automation

## Automations

### 1. New Ticket to Triage

Tickets remain in `New Ticket` for 5 hours.

If the ticket has a customer message, it is automatically moved to `Triage`.

JQL:

```text
status = "New Ticket"
AND created <= -5h
AND description IS NOT EMPTY
```

Action:

`New Ticket → Triage`

---

### 2. Missing Customer Message

If the customer message field is empty, it is moved to `Waiting for Customer`.

JQL:

```text
status = "New Ticket"
AND description IS EMPTY
```

Action:

`New Ticket → Waiting for Customer`

---

### 3. Priority-Based Due Dates

The due date begins when a ticket enters `Assigned`.

* **High Priority** → 1 day
* **Medium Priority** → 3 days
* **Low Priority** → 5 days

Smart values used:

```text
{{now.plusDays(1).jiraDate}}
{{now.plusDays(3).jiraDate}}
{{now.plusDays(5).jiraDate}}
```

---

### 4. Overdue Ticket Handling

Jira checks every 5 hours for tickets that have passed their due date and are not resolved or closed.

JQL:

```text
duedate < now()
AND status NOT IN ("Resolved Ticket", "Closed")
```

Action:

**Flag the ticket**

---

### 5. Automatic Ticket Closure

Resolved tickets are automatically closed if they remain in `Resolved Ticket` for more than 7 days.

JQL:

```text
status = "Resolved Ticket"
AND status CHANGED TO "Resolved Ticket" BEFORE -7d
```

Action:

`Resolved Ticket → Closed`

---

### 6. Support Team Capacity Management

Each support team can have a maximum of **10 tickets in `In Progress`**.

Only tickets in `In Progress` count towards capacity.

Tickets in `Waiting for Customer`, `Resolved Ticket`, `Closed`, `Triage`, or `New Ticket` do not count.

The first capacity rule was created for **Technical Support**.

The automation:

1. Counts Technical Support tickets in `In Progress`
2. Continues only if the count is below 10
3. Finds Technical Support tickets waiting in `Triage`
4. Prioritises higher-priority tickets first
5. Uses the oldest ticket first when priorities are equal
6. Assigns the selected ticket
7. Moves it through `Assigned` to `In Progress`

Active ticket lookup:

```text
"Support Queue" = "Technical Support"
AND status = "In Progress"
```

Capacity check:

```text
{{activeCount}} < 10
```

Triage lookup:

```text
"Support Queue" = "Technical Support"
AND status = "Triage"
ORDER BY priority DESC, created ASC
```

The first eligible ticket is selected using:

```text
{{lookupIssues.first.key}}
```

The rule runs every 10 minutes and adds one ticket at a time until the team reaches its maximum active workload of 10.

If a ticket leaves `In Progress`, another ticket can be allocated from Triage.

