$('.group').mixItUp({
    layout: {
        display: 'table-row'
    },
    animation: {},
    selectors: {},
    load: {
        sort: 'point:desc'
    }
});


function getPoints() {
    $.ajax({
        url: "/game/get-scores",
        method: 'get',
        data: {}
    }).done(function (response) {
        $.each(response, function (index, score) {
            $('#submit-' + score['id']).attr('data-point', score['score']).find(".score").text(score['score']);
        });
        $('.group').mixItUp('sort', 'point:desc');
        setTimeout(getPoints, 10000);
    }).fail(function () {
        location.reload(true);
    });
}
getPoints();
