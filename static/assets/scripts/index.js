var index_month_doughnut;

function index_online() {
    $.ajax({
        url: 'api/index/online',
        method: 'GET'
    }).
    done(function(data) {

        if (typeof data['status'] == 'undefined') {
            console.log('Ошибка в сервисе: api/index/online');
        
        } else {

            if (data.status != 'successful') {
                console.log('Ошибка в сервисе: api/index/online');
            
            } else {
                var index,
                    dayDict = data.data.day,
                    monthDict = data.data.month,
                    start_date = data.data.month_start_date;
                
                for (index = 0; index < Object.keys(dayDict).length; ++index) {
                    var sectorCode = Object.keys(dayDict)[index],
                        sectorDict = dayDict[sectorCode];
                    
                    document.getElementById('index-inqueue-' + sectorCode).textContent = sectorDict.inqueue;
                    document.getElementById('index-inqueue-' + sectorCode).className = 'text-' + set_inqueue_color(sectorDict.inqueue);

                    if (sectorCode == 'total') {
                        document.getElementById('index-sl-circle-' + sectorCode).className = 'z-index-sl-circle cirlce-' + set_sl_color(sectorDict.sl);
                        document.getElementById('index-sl-' + sectorCode).textContent = sectorDict.sl + '%';
                    } else {
                        document.getElementById('index-sl-' + sectorCode).textContent = sectorDict.sl + ' %';
                    }
                    document.getElementById('index-sl-' + sectorCode).className = 'text-' + set_sl_color(sectorDict.sl);
                    
                    if (document.getElementById('index-asa-' + sectorCode)) {
                        document.getElementById('index-asa-' + sectorCode).textContent = set_min_sec(sectorDict.asa);
                        document.getElementById('index-asa-' + sectorCode).className = 'text-' + set_asa_color(sectorDict.asa,'index');
                    }

                    if (document.getElementById('index-att-' + sectorCode)) {
                        document.getElementById('index-att-' + sectorCode).textContent = set_min_sec(sectorDict.att);
                        document.getElementById('index-att-' + sectorCode).className = 'text-' + set_att_color(sectorDict.att,'index');
                    }

                    if (document.getElementById('index-att-' + sectorCode)) {
                        document.getElementById('index-inqueue2-' + sectorCode).textContent = sectorDict.inqueue;
                    }

                    if (sectorCode.inqueue > 0 && sectorCode.oldest == 0) {
                        document.getElementById('index-mwt-' + sectorCode).textContent = '>16мин';
                        document.getElementById('index-mwt-' + sectorCode).className = 'text-' + set_oldest_color(960);
                    } else {
                        document.getElementById('index-mwt-' + sectorCode).textContent = set_min_sec(sectorDict.oldest);
                        document.getElementById('index-mwt-' + sectorCode).className = 'text-' + set_oldest_color(sectorDict.oldest);
                    }

                    document.getElementById('index-callsoffered-' + sectorCode).textContent = numberWithCommas(sectorDict.callsoffered);
                    document.getElementById('index-acdcalls-abncalls-outflowcalls-' + sectorCode).textContent = numberWithCommas(sectorDict.acdcalls) + ' / ' + numberWithCommas(sectorDict.abncalls) + ' / ' + numberWithCommas(sectorDict.outflowcalls);
                    document.getElementById('index-acceptable-slvlabns-' + sectorCode).textContent = numberWithCommas(sectorDict.acceptable) + ' / ' + numberWithCommas(sectorDict.slvlabns);
                    document.getElementById('index-service-levels-' + sectorCode).textContent = numberWithCommas(sectorDict.sl) + ' %';

                    if ('cba' in sectorDict) {
                        sectorCode = sectorCode + '_cba';

                        if (sectorDict.cba.inqueue > 1 && sectorDict.cba.oldest == 0) {
                            document.getElementById('index-mwt-' + sectorCode).textContent = '>16мин';
                            document.getElementById('index-mwt-' + sectorCode).className = 'text-' + set_oldest_cba_color(960);
    
                            document.getElementById('index-inqueue-' + sectorCode).textContent = sectorDict.cba.inqueue;
                            document.getElementById('index-inqueue-' + sectorCode).className = 'text-' + set_oldest_cba_color(960);
                        } else {
                            document.getElementById('index-mwt-' + sectorCode).textContent = set_min_sec(sectorDict.cba.oldest);
                            document.getElementById('index-mwt-' + sectorCode).className = 'text-' + set_oldest_cba_color(sectorDict.cba.oldest);
    
                            document.getElementById('index-inqueue-' + sectorCode).textContent = sectorDict.cba.inqueue;
                            document.getElementById('index-inqueue-' + sectorCode).className = 'text-' +  set_oldest_cba_color(sectorDict.cba.oldest);
                        }
                    }
                }

                for (index = 0; index < Object.keys(monthDict).length; ++index) {
                    var sectorCode = Object.keys(monthDict)[index],
                        sectorDict = monthDict[sectorCode];

                    if (sectorCode == 'total') {
                        document.getElementById('index-m-sl-' + sectorCode).textContent = sectorDict.sl + '%';
                        document.getElementById('index-m-sl-' + sectorCode).className = 'text-' + set_sl_color(sectorDict.sl);
                        document.getElementById('index-m-sl-circle-' + sectorCode).className = 'z-index-sl-circle cirlce-' + set_sl_color(sectorDict.sl);
                    }

                    document.getElementById('index-m-callsoffered-' + sectorCode).textContent = numberWithCommas(sectorDict.callsoffered);
                    document.getElementById('index-m-acdcalls-abncalls-outflowcalls-' + sectorCode).textContent = numberWithCommas(sectorDict.acdcalls) + ' / ' + numberWithCommas(sectorDict.abncalls) + ' / ' + numberWithCommas(sectorDict.outflowcalls);
                    document.getElementById('index-m-acceptable-slvlabns-' + sectorCode).textContent = numberWithCommas(sectorDict.acceptable) + ' / ' + numberWithCommas(sectorDict.slvlabns);
                    document.getElementById('index-m-service-levels-' + sectorCode).textContent = numberWithCommas(sectorDict.sl) + ' %';                    
                }

                $("#z-index-rings-count").children().remove();
                $("#z-index-month-count").children().remove();
        
                $('#z-index-month-date').text(start_date);
                $('#z-index-month-date2').text(start_date);     
            }
        }

        $('#z-index-curr-date-time').text(getTime());

    }).fail(function(error) {
        console.error(error);
    });
}

