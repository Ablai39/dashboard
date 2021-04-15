function getType(obj) {
    if (obj && obj.constructor && obj.constructor.name) {
        return obj.constructor.name;
    }
    return Object.prototype.toString.call(obj).slice(8, -1).toLowerCase();
}

function logs(nUrl, nRoot, nList) {
    $.ajax({
        url: nUrl,
        async: false,
        method: 'GET'
    }).
    done(function(data) {
        $("<tr>").html("<td style='text-align: left;'>" + nList[0] + "</td>" +
            "<td style='text-align: left;'>" + nUrl + "</td>" +
            "<td style='text-align: center;'>" + nRoot + "</td>" +
            "<td style='text-align: center;'>" + data.status + "</td>" +
            "<td style='text-align: center;'>" + data.updated_datetime + "</td>" +
            "</tr>").appendTo('#logs')

    }).fail(function(error) {
        return error;
    });
}

function getLogs() {
    var nList = [
            ['index-online', '/api/index/online'],
            ['index-operators', '/api/index/online/operators'],
            ['index-graphic', '/api/index/online/graphic'],
            ['index-other-parametrs', '/api/index/online/other_parametrs'],

            ['wallboard_online', '/api/wallboard/online?upravlenie=upib'],
            ['wallboard_online', '/api/wallboard/online?upravlenie=rubs'],
            ['wallboard_online', '/api/wallboard/online?upravlenie=uprk'],

            ['wallboard_operators_7min', '/api/wallboard/online/operators7min?upravlenie=upib'],
            ['wallboard_operators_7min', '/api/wallboard/online/operators7min?upravlenie=rubs'],
            ['wallboard_operators_7min', '/api/wallboard/online/operators7min?upravlenie=uprk'],

            ['wallboard_best5', '/api/wallboard/online/best5?upravlenie=upib'],
            ['wallboard_best5', '/api/wallboard/online/best5?upravlenie=rubs'],
            ['wallboard_best5', '/api/wallboard/online/best5?upravlenie=uprk'],

            ['operators_list', '/api/operators'],

            ['ivr-online', '/api/ivr/online'],
            ['ivr-history', '/api/ivr/history'],

            ['omilia-online', '/api/omilia/online'],
            ['omilia-history', '/api/omilia/history'],
            
            ['reports-acd-abn-calls', '/api/reports/acd-abn-calls'],
            ['reports-acd-abn-utp-calls', '/api/reports/acd-abn-utp-calls']            
        ],
        root = '0',
        step;

    $("#logs").children().remove();

    for (step = 0; step < nList.length; step++) {
        var nURL;

        if (nList[step][0] == 'wallboard_online' || nList[step][0] == 'wallboard_operators_7min' || nList[step][0] == 'wallboard_best5') {
            nURL = nList[step][1] + '&root=' + root;
        } else {
            nURL = nList[step][1] + '?root=' + root;
        }

        logs(nURL, root, nList[step]);
    }
}