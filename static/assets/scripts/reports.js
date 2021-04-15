function reports_acd_abn_calls(acdCalls, abnCalss) {
    var index, p_acd, p_abn,
        info = ACD_ABN_REPORTS;

    if (acdCalls == 0) {
        p_acd = 'd-none';
    } else {
        p_acd = 'empty';
    }

    if (abnCalss == 0) {
        p_abn = 'd-none'
    } else {
        p_abn = 'empty';
    }

    $("#reports-acd-abn-calls").children().remove();

    for (index = 0; index < info.length; ++index) {
        $("<tr>").html("<td>" + info[index].doper + "</td>" +
            "<td>" + info[index].service_level + " %</td>" +
            "<td>" + numberWithCommas_space(info[index].vdn_incalls) + "</td>" +
            "<td>" + numberWithCommas_space(info[index].vdn_abncalls) + "</td>" +
            "<td>" + numberWithCommas_space(info[index].omilia_far_hup + info[index].omilia_near_hup) + "</td>" +
            "<td>" + numberWithCommas_space(info[index].omilia_prc) + " %</td>" +
            "<td>" + numberWithCommas_space(info[index].ivr_successful) + "</td>" +
            "<td>" + numberWithCommas_space(info[index].ivr_successful_prc) + " %</td>" +
            "<td>" + numberWithCommas_space(info[index].ivr_breaked) + "</td>" +
            "<td>" + numberWithCommas_space(info[index].callsoffered) + "</td>" +
            "<td>" + numberWithCommas_space(info[index].callsoffered_prc) + " %</td>" +
            "<td>" + numberWithCommas_space(info[index].acdcalls) + "</td>" +
            "<td>" + numberWithCommas_space(info[index].acdcalls_prc) + " %</td>" +
            "<td class=" + p_acd + ">" + numberWithCommas_space(info[index].acd_do_40sec) + "</td>" +
            "<td class=" + p_acd + ">" + info[index].acd_do_40sec_prc + " %</td>" +
            "<td class=" + p_acd + ">" + numberWithCommas_space(info[index].acd_do_60sec) + "</td>" +
            "<td class=" + p_acd + ">" + info[index].acd_do_60sec_prc + " %</td>" +
            "<td class=" + p_acd + ">" + numberWithCommas_space(info[index].acd_do_2min) + "</td>" +
            "<td class=" + p_acd + ">" + info[index].acd_do_2min_prc + " %</td>" +
            "<td class=" + p_acd + ">" + info[index].acd_do_5min + "</td>" +
            "<td class=" + p_acd + ">" + info[index].acd_do_5min_prc + " %</td>" +
            "<td class=" + p_acd + ">" + info[index].acd_do_10min + "</td>" +
            "<td class=" + p_acd + ">" + info[index].acd_do_10min_prc + " %</td>" +
            "<td class=" + p_acd + ">" + info[index].acd_ot_10min + "</td>" +
            "<td class=" + p_acd + ">" + info[index].acd_ot_10min_prc + " %</td>" +
            "<td>" + numberWithCommas_space(info[index].abncalls) + "</td>" +
            "<td class=" + p_abn + ">" + info[index].abn_do_10sec + "</td>" +
            "<td class=" + p_abn + ">" + info[index].abn_do_10sec_prc + " %</td>" +
            "<td class=" + p_abn + ">" + info[index].abn_do_15sec + " </td>" +
            "<td class=" + p_abn + ">" + info[index].abn_do_15sec_prc + " %</td>" +
            "<td class=" + p_abn + ">" + info[index].abn_do_20sec + "</td>" +
            "<td class=" + p_abn + ">" + info[index].abn_do_20sec_prc + " %</td>" +
            "<td class=" + p_abn + ">" + info[index].abn_do_30sec + "</td>" +
            "<td class=" + p_abn + ">" + info[index].abn_do_30sec_prc + " %</td>" +
            "<td class=" + p_abn + ">" + info[index].abn_do_40sec + "</td>" +
            "<td class=" + p_abn + ">" + info[index].abn_do_40sec_prc + " %</td>" +
            "<td class=" + p_abn + ">" + info[index].abn_do_60sec + "</td>" +
            "<td class=" + p_abn + ">" + info[index].abn_do_60sec_prc + " %</td>" +
            "<td class=" + p_abn + ">" + info[index].abn_do_2min + "</td>" +
            "<td class=" + p_abn + ">" + info[index].abn_do_2min_prc + " %</td>" +
            "<td class=" + p_abn + ">" + info[index].abn_do_5min + "</td>" +
            "<td class=" + p_abn + ">" + info[index].abn_do_5min_prc + " %</td>" +
            "<td class=" + p_abn + ">" + info[index].abn_do_10min + "</td>" +
            "<td class=" + p_abn + ">" + info[index].abn_do_10min_prc + " %</td>" +
            "<td class=" + p_abn + ">" + info[index].abn_ot_10min + "</td>" +
            "<td class=" + p_abn + ">" + info[index].abn_ot_10min_prc + " %</td>" +
            "<td>" + info[index].abncalls_prc + " %</td>" +
            "</tr>").appendTo('#reports-acd-abn-calls')
    }

    $("<tr class='empty_tr'>").html("<td></td>" +
        "</tr>").appendTo('#reports-acd-abn-calls')
}

