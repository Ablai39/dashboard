function wallboard_best_top5() {
    $.ajax({
        url: '/api/wallboard/online/best5?upravlenie=' + upravlenie,
        dataType: 'json',
        method: 'GET'
    }).
    done(function(data) {
        var best_five = data.result;
        var step, nn, usrtab;
        $("#z-wallboard-top5-table-body").children().remove()

        for (step = 0; step < best_five.length; step++) {

            nn = step + 1;
            usrtab = pad(best_five[step].usrtab, 8);

            $("<tr style='height: 60px;'>").html("<td style='border: none; width: 10%; text-align: center; padding: 0px;'>" + nn + "</td>" +
                "<td style='border: none; padding: 0px;'>" +
                "<div class='widget-content-wrapper'>" +
                "<div class='widget-content-left mr-3'>" +
                "<img height='50' class='rounded-circle' src='http://om/foto/orgmanager/" + usrtab + ".jpg'>" +
                "</div>" +
                "<div class='widget-heading'>" + best_five[step].name + "</div>" +
                "</div>" +
                "</td>" +
                "<td class='text-center' style='border: none; padding: 0px;'>" + best_five[step].cnt + "</td>" +
                "</tr>").appendTo('#z-wallboard-top5-table-body')
        }
    }).fail(function(error) {
        console.error(error);
    });
}

var DisplayOriginalSize = 1

function wallboard_on_full_display() {
    if (DisplayOriginalSize == 1) {
        document.getElementById("z-base-app-main__outer").style.paddingLeft = '0px';
        document.getElementById("z-base-app-sidebar").style.display = 'none';
        document.getElementById("z-base-app-main").style.paddingTop = '0px';
        document.getElementById("z-base-app-header").style.display = 'none';
        document.getElementById("z-base-app-wrapper-footer").style.display = 'none';
        document.getElementById("z-base-app-main").style.backgroundColor = '#222';

        DisplayOriginalSize = 0;
        var html = document.documentElement;
        fullScreen(html);

    } else {
        document.getElementById("z-base-app-main__outer").style.paddingLeft = '280px';
        document.getElementById("z-base-app-sidebar").style.display = '';
        document.getElementById("z-base-app-main").style.paddingTop = '60px';
        document.getElementById("z-base-app-header").style.display = '';
        document.getElementById("z-base-app-wrapper-footer").style.display = '';
        document.getElementById("z-base-app-main").style.backgroundColor = '';

        DisplayOriginalSize = 1;

        // document.getElementById("z-wallboard-inqueue").style.width = '470px';
        // document.getElementById("z-wallboard-inqueue").style.height = '235px';
        // document.cancelFullScreen();
    }
}

function wallboard_online() {
    $.ajax({
        url: '/api/wallboard/online',
        dataType: 'json',
        method: 'GET'
    }).
    done(function(data) {
        if (typeof data['status'] == 'undefined') {
            console.log('Ошибка в сервисе: api/wallboard/online');
        }

        else {
            if (data.status != 'successful') {
                console.log('Ошибка в сервисе: api/wallboard/online');
            }

            else {
                // Пропущенные звонки
                var index, missedCalls = data.data.missedCalls;
                $("#z-wallboard-missed-calls-table-body").children().remove();

                if (upravlenie in missedCalls) {
                    for (index = 0; index < missedCalls[upravlenie].length; index++) {
           
                        var p_time = pad(missedCalls[upravlenie][index].time, 4),
                            p_time_1 = p_time.slice(0, 2),
                            p_time_2 = p_time.slice(2, 4),
            
                            p_operator_name;
            
                        if (missedCalls[upravlenie][index].count == 1) {
                            p_operator_name = missedCalls[upravlenie][index].operatorName
                        } else {
                            p_operator_name = missedCalls[upravlenie][index].operatorName + " (" + missedCalls[upravlenie][index].count.toString() + ")"
                        }
            
                        $("<tr style='color: #fff; line-height: 2.5rem;'>").html("<td style='text-align:center; border: none; padding: 0px;'>" +
                            "<div class='pe-7s-attention add_blink_animate800' style=color: #fff; margin-right: 10px;'></div>" +
                            "</td>" +
                            "<td style='text-align:left; border: none; padding: 0px;'>" + p_operator_name + "</td>" +
                            "<td style='text-align:left; border: none; padding: 0px; margin-left:5px;'> в " + p_time_1.toString() + ":" + p_time_2.toString() + " (" + missedCalls[upravlenie][index].splitCode + ")</td>" +
                            "</tr>").appendTo('#z-wallboard-missed-calls-table-body')
                    }
                }
                
                // ОПЕРАТОРЫ С ПРОДОЛЖИТЕЛЬНОСТЬЮ РАЗГОВОРА СВЫШЕ 7-ми мин
                var acd7minOperators = data.data.acd7min;
                $("#z-wallboard-7min-calls-table-body").children().remove();

                if (upravlenie in acd7minOperators) {
                    for (index = 0; index < acd7minOperators[upravlenie].length; index++) {

                        $("<tr style='color: #fff; line-height: 2.5rem;'>").html("<td style='text-align:center; border: none; padding: 0px;'>" +
                        "<div class='pe-7s-attention add_blink_animate800' style = 'color: #fff; margin-right:10px;'></div>" +
                        "</td>" +
                        "<td style='text-align:left; border: none; padding: 0px;'>" + acd7minOperators[upravlenie][index].name + "</td>" +
                        "<td style='text-align:left; border: none; padding: 0px; margin-left:5px;'>" + set_min_sec(acd7minOperators[upravlenie][index].duration) + "</td>" +
                        "</tr>").appendTo('#z-wallboard-7min-calls-table');
                    }
                }          
            }
        }
    }).fail(function(error) {
        console.error(error);
    });
}

