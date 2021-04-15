function graphics_sl() {
 
    $.ajax({
        url: '/api/graphics/service-level',
        dataType: 'json',
        method: 'GET'
    }).
    done(function(data) {

        var status = data.status,
            skillsLSt = ['all','cards','retail','homebank','onlinebank'];

        if (status == 'successful') {
            for (index = 0; index < skillsLSt.length; index++){
                nameSkill = skillsLSt[index];

                var chLineSL = document.getElementById("graphics-" + nameSkill + "-sl"),
                    chLineCalls = document.getElementById("graphics-" + nameSkill + "-callsoffered"),
                    colors = [window.chartColors.orange, window.chartColors.grey, '#3f6ad8', window.chartColors.green, '#d92550', '#8a2be2', '#ffd700'],
                    labelsLst = data.days_range,
                    skill = data[nameSkill],
                    keys = Object.keys(skill),
                    datasetSL = [];
                    datasetCalls = [];
                
                for (step = 0; step < keys.length; step++) {
                    var month_data = skill[keys[step]];
                        name = month_data.name,
                        SL = [],
                        doper = [],
                        callsoffered = [],
                        acceptable = [],
                        slvlabns = [];
    
                    for (index2 = 0; index2 < labelsLst.length; index2++) {
                        labelDay = 'day' + String(labelsLst[index2]);
                        
                        if (labelDay in month_data) {
                            SL.push(month_data[labelDay].sl);
                            doper.push(String(month_data[labelDay].doper));
                            callsoffered.push(month_data[labelDay].callsoffered);
                            acceptable.push(month_data[labelDay].acceptable);
                            slvlabns.push(month_data[labelDay].slvlabns);
                        } else {
                            SL.push('-');
                            doper.push('-');
                            callsoffered.push('-');
                            acceptable.push('-');
                            slvlabns.push('-');
                        }
                    }
    
                    datasetSL.push({
                        data: SL,
                        sl: SL,
                        doper: doper,
                        callsoffered: callsoffered,
                        acceptable: acceptable,
                        slvlabns: slvlabns,
                        backgroundColor: 'transparent',
                        borderColor: colors[step],
                        borderWidth: 4,
                        pointBackgroundColor: colors[step],
                        label: name
                    })
    
                    datasetCalls.push({
                        data: callsoffered,
                        sl: SL,
                        doper: doper,
                        callsoffered: callsoffered,
                        acceptable: acceptable,
                        slvlabns: slvlabns,
                        backgroundColor: 'transparent',
                        borderColor: colors[step],
                        borderWidth: 4,
                        pointBackgroundColor: colors[step],
                        label: name
                    })
                }

                var chartDataSL = {
                    labels: labelsLst,
                    datasets: datasetSL
                },
                    chartDataCalls = {
                        labels: labelsLst,
                        datasets: datasetCalls 
                }
        
                var chartOptions = {
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
                                var text1 = ' Месяц - ' + data.datasets[item.datasetIndex].label,
                                    text2 = ' Дата - ' + data.datasets[item.datasetIndex].doper[item.index],
                                    text3 = ' Service Level - ' + data.datasets[item.datasetIndex].sl[item.index] + ' %',
                                    text4 = ' Кол.вх.звонков - ' + numberWithCommas(data.datasets[item.datasetIndex].callsoffered[item.index]),
                                    text5 = ' Принятых в пределах SL - ' + numberWithCommas(data.datasets[item.datasetIndex].acceptable[item.index]),
                                    text6 = ' Потерянных в пределах SL - ' + numberWithCommas(data.datasets[item.datasetIndex].slvlabns[item.index]);
                                    text7 = '-------------------------------------------';
        
                                return [text1, text2, text3, text4, text5, text6, text7];
                            },
                            scales: {
                                yAxes: [{ ticks: { fontSize: 20, fontFamily: "'Roboto', sans-serif", fontColor: '#000', fontStyle: '500' } }],
                                xAxes: [{ ticks: { fontSize: 20, fontFamily: "'Roboto', sans-serif", fontColor: '#000', fontStyle: '500' } }]
                            }
                        }
                    }
                }
        
                if (chLineSL) {
                    new Chart(chLineSL, {
                        type: 'line',
                        data: chartDataSL,
                        options: chartOptions
                    });           
                }
        
                if (chLineCalls) {
                    new Chart(chLineCalls, {
                        type: 'line',
                        data: chartDataCalls,
                        options: chartOptions
                    });           
                }
            }
        }
    }).fail(function(error) {
        console.error(error);
    });
}

function graphics_show(value) {
    if (document.getElementById("graphics-diagrams-" + value).style.display == 'none') {
        document.getElementById("graphics-diagrams-" + value).style.display = "flex";
        document.getElementById("graphics-diagrams-" + value).style.opacity = '1';

    } else {
        document.getElementById("graphics-diagrams-" + value).style.display = 'none';
    }
}