function reports_acd_abn_utp_calls(acdCalls, abnCalss) {
    var index, p_acd, p_abn,
        info = ACD_ABN_UTP_REPORTS;

    if (acdCalls == 0) {
        p_acd = 'd-none';
    } else {
        p_acd = 'empty';
    }

    if (abnCalss == 0) {
        p_abn = 'd-none'
    } else {
        p_abn = 'empty';
    }

    $("#reports-acd-abn-utp-calls").children().remove();

    for (index = 0; index < info.length; ++index) {
        $("<tr>").html("<td>" + info[index].doper + "</td>" +
            "<td>" + info[index].service_level + " %</td>" +
            "<td>" + numberWithCommas_space(info[index].callsoffered) + "</td>" +
            "<td>" + numberWithCommas_space(info[index].acdcalls) + "</td>" +
            "<td>" + numberWithCommas_space(info[index].acdcalls_prc) + " %</td>" +
            "<td class=" + p_acd + ">" + numberWithCommas_space(info[index].acd_do_40sec) + "</td>" +
            "<td class=" + p_acd + ">" + info[index].acd_do_40sec_prc + " %</td>" +
            "<td class=" + p_acd + ">" + numberWithCommas_space(info[index].acd_do_60sec) + "</td>" +
            "<td class=" + p_acd + ">" + info[index].acd_do_60sec_prc + " %</td>" +
            "<td class=" + p_acd + ">" + numberWithCommas_space(info[index].acd_do_2min) + "</td>" +
            "<td class=" + p_acd + ">" + info[index].acd_do_2min_prc + " %</td>" +
            "<td class=" + p_acd + ">" + info[index].acd_do_5min + "</td>" +
            "<td class=" + p_acd + ">" + info[index].acd_do_5min_prc + " %</td>" +
            "<td class=" + p_acd + ">" + info[index].acd_do_10min + "</td>" +
            "<td class=" + p_acd + ">" + info[index].acd_do_10min_prc + " %</td>" +
            "<td class=" + p_acd + ">" + info[index].acd_ot_10min + "</td>" +
            "<td class=" + p_acd + ">" + info[index].acd_ot_10min_prc + " %</td>" +
            "<td>" + numberWithCommas_space(info[index].abncalls) + "</td>" +
            "<td class=" + p_abn + ">" + info[index].abn_do_10sec + "</td>" +
            "<td class=" + p_abn + ">" + info[index].abn_do_10sec_prc + " %</td>" +
            "<td class=" + p_abn + ">" + info[index].abn_do_15sec + " </td>" +
            "<td class=" + p_abn + ">" + info[index].abn_do_15sec_prc + " %</td>" +
            "<td class=" + p_abn + ">" + info[index].abn_do_20sec + "</td>" +
            "<td class=" + p_abn + ">" + info[index].abn_do_20sec_prc + " %</td>" +
            "<td class=" + p_abn + ">" + info[index].abn_do_30sec + "</td>" +
            "<td class=" + p_abn + ">" + info[index].abn_do_30sec_prc + " %</td>" +
            "<td class=" + p_abn + ">" + info[index].abn_do_40sec + "</td>" +
            "<td class=" + p_abn + ">" + info[index].abn_do_40sec_prc + " %</td>" +
            "<td class=" + p_abn + ">" + info[index].abn_do_60sec + "</td>" +
            "<td class=" + p_abn + ">" + info[index].abn_do_60sec_prc + " %</td>" +
            "<td class=" + p_abn + ">" + info[index].abn_do_2min + "</td>" +
            "<td class=" + p_abn + ">" + info[index].abn_do_2min_prc + " %</td>" +
            "<td class=" + p_abn + ">" + info[index].abn_do_5min + "</td>" +
            "<td class=" + p_abn + ">" + info[index].abn_do_5min_prc + " %</td>" +
            "<td class=" + p_abn + ">" + info[index].abn_do_10min + "</td>" +
            "<td class=" + p_abn + ">" + info[index].abn_do_10min_prc + " %</td>" +
            "<td class=" + p_abn + ">" + info[index].abn_ot_10min + "</td>" +
            "<td class=" + p_abn + ">" + info[index].abn_ot_10min_prc + " %</td>" +
            "<td>" + info[index].abncalls_prc + " %</td>" +
            "</tr>").appendTo('#reports-acd-abn-utp-calls')
    }

    $("<tr class='empty_tr'>").html("<td></td>" +
        "</tr>").appendTo('#reports-acd-abn-utp-calls')
}

