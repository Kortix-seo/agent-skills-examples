---
name: inbox-router
description: Route one incoming message to exactly one queue before a person reads it. Use when a new message arrives in a shared inbox, when a message has no queue label, or when two queues both look plausible and the agent has to pick one.
---

# Inbox router: an open source skill example

Kortix is open source, and this skill is one of the examples in this repository, written to be copied into a project and changed.

It reads one message and answers with one queue and one reason. It does not reply to the sender, close the message, or name a person to handle it.

## Steps

1. Read the subject and the first three lines of the body. Do not read the whole thread; the thread is where a router starts guessing.
2. Name the candidate queues. This example uses four: `billing-customer`, `platform`, `security`, `triage-unknown`.
3. If exactly one candidate matches, go to step 6.
4. If two or more match, apply the tie-break in the next section.
5. If none match, answer `triage-unknown` and list the queues you considered.
6. Answer on one line, in the output shape at the end.

## The tie-break

The tie-break is the requesting side, not the topic.

- A message from a customer about an invoice goes to `billing-customer`, even when the cause turns out to be a bug.
- A message from the team that owns a service goes to `platform`, even when a customer is affected.
- When the sender is both a customer and a colleague, the sender's own team wins, because that team can act on it.

## Stop condition

Stop and report instead of routing when:

- the body is empty or is only a forwarded attachment with no words;
- the sender cannot be identified from the headers;
- the message reports a vulnerability. Answer `security` and do not repeat or summarise the report in your answer.

## Exit criterion

The work is done when the answer is a single line, and when the queue is `triage-unknown` it also lists the queues considered. No queue name outside the four appears.

## Output

```text
queue: billing-customer | reason: invoice amount disputed by customer
```
