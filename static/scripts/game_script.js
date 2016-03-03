function onclick(data) {
    var win = window.open(data, '_blank');
    if (win) {
        win.focus();
    } else {
        alert('allow popups');
    }
}

function getPoints() {
    $.ajax({
        url: "/game/get-brackets",
        method: 'get',
        data: {}
    }).done(function (response) {
        var container = $('#bracket');
        container.bracket({
            init: response,
            skipConsolationRound: true,
            onMatchClick: onclick
        });
        setTimeout(getPoints, 10000);
    }).fail(function () {
        location.reload(true);
    });
}

getPoints();

