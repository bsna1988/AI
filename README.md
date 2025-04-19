To run open-webui:
`open-webui serve`
Open
http://localhost:8080/

How to install mcp in open-webui
https://docs.openwebui.com/openapi-servers/mcp/

You can easily run the recommended MCP server directly through the MCP-to-OpenAPI proxy (mcpo) like this:
`uvx mcpo --port 8000 -- java -Dspring.ai.mcp.server.stdio=true -Dspring.main.web-application-type=none -Dlogging.pattern.console= -jar /Users/sasha/AI/mcp-github/target/mcp-github-0.0.1-SNAPSHOT.jar`