function index_fcr_acr() {
    $.ajax({
        url: 'api/index/online/other_parametrs',
        method: 'GET'
    }).
    done(function(data) {

        if (typeof data['status'] == 'undefined') {
            console.log('Ошибка в сервисе: api/index/online/other_parametrs');
        }

        else {
            if (data.status != 'successful') {
                console.log('Ошибка в сервисе: api/index/online/other_parametrs');
            }

            else {
                index_fcr_acr_dict = data.data;
                

                var fcr = data.data.fcr,
                    index,
                    acrDict = data.data.acr;

                for (index = 0; index < Object.keys(acrDict).length; ++index) {
                    var sectorCode = Object.keys(acrDict)[index];

                    if (sectorCode == 'all') {
                        continue;
                    }

                    document.getElementById('index-acr-' + sectorCode).textContent = acrDict[sectorCode];
                    document.getElementById('index-acr-' + sectorCode).className = 'text-' + set_acr_color(acrDict[sectorCode]);
                }

                document.getElementById('index-fcr-day').textContent = fcr + '%';
                document.getElementById('index-fcr-day').className = 'text-' + set_fcr_color(fcr);
            }
        }

    }).fail(function(error) {
        console.error(error);
    });
}

function index_operators() {
    $.ajax({
        url: 'api/index/online/operators',
        method: 'GET'
    }).
    done(function(data) {

        if (typeof data['status'] == 'undefined') {
            console.log('Ошибка в сервисе: api/index/operators');
        } 
        else {

            if (data.status != 'successful') {
                console.log('Ошибка в сервисе: api/index/operators');
            } 
            else {
                INDEX_OPERATORS_DATA = data.data;

                var sectorData = data.data.sectors,
                    depsData = data.data.deps;

                function setValue(ElementID, value) {
                    var Exist = document.getElementById(ElementID).classList.contains('btn-outline-primary2');
        
                    document.getElementById(ElementID).textContent = value;
        
                    if (value > 0) {
                        if (Exist == false) {
                            document.getElementById(ElementID).classList.add('btn-outline-primary2');
                        }
                        document.getElementById(ElementID).style.textDecoration = 'underline';
                        document.getElementById(ElementID).style.cursor = 'pointer';
                    } else {
                        document.getElementById(ElementID).style.textDecoration = '';
                        if (Exist) {
                            document.getElementById(ElementID).classList.remove('btn-outline-primary2');
                        }
                    }
                }
               
                for (index = 0; index < Object.keys(sectorData).length; ++index) {
                    var sectorCode = Object.keys(sectorData)[index],
                        modeReasons = sectorData[sectorCode].ModeReasons;

                        if (sectorCode == 'unknown') {
                            continue
                        }
                        
                    for (indexReason = 0; indexReason < Object.keys(modeReasons).length; ++indexReason) {
                        var reasonCode = Object.keys(modeReasons)[indexReason];
                        
                        setValue('index-' + reasonCode + '-' + sectorCode, modeReasons[reasonCode].length);
                    }

                    document.getElementById('index-status-available-' + sectorCode).textContent = modeReasons.available.length;
                    document.getElementById('index-status-available-' + sectorCode).className = 'text-success';
                    document.getElementById('index-status-acd-' + sectorCode).textContent = modeReasons.acd.length;
                    document.getElementById('index-status-acd-' + sectorCode).className = 'text-success';

                    document.getElementById('index-operatorsCC-' + sectorCode).textContent = sectorData[sectorCode].totalAgents_CC;
                    document.getElementById('index-operatorsFilial-' + sectorCode).textContent = sectorData[sectorCode].totalAgents_Filial;
                    document.getElementById('index-operatorsUnknown-' + sectorCode).textContent = sectorData[sectorCode].totalAgents_Unknown;

                    if ('cba' in sectorData[sectorCode]) {
                        modeReasons = sectorData[sectorCode].cba.ModeReasons;
                        setValue('index-cba-' + sectorCode, modeReasons['acd'].length);
                        
                        document.getElementById('index-status-available-' + sectorCode + '_cba').textContent = modeReasons.available.length;
                        document.getElementById('index-status-available-' + sectorCode + '_cba').className = 'text-success';
                        document.getElementById('index-status-acd-' + sectorCode + '_cba').textContent = modeReasons.acd.length;
                        document.getElementById('index-status-acd-' + sectorCode + '_cba').className = 'text-success';
                    }
                }

                // операторы управлений
                var totalAgentsOnline = 0;
                for (index = 0; index < Object.keys(depsData).length; ++index) {
                    var depCode = Object.keys(depsData)[index];
                    totalAgentsOnline += depsData[depCode].length;

                    setValue('index-fact-' + depCode, depsData[depCode].length);
                    document.getElementById('index-pf-delta-' + depCode).textContent = depsData[depCode].length;

                    if (depCode == 'unknown') {
                        if (depsData[depCode].length == 0) {
                            document.getElementById('index-' + depCode + '-tr').style.color = '#eee';
                            document.getElementById('index-fact-' + depCode).textContent = '-';
                            document.getElementById('index-fact-' + depCode).style.color = '#eee';
                            document.getElementById('index-pf-delta-' + depCode).textContent = '-';
                        }
                    }
                }

                document.getElementById('index-fact-total').textContent = totalAgentsOnline;
                document.getElementById('index-pf-delta-total').textContent = totalAgentsOnline;

                // список операторов по выбранному статусу
                var oldSector = document.getElementById('index-operators-sector').textContent,
                    oldSectorLongname = document.getElementById('index-operators-sectorLongname').textContent,
                    oldStatus = document.getElementById('index-operators-state').textContent,
                    oldDscr = document.getElementById('index-operators-dscr').textContent,
                    oldDepCode = document.getElementById('index-operators-depCode').textContent,
                    action = document.getElementById('index-operators-action').textContent;

                if (action == 'widgetOperPressed') {
                    index_operators_list(oldSector, oldSectorLongname, oldStatus, oldDscr);
                }

                if (action == 'widgetDepsPressed') {
                    index_depsOperatorsList(oldDepCode);
                }
            }
        }

    }).fail(function(error) {
        console.error(error);
    });
}

