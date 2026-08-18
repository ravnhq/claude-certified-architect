# Exercise 2.4 — Configure MCP Servers with Scoping and Environment Variables

**Difficulty:** Beginner · **Estimate:** 30 minutes
**Source:** https://claudecertificationguide.com/learn/2-tool-design-mcp/2-4-mcp-server-integration#build-exercise

#### Configure MCP Servers with Scoping and Environment Variables  ·  30 minutes
1. Create a .mcp.json file in your project root configuring a community MCP server (e.g. GitHub) with command and args
   *Why:* Project-level .mcp.json is version-controlled and shared with every team member who clones the repository. The exam tests whether you know that team-wide servers belong here, not in ~/.claude.json. Using community servers for standard integrations is always the correct first choice.
   **You should see:** A .mcp.json file at the project root containing an mcpServers object with at least one server entry specifying command (e.g. npx) and args (e.g. -y @modelcontextprotocol/server-github).
2. Use ${GITHUB_TOKEN} environment variable expansion for authentication credentials
   *Why:* Committing credentials directly in .mcp.json is a security risk the exam penalises. The ${VARIABLE_NAME} syntax lets the configuration file reference environment variables without containing the actual values, keeping secrets out of repository history.
   **You should see:** The env section of your server configuration contains ${GITHUB_TOKEN} (not an actual token value). Running git diff confirms no secrets are staged for commit. Each developer sets their own token locally.
3. Add a personal or experimental MCP server to ~/.claude.json for user-level configuration
   *Why:* User-level configuration in ~/.claude.json is personal, not version-controlled, and not shared with teammates. The exam tests whether you know the scoping hierarchy: .mcp.json for team servers, ~/.claude.json for personal or experimental servers.
   **You should see:** A ~/.claude.json file with an mcpServers entry for a personal server (e.g. an experimental integration you are testing). This file is NOT in your project repository and NOT in version control.
4. Expose a content catalogue (e.g. a documentation hierarchy or database schema) as an MCP resource
   *Why:* MCP resources give agents visibility into available data without requiring exploratory tool calls. Without resources, an agent might call list_tables then describe_table for every table, wasting multiple tool calls. A schema resource makes that information available immediately.
   **You should see:** An MCP resource definition that exposes structured data (e.g. a list of database tables with column types, or a documentation table of contents) accessible at a URI like db://schema/main. The resource should have a name, description, and mimeType.
5. Enhance the tool descriptions for your configured MCP server to explain capabilities and outputs in detail, preventing the agent from preferring built-in tools
   *Why:* When an MCP tool has a sparse description, the agent prefers built-in tools like Grep because their descriptions are richer and more detailed. The exam tests whether you know that enhanced MCP descriptions are required to compete with built-in tools for selection priority.
   **You should see:** Tool descriptions that are 3-5 sentences long, explaining what the tool does, what it returns, when to use it, and how it compares to built-in alternatives. For example, a search_codebase tool description that explicitly states it is more accurate than Grep for semantic searches.
