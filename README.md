# NASA PDS Registry MCP Server

A Model Context Protocol (MCP) server that provides access to the NASA Planetary Data System (PDS) Registry API using FastMCP.

<img width="512" height="322" alt="image" src="https://github.com/user-attachments/assets/55d3b3ce-2ac2-4359-a23f-1b1d55efd648" />


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
git clone https://github.com/NASA-PDS/pds-mcp-server.git
cd pds-mcp-server
```

2. Install dependencies:

Requires Python 3.13+.

```bash
python3.13 -m venv {env-name}
source {env-name}/bin/activate
pip install -r requirements.txt
```

## Usage

We propose 3 usage for the PDS MCP services:
- Standalone server
- Integrated with a 3rd party client software or application (Claude Desktop, gradio, ...)



### Running the Server Standalone

If you need to expose the MCP tools as a server, you can run it, standalone, as follows:

```bash
python3.13 pds_mcp_server.py
```

### Integrated with MCP client software 

The MCP tool can be integrated in a client like, Claude Desktop or Custom MCP client.

#### MCP Client Configuration

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

#### Specific instructions

We recommend using this system prompt in your MCP Client:

```
You are only allowed to make one tool call per request. In the returned search results, output the URNs (identifiers) as additional information alongside the result. After each message, you will propose to the user what next steps they can take and ask them to choose.
```

This will prevent the MCP server from uncontrollably making API calls of its own volition, allowing the user to control how they want to search through the NASA Planetary Data System.

#### MCP client software tested 

#### Claude Desktop integration

Connect our MCP server to Claude Desktop, as described in https://modelcontextprotocol.io/quickstart/user#installing-the-filesystem-server, using the following configuration:

Create a project.

Add the instructions above in the instructions section.

Go to the newly created project and you can test with the example conversation above.

#### Custom MCP client

gradio, hugging face

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

## Dependencies

Requires Python 3.13+. Library dependencies listed in `requirements.txt`.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For issues related to:

- **PDS Registry API**: Contact pds-operator@jpl.nasa.gov or open an issue [here](https://github.com/NASA-PDS/pds-api)
- **This MCP Server**: Open an issue in this repository
- **MCP Protocol**: Check the [MCP documentation](https://modelcontextprotocol.io/) or [FastMCP documentation](https://gofastmcp.com/getting-started/welcome)

## Other Resources

- [PDS API Swagger OAS](https://pds.mcp.nasa.gov/api/search/1/swagger-ui/index.html)