function index_operators_list(sector, sectorLongname, status, dscr) {
    $("#index-operators").children().remove();

    var pressedButton = document.getElementById('index-' + status + '-' + sector).textContent;

    if (pressedButton.trim() == '-' || pressedButton.trim() == '0') {
        return console.log('Данных нет');
    }
   
    var stateClass = 'badge-warning',
        data,
        action = document.getElementById('index-operators-action').textContent,
        oldSector = document.getElementById('index-operators-sector').textContent,
        oldStatus = document.getElementById('index-operators-state').textContent,
        oldDepCode = document.getElementById('index-operators-depCode').textContent;
    
    if (action == 'widgetOperPressed') {
        document.getElementById('index-' + oldStatus + '-' + oldSector).classList.remove('active');
    }

    if (action == 'widgetDepsPressed') {
        document.getElementById('index-fact-' + oldDepCode).classList.remove('active');
    }

    if (sector in INDEX_OPERATORS_DATA.sectors) {
        var dataExist = false;

        if (status == 'cba') {
            if ('ModeReasons' in  INDEX_OPERATORS_DATA.sectors[sector].cba) {
                if ('acd' in INDEX_OPERATORS_DATA.sectors[sector].cba.ModeReasons) {
                    data = INDEX_OPERATORS_DATA.sectors[sector].cba.ModeReasons.acd;
                    dataExist = true;
                }
            }
        
        } else if ('ModeReasons' in  INDEX_OPERATORS_DATA.sectors[sector]) {
            if (status in INDEX_OPERATORS_DATA.sectors[sector]['ModeReasons']) {
                data = INDEX_OPERATORS_DATA.sectors[sector]['ModeReasons'][status]
                dataExist = true;
            }

        if (dataExist) {
                    
            if (status == 'available' || status == 'acd') {
                stateClass = 'badge-success';
            } else if (status == 'acw' || status == 'training') {
                stateClass = 'badge-info';
            }
            
            for (index = 0; index < data.length; ++index) {
                var agentNum = index + 1;
                
                $("<tr>").html("<td class='width-3prc' style='text-align:center; min-width:35px;'>" + agentNum + "</td>" +
                "<td class='width-25prc' style='text-align:center;'>" + sectorLongname + "</td>" +
                "<td class='width-27prc' style='text-align:left;'>" + data[index].name + ' (' + data[index].id + ")</td>" +
                "<td class='width-25prc' style='text-align:center;'>" + set_min_sec(data[index].duration) + "</td>" +
                "<td class='width-20prc' style='text-align:center;'><span class='badge " + stateClass + "'>" + dscr + "</span></td>" +
                "</tr>").appendTo('#index-operators')
            } 

            document.getElementById('index-' + status + '-' + sector).classList.add('active');
            document.getElementById('index-operators-action').textContent = 'widgetOperPressed';
            document.getElementById('index-operators-sector').textContent = sector;
            document.getElementById('index-operators-sectorLongname').textContent = sectorLongname;
            document.getElementById('index-operators-state').textContent = status;
            document.getElementById('index-operators-dscr').textContent = dscr;
            }
        }
    }
}

