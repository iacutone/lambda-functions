const https     = require('https');
var trelloKey   = "<trelloKey>";
var trelloBoard = "<trelloBoard>"
var trelloToken = "<trelloToken";
var trelloUrl   = `https://api.trello.com/1/boards/${trelloBoard}/lists?cards=open&card_fields=name&fields=name&key=${trelloKey}&token=${trelloToken}`
var flowToken   = "<flowDockToken>";

function createID() {
  var date = new Date();

  return date.getFullYear().toString() + date.getMonth().toString() + date.getMinutes().toString();
}

var threadId = createID();

function callback(error, response, body) {
  if (!error) {
    var info = JSON.parse(JSON.stringify(body));
    console.log(info);
  }
  else {
    console.log('Error happened: '+ error);
  }
}

function buildFieldArray(body) {
  var fieldArray = new Array;

  for (i = 0; i < body.length; i++) {
    var hash = {}
    hash["label"] = body[i].name
    hash["value"] = body[i].cards.length
    fieldArray.push(hash)
  }

  return fieldArray;
}

function buildTable(body) {
  var tableRows = '';

  for (i = 0; i < body.length; i++) {
    tableRows += "<tr>"
    tableRows += "<td>" + body[i].name + "</td><td>" + body[i].cards.length + "</td>"
    tableRows += "</tr>"
  }

  return tableRows;
}

function postToFlowDock(body) {
  tableRows = buildTable(body);
  fieldArray = buildFieldArray(body);

  var data = JSON.stringify({
    "flow_token": flowToken,
    "event": "activity",
    "author": {
      "name": "Trello",
      "avatar": "https://pbs.twimg.com/profile_images/552177275911671808/JiszgZdZ.png"
    },
    "title": "ticket stats",
    "body": "<table><tr><th>List Name</th><th>Count</th></tr>" + tableRows + "</table>",
    "external_thread_id": threadId,
    "thread": {
      "title": "Trello Card stats",
      "fields": fieldArray,
      "body": "Updated from Trello every hour"
    }
  });

  var options = {
    host: 'api.flowdock.com',
    port: '443',
    path: '/messages',
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Content-Length': Buffer.byteLength(data)
    }
  };

  var request = https.request(options, function(response) {
    console.log("statusCode: ", response.statusCode);
    console.log("headers: ", response.headers);

    response.setEncoding('utf8');
    response.on('data', function (chunk) {
      console.log("body: " + chunk);
    });
  });

  request.on('error', function (e) {
    console.log('Request error: ' + e);
  });

  console.log("body: " + data);
  request.write(data);
  request.end();
}

exports.handler = function(event, context) {
  
  const getContent = function(url) {
    // return new pending promise
    return new Promise((resolve, reject) => {
      // select http or https module, depending on reqested url
      const lib = url.startsWith('https') ? require('https') : require('http');
      const request = lib.get(url, (response) => {
        // handle http errors
        if (response.statusCode < 200 || response.statusCode > 299) {
           reject(new Error('Failed to load page, status code: ' + response.statusCode));
         }
        // temporary data holder
        const body = [];
        // on every content chunk, push it to the data array
        response.on('data', (chunk) => body.push(chunk));
        // we are done, resolve promise with those joined chunks
        response.on('end', () => resolve(JSON.parse(body.join(''))));
      });
      // handle connection errors of the request
      request.on('error', (err) => reject(err))
      })
  };

  getContent(trelloUrl).then((response) => postToFlowDock(response)).catch((err) => console.error('Error' + err));
  
};
