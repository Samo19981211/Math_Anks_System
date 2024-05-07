const request = require('request');

exports.changeQuery = (panelId, newQuery, callback) => {
  const apiKey = 'eyJrIjoiNGNvNDE0TmJPNHpLSVlrMFV5c3NpRGxrRlZkbEZaNlUiLCJuIjoibWF0YXNua3NhcHAiLCJpZCI6MX0=';
  const options = {
    method: 'PATCH',
    url: `http://localhost:3000/d/557g6kYVz/matanks_app?orgId=1`,
    headers: {
      Authorization: `Bearer ${apiKey}`,
      'Content-Type': 'application/json',
    },
    body: {
      panels: [
        {
          id: panelId,
          targets: [
            {
              refId: 'A',
              query: newQuery,
            },
          ],
        },
      ],
    },
    json: true,
  };

  request(options, (error, response, body) => {
    if (error) {
      console.error(error);
      callback(error, null);
    } else {
      console.log(`Response from Grafana: ${JSON.stringify(body)}`);
      callback(null, body);
    }
  });
};