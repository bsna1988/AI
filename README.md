# To run open-webui:
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

# Download confluence
- put confluence link and creds in .env file
- API token page https://id.atlassian.com/manage-profile/security/api-tokens
- `python download_confluence.py`

# Elastic
`docker pull docker.elastic.co/elasticsearch/elasticsearch:8.10.4`
`docker run -p 9200:9200 -e "discovery.type=single-node" -e "ES_JAVA_OPTS=-Xms1024m -Xmx1024m" -e "xpack.security.enabled=false" elasticsearch:8.18.4`


# Olama
`ollama pull zephyr:7b-alpha-q3_K_S`
https://docs.haystack.deepset.ai/docs/ollamachatgenerator
`pip install ollama-haystack`

# Pipelined
https://docs.openwebui.com/pipelines/
```
 docker run -d -p 9099:9099 --add-host=host.docker.internal:host-gateway -e PIPELINES_URLS="https://github.com/bsna1988/AI/blob/main/confluence_pipeline/haystack_pipeline.py" -v pipelines:/app/pipelines --name pipelines --restart always ghcr.io/open-webui/pipelines:main
```