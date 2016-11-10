var request = require('request');
var trelloKey = '<yourTrelloKey>';
var trelloToken = '<yourTrelloToken>';
var trelloUrl = `https://api.trello.com/1/boards/v2w2pl1W/lists\?cards\=open\&card_fields\=name\&fields\=name\&key\=${trelloKey}\&token\=${trelloToken}`;
var flowToken = '<yourFlowToken>';

exports.handler = function(event, context) {

  request.get(trelloUrl, function(response) {
    var body = '';

    response.on("data", function(chunk) {
      body += chunk;
    });

    response.on('end', function() {
      var fieldArray = new Array;

      for (i = 0; i < body.length; i++) {
        var hash = {}
        hash["label"] = body[i].name
        hash["value"] = body[i].cards.length
        fieldArray.push(hash)
      }

      var tableRows = '';
      for (i = 0; i < body.length; i++) {
        tableRows += "<tr>"
        tableRows += "<td>" + body[i].name + "</td><td>" + body[i].cards.length + "</td>"
        tableRows += "</tr>"
      }

      var data = JSON.stringify({
        "flow_token": flowToken,
        "event": "activity",
        "author": {
          "name": "Trello",
          "avatar": "https://pbs.twimg.com/profile_images/552177275911671808/JiszgZdZ.png"
        },
        "title": "ticket stats",
        "body": "<table><tr><th>List Name</th><th>Count</th></tr>" + tableRows + "</table>",
        "external_thread_id": "1",
        "thread": {
          "title": "Trello Card stats",
          "fields": fieldArray,
          "body": "Updated from Trello every hour"
        }});

      var options = {
        method: 'POST',
        url: 'https://api.flowdock.com/messages',
        headers: {
          'Content-Type': 'application/json',
          'Content-Length': Buffer.byteLength(data)
        },
        body: data
      };

      function callback(error, response, body) {
        if (!error) {
          var info = JSON.parse(JSON.stringify(body));
          console.log(info);
        }
        else {
          console.log('Error happened: '+ error);
        }
      }

      request(options, callback);
    });
  }).on('error', function(err) {
    console.log('Error, with: ' + err.message);
    context.done("Failed");
  });
};