function wallboard_index_info() {
    $.ajax({
        url: '/api/index/online',
        dataType: 'json',
        method: 'GET'
    }).
    done(function(data) {

        if (typeof data['status'] == 'undefined') {
            console.log('Ошибка в сервисе: api/index/online');
        }

        else {
            if (data.status != 'successful') {
                console.log('Ошибка в сервисе: api/index/online');
            }

            else {
                var dayDict = data.data.day,
                    icon, iconColor;

                $('#wallboard-all-inqueue').text(String(dayDict.total.inqueue));
                document.getElementById('wallboard-all-inqueue').className = 'text-' + set_inqueue_color(dayDict.total.inqueue, 'wallboard');
                $('#wallboard-all-sl').text(String(dayDict.total.sl) + ' %');
                document.getElementById('wallboard-all-sl').className = 'text-' + set_sl_color(dayDict.total.sl, 'wallboard');
        
                $("#wallboard-table-main-body").children().remove();

                for (index = 0; index < Object.keys(dayDict).length; ++index) {
                    var sectorCode = Object.keys(dayDict)[index];

                    if (sectorCode == 'total') {
                        continue;
                    }

                    if (set_inqueue_color(dayDict[sectorCode].inqueue) == 'danger') {
                        icon = 'pe-7s-attention add_blink_animate800';
                        iconColor = '#d92550'
                    } else if (set_inqueue_color(dayDict[sectorCode].inqueue) == 'warning') {
                        icon = 'pe-7s-users';
                        iconColor = '#ffc107';
                    } else if (dayDict[sectorCode].inqueue >= 1) {
                        icon = 'pe-7s-users';
                        iconColor = '#fff';
                    } else {
                        icon = 'nn';
                        iconColor = 'nn';
                    }

                    $("<tr>").html("<td style='text-align:left;'>" + dayDict[sectorCode].longname + "</td>" +
                    "<td style='text-align: right;'><div class=" + icon + " style = color:" + iconColor + "></div></td>" +
                    "<td class='text-" + set_inqueue_color(dayDict[sectorCode].inqueue, 'wallboard') + "' style='text-align: left;'>" + dayDict[sectorCode].inqueue + "</td>" +
                    "<td class='text-" + set_sl_color(dayDict[sectorCode].sl, 'wallboard') + "'>" +
                    "<i class='fa fa-fw' id='index-sl-arrow-" + name + "' aria-hidden='true' style='font-size: 15px; margin-right: 5px; display:none;'></i>" +
                    dayDict[sectorCode].sl + " %</td>" +
                    "<td class='text-" + set_asa_color(dayDict[sectorCode].asa, 'wallboard') + "'>" + dayDict[sectorCode].asa + "<span style='text-transform: none;'> сек</span></td>" +
                    "<td>" + numberWithCommas(dayDict[sectorCode].callsoffered) + "</td>" +
                    "</tr>").appendTo('#wallboard-table-main-body');
                }
            }
        }

        $('#z-wallboard-curr-date-time').text(getTime());

    }).fail(function(error) {
        console.error(error);
    });
}