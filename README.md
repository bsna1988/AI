To run open-webui:
`open-webui serve`
Open
http://localhost:8080/

How to install mcp in open-webui
https://docs.openwebui.com/openapi-servers/mcp/

You can easily run the recommended MCP server directly through the MCP-to-OpenAPI proxy (mcpo) like this:
`uvx mcpo --port 8000 -- java -Dspring.ai.mcp.server.stdio=true -Dspring.main.web-application-type=none -Dlogging.pattern.console= -jar /Users/sasha/AI/mcp-servers/mcp-github/target/mcp-github-0.0.1-SNAPSHOT.jar`

To run github-mcp-server
`export GITHUB_PERSONAL_ACCESS_TOKEN=`
`uvx mcpo --port 8000 -- docker run -i --rm -e GITHUB_PERSONAL_ACCESS_TOKEN ghcr.io/github/github-mcp-server`

To run [mcp-attlasian|https://github.com/sooperset/mcp-atlassian]
`uvx mcpo --port 8000 -- docker run -i --rm --env-file /Users/sasha/AI/env.properties ghcr.io/sooperset/mcp-atlassian:latest`