function reports_acd_abn_calls_upd() {
    $.ajax({
        url: '/api/reports/main-report',
        method: 'GET'
    }).
    done(function(data) {
        ACD_ABN_REPORTS = data.result;

        reports_acd_abn_calls(0, 0);

    }).fail(function(error) {
        console.error(error);
    });
}

function reports_acd_abn_utp_calls_upd() {
    $.ajax({
        url: '/api/reports/utp-calls',
        method: 'GET'
    }).
    done(function(data) {
        ACD_ABN_UTP_REPORTS = data.result;

        reports_acd_abn_utp_calls(0, 0);

    }).fail(function(error) {
        console.error(error);
    });
}

function showDetail(report, value) {
    var newClass, step, rows,
        newColspan,
        classNameAcd,
        classNameAbn,
        acdOpened = 0,
        abnOpened = 0;

    if (report == 'acd-abn') {
        classNameAcd = document.getElementById('acd-row1').className;
        classNameAbn = document.getElementById('abn-row1').className;
    } else if (report == 'acd-abn-utp') {
        classNameAcd = document.getElementById('reports-utp-acd1').className;
        classNameAbn = document.getElementById('reports-utp-abn1').className;
    }

    if (classNameAcd == 'empty') {
        acdOpened = 1;
    }

    if (classNameAbn == 'empty') {
        abnOpened = 1;
    }

    if (value == 'acd') {
        rows = 13;
        if (acdOpened == 1) {
            newClass = 'd-none';
            newColspan = '2';
            acdOpened = 0;
            newTextContent = '(+)'
        } else {
            newClass = 'empty';
            newColspan = '12';
            acdOpened = 1;
            newTextContent = ''
        }
    }

    if (value == 'abn') {
        rows = 21;
        if (abnOpened == 1) {
            newClass = 'd-none';
            newColspan = '2';
            abnOpened = 0;
            newTextContent = '(+)'
        } else {
            newClass = 'empty';
            newColspan = '20';
            abnOpened = 1;
            newTextContent = ''
        }
    }

    for (step = 1; step <= rows; step++) {
        if (report == 'acd-abn') {
            document.getElementById(value + '-row' + String(step)).className = newClass;
        } else if (report == 'acd-abn-utp') {
            document.getElementById('reports-utp-' + value + String(step)).className = newClass;
        }
    }

    if (report == 'acd-abn') {
        document.getElementById(value + '-row1').colSpan = newColspan;
        document.getElementById(value + '-dop-info').textContent = newTextContent;
        reports_acd_abn_calls(acdOpened, abnOpened);
    } else if (report == 'acd-abn-utp') {
        document.getElementById('reports-utp-' + value + '1').colSpan = newColspan;
        document.getElementById('reports-utp-' + value + '-dop-info').textContent = newTextContent;
        reports_acd_abn_utp_calls(acdOpened, abnOpened);
    }
}

function loadReport(report) {
    var btnText = document.getElementById('opncls-btn-' + report).textContent;

    if (btnText.toUpperCase() == 'ПОКАЗАТЬ') {
        document.getElementById('rpt-' + report).style.display = 'block';
        document.getElementById('opncls-btn-' + report).textContent = 'Скрыть'
    } else {
        document.getElementById('rpt-' + report).style.display = 'None';
        document.getElementById('opncls-btn-' + report).textContent = 'Показать'
    }

    // if (report == 'main-acd-abn') {
    //     reports_acd_abn_calls_upd();
    // } else if (report == 'acd-abn-utp') {
    //     reports_acd_abn_utp_calls_upd();
    // }
}