function index_depsOperatorsList(depCode) {
    $("#index-operators").children().remove();

    var action = document.getElementById('index-operators-action').textContent,
        oldSector = document.getElementById('index-operators-sector').textContent,
        oldStatus = document.getElementById('index-operators-state').textContent,
        oldDepCode = document.getElementById('index-operators-depCode').textContent;

    if (action == 'widgetOperPressed') {
        document.getElementById('index-' + oldStatus + '-' + oldSector).classList.remove('active');
    }

    if (action == 'widgetDepsPressed') {
        document.getElementById('index-fact-' + oldDepCode).classList.remove('active');
    }

    var data = INDEX_OPERATORS_DATA.deps;

    if (depCode in data) {
        for (index = 0; index < data[depCode].length; ++index) {
            var agentNum = index + 1,
                agentReason = data[depCode][index].modeReason;

            if (agentReason == 'available') {
                stateClass = 'badge-success';
            } 
            else if (agentReason == 'acd') {
                stateClass = 'badge-success';
            } 
            else if (agentReason == 'acw') {
                stateClass = 'badge-info';
            } 
            else if (agentReason == 'training') {
                stateClass = 'badge-info';
            }
            else if (agentReason == 'unknown') {
                stateClass = 'badge-danger';
            }
            else {
                stateClass = 'badge-warning';
            }

            $("<tr>").html("<td class='width-3prc' style='text-align:center; min-width:35px;'>" + agentNum + "</td>" +
            "<td class='width-25prc' style='text-align:center;'>" + data[depCode][index].sectorLongname + "</td>" +
            "<td class='width-27prc' style='text-align:left;'>" + data[depCode][index].name + ' (' + data[depCode][index].id + ")</td>" +
            "<td class='width-25prc' style='text-align:center;'>" + set_min_sec(data[depCode][index].duration) + "</td>" +
            "<td class='width-20prc' style='text-align:center;'><span class='badge " + stateClass + "'>" + data[depCode][index].modeReasonLongname + "</span></td>" +
            "</tr>").appendTo('#index-operators');
        }

        document.getElementById('index-fact-' + depCode).classList.add('active');
        document.getElementById('index-operators-action').textContent = 'widgetDepsPressed';
        document.getElementById('index-operators-depCode').textContent = depCode;
    }
}

