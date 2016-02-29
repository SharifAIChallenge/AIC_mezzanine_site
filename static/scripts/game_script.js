var doubleElimination = {
    "teams": [
        ["Team 1", "Team 2"],
        ["Team 3", "Team 4"]
    ],
    "results": [            // List of brackets (three since this is double elimination)
        [                     // Winner bracket
            [[1, 2], [3, 4]],   // First round and results
            [[5, 6]]            // Second round
        ],
        [                     // Loser bracket
            [[7, 8]],           // First round
            [[9, 10]]           // Second round
        ],
        [                     // Final "bracket"
            [                   // First round
                [11, 12],         // Match to determine 1st and 2nd
                [13, 14]          // Match to determine 3rd and 4th
            ],
            [                   // Second round
                [15, 16]          // LB winner won first round (11-12) so need a final decisive round
            ]
        ]
    ]
}


function saveFn(data, userData) {
    var json = jQuery.toJSON(data)
    $('#saveOutput').text('POST ' + userData + ' ' + json)
    /* You probably want to do something like this
     jQuery.ajax("rest/"+userData, {contentType: 'application/json',
     dataType: 'json',
     type: 'post',
     data: json})
     */
}

//$(function () {
//    var container = $('#saved')
//    container.bracket({
//        init: doubleElimination,
//        save: saveFn,
//        userData: "http://myapi"
//    })
//
//    /* You can also inquiry the current data */
//    var data = container.bracket('data')
//    $('#dataOutput').text(jQuery.toJSON(data))
//})


//window.setInterval(function () {
//    getPoints();  //calling every 10 seconds
//}, 10 * 1000);

function getPoints() {
    $.ajax({
        url: "get_points",
        method: 'get',
        context: document.body,
        data: {
            'group': 'all'
        }
    }).done(function () {
        $(this).addClass("done");
    });
}

$("a.group-link").fancybox({
    type: 'iframe',
    width: "100%",
    height: "100%",
    autoSize: false
});