# NASA PDS Registry MCP Server

A Model Context Protocol (MCP) server that provides access to the NASA Planetary Data System (PDS) Registry API using FastMCP.

## Overview

This MCP server enables human-in-the-loop agentic search and exploration of NASA PDS data products, bundles, and collections through a simple interface. It directly integrates with the [NASA PDS Registry API](https://nasa-pds.github.io/pds-api/).

By open-sourcing this MCP server, we aim to support the researchers of the Planetary Data Science community by making it easier to access NASA PDS data. Our goal is to provide enhanced search capabilities that enable more effective data exploration and improve accessibility for future research endeavors.

## Features

- **Mission & Project Search**: Find space missions, investigations, and research projects with filtering by keywords and mission types
- **Celestial Body Discovery**: Search for planets, moons, asteroids, comets, and other astronomical targets by name or type
- **Spacecraft & Platform Search**: Locate spacecraft, rovers, landers, telescopes, and other instrument-carrying platforms
- **Scientific Instrument Lookup**: Find cameras, spectrometers, detectors, and other scientific instruments used in space missions
- **Data Collection Exploration**: Search and filter data collections by mission, target, instrument, or spacecraft relationships
- **Product Relationship Mapping**: Discover connections between missions, targets, instruments, and data products
- **Detailed Product Information**: Retrieve comprehensive metadata and details for specific PDS products using URN identifiers
- **Reference Data Access**: Access categorized lists of target types, spacecraft types, instrument types, and mission types for filtering and discovery

### Example Conversation

1. Which instrument do seismic observations in the PDS?
2. What is the identifier of the moon in the PDS?
3. What data is collected from these instruments are targeting the Moon? (include URNs if need be)?
4. What missions produced these observations?

## Installation

1. Clone this repository:

```bash
git clone https://github.com/NASA-PDS/pds-mcp.git
cd pds-mcp
```

2. Install dependencies:

```bash
python3.13 -m venv {env-name}
source pds-env/bin/activate
pip install -r requirements.txt
```
Requires Python 3.13+.

## Usage

### Running the Server

```bash
python3.13 pds_mcp_server.py
```

### MCP Client Configuration

Add this to your MCP client configuration (e.g., Claude Desktop):

```json
{
  "mcpServers": {
    "pds-registry": {
      "command": "/path/to/{env-name}/bin/python3.13",
      "args": ["/path/to/pds_mcp_server.py"],
      "env": {}
    }
  }
}
```

### System Prompt

We recommend using this system prompt in your MCP Client:

```
You are only allowed to make one tool call per request. In the returned search results, output the URNs (identifiers) as additional information alongside the result. After each message, you will propose to the user what next steps they can take and ask them to choose.
```

This will prevent the MCP server from uncontrollably making API calls of its own volition, allowing the user to control how they want to search through the NASA Planetary Data System.

## Development

### MCP Inspector (Debugging)

```bash
npx @modelcontextprotocol/inspector python src/main.py
```

More on MCP Inspector [here](https://modelcontextprotocol.io/legacy/tools/inspector).

### Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For issues related to:

- **PDS Registry API**: Contact pds-operator@jpl.nasa.gov or open an issue [here](https://github.com/NASA-PDS/pds-api)
- **This MCP Server**: Open an issue in this repository
- **MCP Protocol**: Check the [MCP documentation](https://modelcontextprotocol.io/) or [FastMCP documentation](https://gofastmcp.com/getting-started/welcome)

## Other Resources

- [PDS API Swagger OAS](https://pds.mcp.nasa.gov/api/search/1/swagger-ui/index.html)
