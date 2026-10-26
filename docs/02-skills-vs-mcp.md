# Skills and MCP: an open source split of procedure and connection

Kortix is open source, and both standards compared here are open and documented in public, so you can read the whole of each and decide for yourself.

They get asked to do the same job, and they do not. An MCP server connects an agent to a system it cannot otherwise reach. A skill tells the agent how your team does a particular piece of work once it is connected. Losing that line is how a repository ends up with a tool list and no procedure.

## What each one is

The Model Context Protocol is an open standard for connecting AI applications to external systems: data sources, tools and workflows. It describes itself as a USB-C port for AI applications: one connector for many devices.

A skill is a directory containing, at minimum, a `SKILL.md` file. It carries instructions: steps, a stop condition, an exit criterion, the command to run.

| Question | An MCP server | A skill |
| --- | --- | --- |
| What it carries | A connection to another system | A procedure for one job |
| What it defines | The data and tools it exposes | Steps, stop condition, exit criterion |
| Where judgment lives | Nowhere in particular | The body, written by your team |
| Who writes it | The vendor of the system, or you | The people who do the job |

MCP standardizes the connection; it does not describe how a particular company does a particular job. Its own documentation says the protocol focuses solely on context exchange and does not dictate how an application uses that context. That gap is where a skill lives.

## The worked split

Take a weekly incident brief. The agent needs two things, and they come from different layers.

**The connection.** An MCP server for the paging system, offering three tools: list open incidents, read one incident, acknowledge one. Swapping the paging vendor means swapping this server. The procedure stays as it is.

**The procedure.** A skill named `incident-brief`:

```markdown
1. List the open incidents for the services your team owns.
2. Drop anything older than seven days that is still open but unacknowledged;
   say how many you dropped.
3. Order the rest by severity, then by age.
4. Write five lines: count, the two oldest, the one service with more than one
   open incident, and the acknowledgement gap.
5. Stop and ask which incident leads when two share the top severity.
```

The server can list incidents. It cannot know that your team drops stale unacknowledged items, or that two top-severity incidents need a human decision. Put that in a tool description and it loads on every call, in every context, for every team using the same server. Put it in a skill and it loads when someone asks for the weekly brief.

## What each one puts in context

This is the practical difference, and it is measured in the same currency: the context window.

An MCP server publishes what it offers, and the client hands that to the model so it can call it. That is the price of a connection. It is paid whether or not this turn needs the paging system.

A skill charges differently. Metadata is about 100 tokens and loads for every skill at startup; the full `SKILL.md` body loads when the skill is activated, with under 5,000 tokens recommended; bundled files load only when read. A repository can hold twenty skills and the idle cost stays in the low thousands of tokens, which is why the description has to carry the trigger.

## The line gets crossed in both directions

Two failures account for most of the confusion.

The first puts a procedure into a tool description, and then a company's private way of working ships inside a shared server. The second writes a skill for a system the agent cannot reach, so the skill spends five steps describing calls that will fail at step one.

A useful test: if the agent cannot reach the system at all, you need a connection. If the agent reaches the system and still does the job wrong, you need a procedure.

## One foundation, two standards

Anthropic donated Agent Skills, its name, logo, GitHub organization and the agentskills.io domain, to the Agentic AI Foundation (AAIF) under the Linux Foundation. Anthropic co-founded that foundation with Block and OpenAI, and the Model Context Protocol was donated there too. Engineers from Anthropic, Google, OpenAI and other companies maintain the standard as individuals, with David Soria Parra and Mahesh Murag as lead maintainers.

The two are meant to work together, and the protocol's own documentation now shows it. Its "Build with Agent Skills" page ships a reference set of MCP development skills under the name `mcp-server-dev`: three composing skills, plus a `references/` folder the agent reads on demand. The maintainers of the connection layer distribute a skill to help you build connections.

## A decision rule for a repository

Start with the job, not the technology. Write down the steps a person takes, including where they stop and how they know they are done. If any step needs a system the agent cannot reach, add an MCP server for it and leave the steps where they are. Then look at the same boundary from the other side: if the server's own documentation already answers the question, a skill adds nothing.