function index_graphic() {

    $.ajax({
        url: 'api/index/online/graphic',
        dataType: 'json',
        method: 'GET'
    }).
    done(function(data) {

        if (typeof data['status'] == 'undefined') {
            console.log('Ошибка в сервисе: api/index/online/graphic');
        
        } else {

            if (data.status != 'successful') {
                console.log('Ошибка в сервисе: api/index/online/graphic');
            
            } else {
                var chLine = document.getElementById("index-graphic"),
                    hoursKeys = data.hours_keys,
                    labelsLst = data.hours,
                    datasetSL = [],
                    dataDict = data.data;
                
                time_of_update_index_graphic = new Date();

                for (index = 0; index < Object.keys(dataDict).length; index++){

                    var sectorCode = Object.keys(dataDict)[index],
                        sectorDict = dataDict[sectorCode],
                        hoursDict = sectorDict.hours,
                        SL = [],
                        time = [],
                        callsoffered = [],
                        acceptable = [],
                        slvlabns = [],
                        acdcalls = [],
                        abncalls = [],
                        outflowcalls = [],
                        operatorsCount = [];
                        
                    for (index2 = 0; index2 < hoursKeys.length; index2++) {
                        var hoursKey = hoursKeys[index2];

                        if (hoursKey in hoursDict) {
                            SL.push(hoursDict[hoursKey].sl);
                            time.push(String(hoursDict[hoursKey].time));
                            callsoffered.push(hoursDict[hoursKey].callsoffered);
                            acceptable.push(hoursDict[hoursKey].acceptable);
                            slvlabns.push(hoursDict[hoursKey].slvlabns);
                            acdcalls.push(hoursDict[hoursKey].acdcalls);
                            abncalls.push(hoursDict[hoursKey].abncalls);
                            outflowcalls.push(hoursDict[hoursKey].outflowcalls);
                            operatorsCount.push(hoursDict[hoursKey].operators_count);
                        } else {
                            SL.push('-');
                            time.push('-');
                            callsoffered.push('-');
                            acceptable.push('-');
                            slvlabns.push('-');
                            acdcalls.push('-');
                            abncalls.push('-');
                            outflowcalls.push('-');
                            operatorsCount.push('-');
                        }
                    }

                    datasetSL.push({
                        data: SL,
                        sl: SL,
                        time: time,
                        callsoffered: callsoffered,
                        acceptable: acceptable,
                        slvlabns: slvlabns,
                        acdcalls: acdcalls,
                        abncalls: abncalls,
                        outflowcalls: outflowcalls,
                        operatorsCount: operatorsCount,
                        backgroundColor: 'transparent',
                        borderColor: sectorDict.graphicLineColor,
                        borderWidth: 4,
                        pointBackgroundColor: sectorDict.graphicLineColor,
                        label: sectorDict.longname
                    });
                }

                if (chLine) {
                    if (index_chLine != '0') {
                        index_chLine.destroy();                    
                    }
    
                    index_chLine = new Chart(chLine, {
                        type: 'line',
                        data: {
                            labels: labelsLst,
                            datasets: datasetSL
                        },
                        options: {
                            scales: {
                                yAxes: [{
                                    ticks: {
                                        beginAtZero: false,
                                    }
                                }]
                            },
                            centertext: '',
                            legend: {
                                display: true,
                                position: "bottom",
                                labels: {
                                    fontSize: 14
                                }
                            },
                            maintainAspectRatio: true,
                            tooltips: {
                                callbacks: {
                                    title: function() {
                                        return 'Service Level';
                                    },
                                    label: function(item, data) {
                                        var text1 = ' Время - ' + data.datasets[item.datasetIndex].time[item.index],
                                            text2 = ' Service Level - ' + data.datasets[item.datasetIndex].sl[item.index] + ' %',
                                            text3 = ' Кол.вх.звонков - ' + numberWithCommas(data.datasets[item.datasetIndex].callsoffered[item.index]),
                                            text4 = ' Кол.принятых звонков - ' + numberWithCommas(data.datasets[item.datasetIndex].acdcalls[item.index]),
                                            text5 = ' Кол.потерянных звонков - ' + numberWithCommas(data.datasets[item.datasetIndex].abncalls[item.index]),
                                            text6 = ' Кол.переадресованных звонков - ' + numberWithCommas(data.datasets[item.datasetIndex].outflowcalls[item.index]),
                                            text7 = ' Принятых в пределах SL - ' + numberWithCommas(data.datasets[item.datasetIndex].acceptable[item.index]),
                                            text8 = ' Потерянных в пределах SL - ' + numberWithCommas(data.datasets[item.datasetIndex].slvlabns[item.index]);
                                            text9 = ' Кол.обсл.операторов - ' + numberWithCommas(data.datasets[item.datasetIndex].operatorsCount[item.index]);
                                            text10 = '-------------------------------------------';
                
                                        return [text1, text2, text3, text4, text5, text6, text7, text8, text9, text10];
                                    },
                                    scales: {
                                        yAxes: [{ ticks: { fontSize: 20, fontFamily: "'Roboto', sans-serif", fontColor: '#000', fontStyle: '500' } }],
                                        xAxes: [{ ticks: { fontSize: 20, fontFamily: "'Roboto', sans-serif", fontColor: '#000', fontStyle: '500' } }]
                                    }
                                }
                            }
                        }
                    });           
                }
            }
        }
        
    }).fail(function(error) {
        console.error(error);
    });
}

function showSLformula() {
    if (document.getElementById("index-row-formula").style.display == 'none') {
        document.getElementById("index-row-formula").style.display = "";
        document.getElementById("index-row-formula").style.opacity = '1';
        $('#z-sl-formula').text('(скрыть формулу)');

    } else {
        document.getElementById("index-row-formula").style.display = 'none';
        $('#z-sl-formula').text('(см. формулу)');
    }
}

function index_chats() {
    $.ajax({
        url: 'api/index/chats',
        method: 'GET'
    }).
    done(function(data) {

        if (typeof data['status'] == 'undefined') {
            console.log('Ошибка в сервисе: api/index/chats');
        
        } else {

            if (data.status != 'successful') {
                console.log('Ошибка в сервисе: api/index/chats');
            
            } else {
                var inqueue = data.data.usersInQueueN.all,
                    served = data.data.movedToOperatorN.all;

                document.getElementById('index-inqueue-chats').textContent = inqueue;
                document.getElementById('index-inqueue-chats-color').className = 'text-' + set_chats_inqueue_color(inqueue);

                document.getElementById('index-inqueue-chats2').textContent = inqueue;
                document.getElementById('index-inqueue-chats2').className = 'text-' + set_chats_inqueue_color(inqueue);

                document.getElementById('index-status-acd-chats').textContent = served;
                document.getElementById('index-status-acd-chats').className = 'text-success';
            }
        }

    }).fail(function(error) {
        console.error(error);
    });
}