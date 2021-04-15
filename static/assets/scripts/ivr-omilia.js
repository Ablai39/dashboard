function fget_skill_longname(vdn) {
    res = vdn
    if (vdn == '79588') {
        return 'Новые кредиты (УТП)_ru'

    } else if (vdn == '79585') {
        return 'Homebank_ru'

    } else if (vdn == '79587') {
        return 'Платежи и переводы_ru'

    } else if (vdn == '79586') {
        return 'Розница / Общие вопросы_ru'

    } else if (vdn == '79584') {
        return 'Карточки_ru'

    } else if (vdn == '79515') {
        return 'Карточки_kz'
    
    } else if (vdn == '79516') {
        return 'Homebank_kz'
    
    } else if (vdn == '79519') {
        return 'Новые кредиты (УТП)_kz'

    } else if (vdn == '79518') {
        return 'Платежи и переводы_kz'

    } else if (vdn == '79517') {
        return 'Розница / Общие вопросы_kz'

    }

    return vdn;
}

function fgetVdnCode(vdn) {
    res = vdn
    if (vdn == '79588') {
        return 'credits_ru'
    } else if (vdn == '79519') {
        return 'credits_kz'

    } else if (vdn == '79585') {
        return 'homebank_ru'
    } else if (vdn == '79516') {
        return 'homebank_kz'

    } else if (vdn == '79587') {
        return 'payments_ru'
    } else if (vdn == '79518') {
        return 'payments_kz'

    } else if (vdn == '79586') {
        return 'retail_ru'
    } else if (vdn == '79517') {
        return 'retail_kz'

    } else if (vdn == '79584') {
        return 'cards_ru'
    } else if (vdn == '79515') {
        return 'cards_kz'
    }

    return vdn;
}

function fget_intent_longname(intent) {

    if (intent == 'Card-Balance') {
        return ['Dynamic', 'Баланс по карте']

    } else if (intent == 'HomeBank-Connect') {
        return ['Static', 'Подключение SMS банкинга']

    } else if (intent == 'Card-Block') {
        return ['Dynamic', 'Блокировка карты']

    } else if (intent == 'Card-Unblock') {
        return ['Static', 'Разблокировка карты']

    } else if (intent == 'HomeBank-Remove-Restrictions') {
        return ['Static', 'Снять ограничения в Homebank']

    } else if (intent == 'HomeBank-Restore-Access') {
        return ['Static', 'Восстановить доступ к Homebank']

    } else if (intent == 'Credit_Card-Debt') {
        return ['Dynamic', 'Задолженность по кредитной карте']

    } else if (intent == 'Debt-Early_Payment-Info') {
        return ['Dynamic', 'Досрочное погашение']

    } else if (intent == 'Debt-Info') {
        return ['Dynamic', 'Задолженность по кредиту']
    
    } else if (intent == 'Block_Arrest-Info') {
        return ['Dynamic', 'Информация по арестам и блокировкам']

    } else if (intent == 'Renew-PIN_Counter') {
        return ['Dynamic', 'Сброс попыток неверного ввода PIN']
    
    } else if (intent == 'Card-Remove-Restrictions') {
        return ['Dynamic', 'Снятие лимитов']

    } else if (intent == 'OtherRequests') {
        return ['-', 'Другой запрос ']
    }
    return ['-', '! ' + intent];
}

function double_tap(doper, btnid, type) {

    if (OMILIA_HST_BTN != '') {
        document.getElementById(OMILIA_HST_BTN).classList.remove('active');
    }
    document.getElementById(btnid).classList.add('active');
    OMILIA_HST_BTN = btnid;

    if (type == 'all') {
        omilia_topic_th_app(doper);
    }
    omilia_hst_transfers_day(doper);
}

function omilia_topic_th_app(doper) {
    $.ajax({
        url: '/api/omilia/history/separated?doper=' + doper,
        dataType: 'json',
        method: 'GET'
    }).
    done(function(data) {
   
        var info = data.themes.result,
            total = data.themes.total,
            omilia_topic_element = document.getElementById("z-omilia-topic-of-appeal"),
            theme = [],
            omilia_themes_data = [],
            omilia_themes_data_prc = [],
            dynamic = 0,
            static = 0,
            other = 0,
            total_tem_dyn = 0,
            total_tem_sta = 0,
            total_tem_oth = 0,
            total_tem_dprc = 0,
            total_tem_sprc = 0,
            total_tem_oprc = 0;

        $('#omilia-top-app').text(' (за ' + doper + ')');

        $("#z-omilia-themes-dyn").children().remove();
        $("#z-omilia-themes-sta").children().remove();
        $("#z-omilia-themes-oth").children().remove();
        $("#z-omilia-themes-all").children().remove();
        document.getElementById("z-omilia-row-6").style.opacity = '1';       

        for (step = 0; step < info.length; step++) {
            var themes_data = fget_intent_longname(info[step].intent);

            nn = step + 1;
            theme[step] = themes_data[1]
            omilia_themes_data[step] = info[step].cnt;
            omilia_themes_data_prc[step] = Math.round(info[step].cnt / total * 100 * 100) / 100
            
            if (themes_data[0] == 'Dynamic') {
                dynamic += 1;
                total_tem_dyn += info[step].cnt;
                total_tem_dprc += omilia_themes_data_prc[step];
            $("<tr>").html("<td style='text-align: center; vertical-align:middle; min-width: 40px; max-width: 40px;'>" + dynamic + "</td>" +
                "<td style='text-align: center; vertical-align:middle; min-width: 100px; max-width: 100px;'>" + themes_data[0] + "</td>" +
                "<td style='text-align: left; vertical-align:middle; min-width: 200px; max-width: 200px;'>" + theme[step] + "</td>" +
                "<td style='text-align: center; vertical-align:middle; min-width: 100px; max-width: 100px;'>" + numberWithCommas(omilia_themes_data[step]) + "</td>" +
                "<td style='text-align: center; vertical-align:middle; min-width: 200px; max-width: 200px;'>" + omilia_themes_data_prc[step] + " %</td>"
            ).appendTo('#z-omilia-themes-dyn')
            
            } else if (themes_data[0] == 'Static'){
                static += 1;
                total_tem_sta += info[step].cnt;
                total_tem_sprc += omilia_themes_data_prc[step];
            $("<tr>").html("<td style='text-align: center; vertical-align:middle; min-width: 40px; max-width: 40px;'>" + static + "</td>" +
                "<td style='text-align: center; vertical-align:middle; min-width: 100px; max-width: 100px;'>" + themes_data[0] + "</td>" +
                "<td style='text-align: left; vertical-align:middle; min-width: 200px; max-width: 200px;'>" + theme[step] + "</td>" +
                "<td style='text-align: center; vertical-align:middle; min-width: 100px; max-width: 100px;'>" + numberWithCommas(omilia_themes_data[step]) + "</td>" +
                "<td style='text-align: center; vertical-align:middle; min-width: 200px; max-width: 200px;'>" + omilia_themes_data_prc[step] + " %</td>"
            ).appendTo('#z-omilia-themes-sta')
            
            } else {
                other += 1; 
                total_tem_oth += info[step].cnt;
                total_tem_oprc += omilia_themes_data_prc[step];
            $("<tr>").html("<td style='text-align: center; vertical-align:middle; min-width: 40px; max-width: 40px;'>" + other + "</td>" +
                "<td style='text-align: center; vertical-align:middle; min-width: 100px; max-width: 100px;'>" + themes_data[0] + "</td>" +
                "<td style='text-align: left; vertical-align:middle; min-width: 200px; max-width: 200px;'>" + theme[step] + "</td>" +
                "<td style='text-align: center; vertical-align:middle; min-width: 100px; max-width: 100px;'>" + numberWithCommas(omilia_themes_data[step]) + "</td>" +
                "<td style='text-align: center; vertical-align:middle; min-width: 200px; max-width: 200px;'>" + omilia_themes_data_prc[step] + " %</td>"
            ).appendTo('#z-omilia-themes-oth')}
        }
        
        var total_th_sum = 0,
            total_th_sprc = 0;

        for (step = 0; step < info.length; step++) {
            var themes_data = fget_intent_longname(info[step].intent);

            total_th_sum += info[step].cnt;
            total_th_sprc += omilia_themes_data_prc[step];


            nn = step + 1;
            theme[step] = themes_data[1]
            omilia_themes_data[step] = info[step].cnt;
            omilia_themes_data_prc[step] = Math.round(info[step].cnt / total * 100 * 100) / 100

            $("<tr>").html("<td style='text-align: center; vertical-align:middle; min-width: 40px; max-width: 40px;'>" + nn + "</td>" +
                "<td style='text-align: center; vertical-align:middle; min-width: 100px; max-width: 100px;'>" + themes_data[0] + "</td>" +
                "<td style='text-align: left; vertical-align:middle; min-width: 200px; max-width: 200px;'>" + theme[step] + "</td>" +
                "<td style='text-align: center; vertical-align:middle; min-width: 100px; max-width: 100px;'>" + numberWithCommas(omilia_themes_data[step]) + "</td>" +
                "<td style='text-align: center; vertical-align:middle; min-width: 200px; max-width: 200px;'>" + omilia_themes_data_prc[step] + " %</td>"
            ).appendTo('#z-omilia-themes-all')
        }
        
            $("<tr style='border-top: 1px solid rgba(13, 27, 62, 0.7)'>").html("<td style='text-align: center; vertical-align:middle; min-width: 40px; max-width: 40px;'>-</td>" +
            "<td style='text-align: center; vertical-align:middle; font-weight: bold; min-width: 100px; max-width: 100px;'>Итого</td>" +
            "<td style='text-align: center; vertical-align:middle; font-weight: bold; min-width: 200px; max-width: 200px;'>&nbsp</td>"+
            "<td style='text-align: center; vertical-align:middle; font-weight: bold; min-width: 100px; max-width: 100px;'>" + numberWithCommas(total_tem_dyn) + "</td>" +
            "<td style='text-align: center; vertical-align:middle; font-weight: bold; min-width: 200px; max-width: 200px;'>" + total_tem_dprc.toFixed(1) + " %</td>"
            ).appendTo('#z-omilia-themes-dyn');
                       
            $("<tr style='border-top: 1px solid rgba(13, 27, 62, 0.7)'>").html("<td style='text-align: center; vertical-align:middle; min-width: 40px; max-width: 40px;'>-</td>" +
            "<td style='text-align: center; vertical-align:middle; font-weight: bold; min-width: 100px; max-width: 100px;'>Итого</td>" +
            "<td style='text-align: center; vertical-align:middle; font-weight: bold; min-width: 200px; max-width: 200px;'>&nbsp</td>" +
            "<td style='text-align: center; vertical-align:middle; font-weight: bold; min-width: 100px; max-width: 100px;'>" + numberWithCommas(total_tem_sta) + "</td>" +
            "<td style='text-align: center; vertical-align:middle; font-weight: bold; min-width: 200px; max-width: 200px;'>" + total_tem_sprc.toFixed(1) + " %</td>"
            ).appendTo('#z-omilia-themes-sta');

            $("<tr style='border-top: 1px solid rgba(13, 27, 62, 0.7)'>").html("<td style='text-align: center; vertical-align:middle; min-width: 40px; max-width: 40px;'>-</td>" +
            "<td style='text-align: center; vertical-align:middle; font-weight: bold; min-width: 100px; max-width: 100px;'>Итого</td>" +
            "<td style='text-align: center; vertical-align:middle; font-weight: bold; min-width: 200px; max-width: 200px;'>&nbsp</td>" +
            "<td style='text-align: center; vertical-align:middle; font-weight: bold; min-width: 100px; max-width: 100px;'>" + numberWithCommas(total_tem_oth) + "</td>" +
            "<td style='text-align: center; vertical-align:middle; font-weight: bold; min-width: 200px; max-width: 200px;'>" + total_tem_oprc.toFixed(1) + " %</td>"
            ).appendTo('#z-omilia-themes-oth');

            $("<tr style='border-top: 1px solid rgba(13, 27, 62, 0.7)'>").html("<td style='text-align: center; vertical-align:middle; min-width: 40px; max-width: 40px;'>-</td>" +
            "<td style='text-align: center; vertical-align:middle; font-weight: bold; min-width: 100px; max-width: 100px;'>Итого</td>" +
            "<td style='text-align: center; vertical-align:middle; font-weight: bold; min-width: 200px; max-width: 200px;'>&nbsp</td>" +
            "<td style='text-align: center; vertical-align:middle; font-weight: bold; min-width: 100px; max-width: 100px;'>" + numberWithCommas(total_th_sum) + "</td>" +
            "<td style='text-align: center; vertical-align:middle; font-weight: bold; min-width: 200px; max-width: 200px;'>" + total_th_sprc.toFixed(1) + " %</td>"
            ).appendTo('#z-omilia-themes-all');

        if (omilia_topic_element) {
            new Chart(omilia_topic_element, {
                type: "doughnut",
                data: {
                    datasets: [{
                        data: omilia_themes_data_prc,
                        backgroundColor: ['#008B8B',
                            window.chartColors.yellow,
                            window.chartColors.grey,
                            window.chartColors.red,
                            window.chartColors.blue,
                            window.chartColors.orange,
                            '#BA55D3',
                            '#FF69B4',
                            '#A52A2A',
                            '#008000',
                            '#8A2BE2',
                        ],
                        label: "Dataset 1"
                    }],
                    labels: theme
                },
                options: {
                    responsive: !0,
                    legend: {
                        position: "left"
                    },
                    animation: {
                        animateScale: !0,
                        animateRotate: !0
                    },
                    tooltips: {
                        callbacks: {
                            title: function() {
                                return '';
                            },
                            label: function(item, data) {
                                return theme[item.index] + ': ' + omilia_themes_data_prc[item.index] + ' %';
                            }
                        }
                    }
                }
            });
        }

    }).fail(function(error) {
        console.error(error);
    });
}

function omilia_hst_transfers_day(doper) {
    $.ajax({
        url: '/api/omilia/history/transfers?doper=' + doper,
        dataType: 'json',
        method: 'GET'
    }).
    done(function(data) {
   
        var info = data.transfers.result,
            total = data.transfers.total,
            omilia_transfer = document.getElementById("z-omilia-canvas-transfer-2gr"),
            omilia_skill_groups = [],
            omilia_skill_data = [],
            omilia_skill_data_prc = [];
        
        $('#omilia-history-days').text(' (за ' + doper + ')');

        document.getElementById("z-omilia-column-tr-2gr").style.opacity = '1';

        // 2-й элемент общая сумма
        // 3-й элемент kz
        // 4-й элемент ru
        cards = ['Карточки','cards',0,0,0];
        homebank = ['Homebank','homebank',0,0,0];
        retail = ['Розница / Общие вопросы','retail',0,0,0];
        payments = ['Платежи и переводы','payments',0,0,0];
        credits = ['Новые кредиты (УТП)','credits',0,0,0];
        
        var total = 0,
        totalGetPrc = 0;
        for (index = 0; index < info.length; index++) {
            code = fgetVdnCode(info[index].point);
            cnt = info[index].cnt;

            if (code == 'cards_kz') {
                cards[2] += cnt;
                cards[3] = cnt;
                total += cnt
            } else if (code == 'cards_ru') {
                cards[2] += cnt;
                cards[4] = cnt;
                total += cnt;
            }

            if (code == 'retail_kz') {
                retail[2] += cnt;
                retail[3] = cnt;
                total += cnt
            } else if (code == 'retail_ru') {
                retail[2] += cnt;
                retail[4] = cnt;
                total += cnt
            }

            if (code == 'payments_kz') {
                payments[2] += cnt;
                payments[3] = cnt;
                total += cnt
            } else if (code == 'payments_ru') {
                payments[2] += cnt;
                payments[4] = cnt;
                total += cnt
            }

            if (code == 'homebank_kz') {
                homebank[2] += cnt;
                homebank[3] = cnt;
                total += cnt
            } else if (code == 'homebank_ru') {
                homebank[2] += cnt;
                homebank[4] = cnt;
                total += cnt
            }

            if (code == 'credits_kz') {
                credits[2] += cnt;
                credits[3] = cnt;
                total += cnt
            } else if (code == 'credits_ru') {
                credits[2] += cnt;
                credits[4] = cnt;
                total += cnt
            }
        }
        
        nList = [cards, homebank, retail, payments, credits];

        for (step = 0; step < nList.length; step++) {
            document.getElementById(nList[step][1] + '_cell_amount_ten').textContent = numberWithCommas(nList[step][2]);
            document.getElementById(nList[step][1] + '_kz_cell_amount_ten').textContent = numberWithCommas(nList[step][3]);
            document.getElementById(nList[step][1] + '_ru_cell_amount_ten').textContent = numberWithCommas(nList[step][4]);
            document.getElementById(nList[step][1] + '_cell_prc_ten').textContent = get_prc(nList[step][2], total) + '%';
            let totalPrc = get_prc(nList[step][2], total);
            totalGetPrc += totalPrc;
            
            $('#' + nList[step][1] + '_kz_span_ten').text('' + get_prc(nList[step][3], nList[step][2]) + '%' + '');
            $('#' + nList[step][1] + '_ru_span_ten').text('' + get_prc(nList[step][4], nList[step][2]) + '%' + '');
            $('#total_sum_prc_ten').text('' + totalGetPrc.toFixed(0) + '%' + '');

            omilia_skill_groups[step] = nList[step][0];
            omilia_skill_data[step] = nList[step][2];
            omilia_skill_data_prc[step] = totalPrc;
        }

        document.getElementById('total_sum_count_ten').textContent = numberWithCommas(total);
        

        if (omilia_transfer) {
            if (OmiliaTran != undefined) {
                OmiliaTran.destroy();
            }
            
            OmiliaTran = new Chart(omilia_transfer, {
                type: "doughnut",
                data: {
                    datasets: [{
                        data: omilia_skill_data_prc,
                        backgroundColor: [window.chartColors.green, window.chartColors.orange, window.chartColors.red, window.chartColors.blue, window.chartColors.yellow, '#a51fc7', '#4510a8', '#17cc54', '#248596', '#8bd810'],
                        label: "Dataset 1"
                    }],
                    labels: omilia_skill_groups
                },
                options: {
                    responsive: !0,
                    legend: {
                        position: "left"
                    },
                    title: {
                        display: !1,
                        text: "Chart.js Doughnut Chart"
                    },
                    animation: {
                        animateScale: !0,
                        animateRotate: !0
                    },
                    tooltips: {
                        callbacks: {
                            title: function() {
                                return '';
                            },
                            label: function(item, data) {
                                return omilia_skill_groups[item.index] + ': ' + omilia_skill_data_prc[item.index] + ' %';
                            }
                        }
                    }
                }
            });
        }
    }).fail(function(error) {
        console.error(error);
    });
}

function omilia_online(step) {
    $.ajax({
        url: '/api/omilia/online',
        dataType: 'json',
        method: 'GET'
    }).
    done(function(data) {
        var info = data.main,
            transfers = data.transfers,
            themes = data.themes,
            index, index2,
            duration = Math.round(info.AVG_DURATION / 1000),
            hour = duration / 3600 ^ 0,
            minute = (duration / 60 ^ 0) - (hour * 60),
            second = duration - ((hour * 3600) + (minute * 60)),
            online_transfer_2gr = document.getElementById("omilia-online-canvas-transfer-2gr"),
            tr2gr_groups = [],
            tr2gr_data = [],
            tr2gr_prc = [];
        
        console.log('test');
        document.getElementById('omilia-loader').style.display="None";
        document.getElementById('omilia-centered').style.display="None";

        $('#z-omilia-online-all').text(numberWithCommas(info.TOTAL_SUM));
        $('#z-omilia-online-far-hup').text(numberWithCommas(info.FAR_HUP));
        $('#z-omilia-online-near-hup').text(numberWithCommas(info.NEAR_HUP));
        $('#z-omilia-online-transfer').text(numberWithCommas(info.TRANSFER));

        $('.omilia-far-hup-progress').text(info.FAR_HUP + ' из ' + info.TOTAL_SUM);
        document.getElementById('progress-bar-far-hup-id').style.width = info.FAR_HUP_PRC + '%';

        $('.omilia-near-hup-progress').text(info.NEAR_HUP + ' из ' + info.TOTAL_SUM);
        document.getElementById('progress-bar-near-hup-id').style.width = info.NEAR_HUP_PRC + '%';

        $('.omilia-transfer-progress').text(info.TRANSFER + ' из ' + info.TOTAL_SUM);
        document.getElementById('progress-bar-transfer-id').style.width = info.TRANSFER_PRC + '%';

        if (info.FAR_HUP_PRC < 8) {
            $('.omilia-far-hup-progress-prc-reverse').text('- ' + info.FAR_HUP_PRC + '%');
        } else {
            $('.omilia-far-hup-progress-prc').text(info.FAR_HUP_PRC + '%');
        }

        if (info.NEAR_HUP_PRC < 8) {
            $('.omilia-near-hup-progress-prc-reverse').text('- ' + info.NEAR_HUP_PRC + '%');
        } else {
            $('.omilia-near-hup-progress-prc').text(info.NEAR_HUP_PRC + '%');
        }

        if (info.TRANSFER_PRC < 8) {
            $('.omilia-transfer-progress-prc-reverse').text('- ' + info.TRANSFER_PRC + '%');
        } else {
            $('.omilia-transfer-progress-prc').text(info.TRANSFER_PRC + '%');
        }

        if (step == 'first') {
            $('#z-omilia-online-all').spincrement({
                thousandSeparator: ",",
                duration: 1200
            });

            $('#z-omilia-online-far-hup').spincrement({
                thousandSeparator: ",",
                duration: 1200
            });

            $('#z-omilia-online-near-hup').spincrement({
                thousandSeparator: ",",
                duration: 1200
            });

            $('#z-omilia-online-transfer').spincrement({
                thousandSeparator: ",",
                duration: 1200
            });

        }

        if (hour != 0) {
            document.getElementById('z-omilia-online-avg-duration').style.fontSize = "35pt";
            $('#z-omilia-hour').text(hour);
            if (step == 'first') {
                $('#z-omilia-hour').spincrement({
                    thousandSeparator: ",",
                    duration: 1200
                });
            }
            $('#z-omilia-hour-text').text('час');
        }

        if (minute != 0 || hour != 0) {
            if (hour == 0) {
                document.getElementById('z-omilia-online-avg-duration').style.fontSize = "40pt";
            }
            $('#z-omilia-minute').text(minute);
            if (step == 'first') {
                $('#z-omilia-minute').spincrement({
                    thousandSeparator: ",",
                    duration: 1200
                });
            }
            $('#z-omilia-minute-text').text('мин');
        }

        $('#z-omilia-second').text(second);
        if (step == 'first') {
            $('#z-omilia-second').spincrement({
                thousandSeparator: ",",
                duration: 1200
            });
        }
        $('#z-omilia-second-text').text('сек');


        $('#z-omilia-service-level2').text(info.SERVICE_LEVEL);
        if (step == 'first') {
            $('#z-omilia-service-level2').spincrement({
                thousandSeparator: ",",
                duration: 1200
            });
        }
        
        // 2-й элемент общая сумма
        // 3-й элемент kz
        // 4-й элемент ru
        cards = ['Карточки','cards',0,0,0];
        homebank = ['Homebank','homebank',0,0,0];
        retail = ['Розница / Общие вопросы','retail',0,0,0];
        payments = ['Платежи и переводы','payments',0,0,0];
        credits = ['Новые кредиты (УТП)','credits',0,0,0];
        
        var total = 0,
            totalGetPrc = 0;

        for (index = 0; index < transfers.length; index++) {
            code = fgetVdnCode(transfers[index].vdn);
            cnt = transfers[index].cnt;

            if (code == 'cards_kz') {
                cards[2] += cnt;
                cards[3] = cnt;
                total += cnt;
            } else if (code == 'cards_ru') {
                cards[2] += cnt;
                cards[4] = cnt;
                total += cnt;
            }

            if (code == 'retail_kz') {
                retail[2] += cnt;
                retail[3] = cnt;
                total += cnt;
            } else if (code == 'retail_ru') {
                retail[2] += cnt;
                retail[4] = cnt;
                total += cnt;
            }

            if (code == 'payments_kz') {
                payments[2] += cnt;
                payments[3] = cnt;
                total += cnt;
            } else if (code == 'payments_ru') {
                payments[2] += cnt;
                payments[4] = cnt;
                total += cnt;
            }

            if (code == 'homebank_kz') {
                homebank[2] += cnt;
                homebank[3] = cnt;
                total += cnt;
            } else if (code == 'homebank_ru') {
                homebank[2] += cnt;
                homebank[4] = cnt;
                total += cnt;
            }

            if (code == 'credits_kz') {
                credits[2] += cnt;
                credits[3] = cnt;
                total += cnt;
            } else if (code == 'credits_ru') {
                credits[2] += cnt;
                credits[4] = cnt;
                total += cnt;
            }
        }
        
        nList = [cards, homebank, retail, payments, credits];

        for (step = 0; step < nList.length; step++) {
            var nprc;
            document.getElementById(nList[step][1] + '_cell_amount').textContent = numberWithCommas(nList[step][2]);
            document.getElementById(nList[step][1] + '_kz_cell_amount').textContent = numberWithCommas(nList[step][3]);
            document.getElementById(nList[step][1] + '_ru_cell_amount').textContent = numberWithCommas(nList[step][4]);
            document.getElementById(nList[step][1] + '_cell_prc').textContent = get_prc(nList[step][2], total) + '%';
            nprc = get_prc(nList[step][2], total);
            totalGetPrc += nprc;
            
            $('#' + nList[step][1] + '_kz_span').text('' + get_prc(nList[step][3], nList[step][2]) + '%' + '');
            $('#' + nList[step][1] + '_ru_span').text('' + get_prc(nList[step][4], nList[step][2]) + '%' + '');
            $('#total_sum_prc').text('' + totalGetPrc.toFixed(0) + '%' + '');

            tr2gr_groups[step] = nList[step][0];
            tr2gr_data[step] = nList[step][2];
            tr2gr_prc[step] = nprc;
        }

        document.getElementById('total_sum_count').textContent = numberWithCommas(total);

        $("#omilia-online-themes-dynamic").children().remove();
        $("#omilia-online-themes-static").children().remove();
        $("#omilia-online-themes-other").children().remove();

        var dynamic = 0,
            static = 0,
            other = 0,
            total_bwar = 0,
            total_ewar = 0,
            total_uwar = 0,
            total_bsuccess = 0,
            total_esuccess = 0,
            total_usuccess = 0;

        for (index = 0; index < themes.length; index++) {
            var value = fget_intent_longname(themes[index].theme);
              
            if (value[0] == 'Dynamic') {
                dynamic += 1;
                total_bwar += themes[index].cnt;
                total_bsuccess += themes[index].prc;
                $("<tr>").html("<td style='text-align: center; vertical-align:middle; min-width: 40px; max-width: 40px;'>" + dynamic + "</td>" +
                "<td style='text-align: center; vertical-align:middle; min-width: 100px; max-width: 100px;'>" + value[0] + "</td>" +
                "<td style='text-align: left; vertical-align:middle; min-width: 200px; max-width: 200px;'>" + value[1] + "</td>" +
                "<td style='text-align: center; vertical-align:middle; min-width: 100px; max-width: 100px;'>" + numberWithCommas(themes[index].cnt) + "</td>" +
                "<td style='text-align: center; vertical-align:middle; min-width: 200px; max-width: 200px;'>" + themes[index].prc + " %</td>").appendTo('#omilia-online-themes-dynamic')
            
            } else if (value[0] == 'Static') {
                static += 1;
                total_ewar += themes[index].cnt;
                total_esuccess += themes[index].prc;
                $("<tr>").html("<td style='text-align: center; vertical-align:middle; min-width: 40px; max-width: 40px;'>" + static + "</td>" +
                "<td style='text-align: center; vertical-align:middle; min-width: 100px; max-width: 100px;'>" + value[0] + "</td>" +
                "<td style='text-align: left; vertical-align:middle; min-width: 200px; max-width: 200px;'>" + value[1] + "</td>" +
                "<td style='text-align: center; vertical-align:middle; min-width: 100px; max-width: 100px;'>" + numberWithCommas(themes[index].cnt) + "</td>" +
                "<td style='text-align: center; vertical-align:middle; min-width: 200px; max-width: 200px;'>" + themes[index].prc + " %</td>").appendTo('#omilia-online-themes-static')
            
            } else {
                other += 1;
                total_uwar += themes[index].cnt;
                total_usuccess += themes[index].prc;
                $("<tr>").html("<td style='text-align: center; vertical-align:middle; min-width: 40px; max-width: 40px;'>" + other + "</td>" +
                "<td style='text-align: center; vertical-align:middle; min-width: 100px; max-width: 100px;'>" + value[0] + "</td>" +
                "<td style='text-align: left; vertical-align:middle; min-width: 200px; max-width: 200px;'>" + value[1] + "</td>" +
                "<td style='text-align: center; vertical-align:middle; min-width: 100px; max-width: 100px;'>" + numberWithCommas(themes[index].cnt) + "</td>" +
                "<td style='text-align: center; vertical-align:middle; min-width: 200px; max-width: 200px;'>" + themes[index].prc + " %</td>").appendTo('#omilia-online-themes-other')}
            }

            $("#omilia-online-themes-all").children().remove();
            
            var total_bsum = 0,
                total_bprc = 0;
            
        for (index = 0; index < themes.length; index++) {
            var value = fget_intent_longname(themes[index].theme)
            
            total_bsum += themes[index].cnt;
            total_bprc += themes[index].prc;
            $("<tr>").html("<td style='text-align: center; vertical-align:middle; min-width: 40px; max-width: 40px;'>" + (index + 1) + "</td>" +
                "<td style='text-align: center; vertical-align:middle; min-width: 100px; max-width: 100px;'>" + value[0] + "</td>" +
                "<td style='text-align: left; vertical-align:middle; min-width: 200px; max-width: 200px;'>" + value[1] + "</td>" +
                "<td style='text-align: center; vertical-align:middle; min-width: 100px; max-width: 100px;'>" + numberWithCommas(themes[index].cnt) + "</td>" +
                "<td style='text-align: center; vertical-align:middle; min-width: 200px; max-width: 200px;'>" + themes[index].prc + " %</td>"
            ).appendTo('#omilia-online-themes-all')
        }

            $("<tr style='border-top: 1px solid rgba(13, 27, 62, 0.7)'>").html("<td style='text-align: center; vertical-align:middle; min-width: 40px; max-width: 40px;'>-</td>" +
            "<td style='text-align: center; vertical-align:middle; font-weight: bold; min-width: 100px; max-width: 100px;'>Итого</td>" +
            "<td style='text-align: left; vertical-align:middle; font-weight: bold; min-width: 200px; max-width: 200px;'>&nbsp</td>"+
            "<td style='text-align: center; vertical-align:middle; font-weight: bold; min-width: 100px; max-width: 100px;'>" + numberWithCommas(total_bwar) + "</td>" +
            "<td style='text-align: center; vertical-align:middle; font-weight: bold; min-width: 200px; max-width: 200px;'>" + total_bsuccess.toFixed(0) + " %</td>"
            ).appendTo('#omilia-online-themes-dynamic');
                       
            $("<tr style='border-top: 1px solid rgba(13, 27, 62, 0.7)'>").html("<td style='text-align: center; vertical-align:middle; min-width: 40px; max-width: 40px;'>-</td>" +
            "<td style='text-align: center; vertical-align:middle; font-weight: bold; min-width: 100px; max-width: 100px;'>Итого</td>" +
            "<td style='text-align: left; vertical-align:middle; font-weight: bold; min-width: 200px; max-width: 200px;'>&nbsp</td>" +
            "<td style='text-align: center; vertical-align:middle; font-weight: bold; min-width: 100px; max-width: 100px;'>" + numberWithCommas(total_ewar) + "</td>" +
            "<td style='text-align: center; vertical-align:middle; font-weight: bold; min-width: 200px; max-width: 200px;'>" + total_esuccess.toFixed(0) + " %</td>"
            ).appendTo('#omilia-online-themes-static');

            $("<tr style='border-top: 1px solid rgba(13, 27, 62, 0.7)'>").html("<td style='text-align: center; vertical-align:middle; min-width: 40px; max-width: 40px;'>-</td>" +
            "<td style='text-align: center; vertical-align:middle; font-weight: bold; min-width: 100px; max-width: 100px;'>Итого</td>" +
            "<td style='text-align: left; vertical-align:middle; font-weight: bold; min-width: 200px; max-width: 200px;'>&nbsp</td>" +
            "<td style='text-align: center; vertical-align:middle; font-weight: bold; min-width: 100px; max-width: 100px;'>" + numberWithCommas(total_uwar) + "</td>" +
            "<td style='text-align: center; vertical-align:middle; font-weight: bold; min-width: 200px; max-width: 200px;'>" + total_usuccess.toFixed(0) + " %</td>"
            ).appendTo('#omilia-online-themes-other');

            $("<tr style='border-top: 1px solid rgba(13, 27, 62, 0.7)'>").html("<td style='text-align: center; vertical-align:middle; min-width: 40px; max-width: 40px;'>-</td>" +
            "<td style='text-align: center; vertical-align:middle; font-weight: bold; min-width: 100px; max-width: 100px;'>Итого</td>" +
            "<td style='text-align: left; vertical-align:middle; font-weight: bold; min-width: 200px; max-width: 200px;'>&nbsp</td>" +
            "<td style='text-align: center; vertical-align:middle; font-weight: bold; min-width: 100px; max-width: 100px;'>" + numberWithCommas(total_bsum) + "</td>" +
            "<td style='text-align: center; vertical-align:middle; font-weight: bold; min-width: 200px; max-width: 200px;'>" + total_bprc.toFixed(0) + " %</td>"
            ).appendTo('#omilia-online-themes-all');

        if (online_transfer_2gr) {
            if (OmiliaMedTran != undefined) {
                OmiliaMedTran.destroy();
            }
                         
            OmiliaMedTran = new Chart(online_transfer_2gr, {
                type: "doughnut",
                data: {
                    datasets: [{
                        data: tr2gr_prc,
                        backgroundColor: [window.chartColors.green, window.chartColors.orange, window.chartColors.red, window.chartColors.blue, window.chartColors.yellow, '#a51fc7', '#4510a8', '#17cc54', '#248596', '#8bd810'],
                        label: "Dataset 1"
                    }],
                    labels: tr2gr_groups
                },
                options: {
                    responsive: !0,
                    legend: {
                        position: "left"
                    },
                    title: {
                        display: !1,
                        text: "Chart.js Doughnut Chart"
                    },
                    animation: {
                        animateScale: 0,
                        animateRotate: 0
                    },
                    tooltips: {
                        callbacks: {
                            title: function() {
                                return '';
                            },
                            label: function(item, data) {
                                return tr2gr_groups[item.index] + ': ' + tr2gr_prc[item.index] + ' %';
                            }
                        }
                    }
                }
            });
        }


        $('#z-omilia-curr-date-time').text(getTime());

    }).fail(function(error) {
        console.error(error);
    });
}
var p_labels = [];
var p_data = [];

function omilia_online_service_level() {
    $.ajax({
        url: '/api/omilia/online/graphic',
        dataType: 'json',
        method: 'GET'
    }).
    done(function(data) {
        var info = data.result;
        var chLine = document.getElementById("chLine");
        var colors = ['#007bff', '#28a745', '#333333', '#c3e6cb', '#dc3545', '#6c757d'];

        if (p_labels.length == 14) {
            p_labels = []
            p_data = []
        }

        for (step = 0; step < info.length; step++) {
            var service_level = Math.round((Number(nvl(info[step].FAR_HUP, 0) + Number(nvl(info[step].NEAR_HUP, 0))) / info[step].TOTAL) * 100);

            p_labels[p_labels.length] = info[step].TIME
            p_data[p_data.length] = service_level
        }

        var chartData = {
            labels: p_labels,
            datasets: [{
                data: p_data,
                backgroundColor: colors[3],
                borderColor: colors[1],
                borderWidth: 4,
                pointBackgroundColor: colors[1]
            }]
        };

        if (chLine) {
            new Chart(chLine, {
                type: 'line',
                data: chartData,
                options: {
                    scales: {
                        yAxes: [{
                            ticks: {
                                beginAtZero: false
                            }
                        }]
                    },
                    legend: {
                        display: false
                    },
                    tooltips: {
                        callbacks: {
                            title: function() {
                                return '';
                            },
                            label: function(item, data) {
                                return 'Время: ' + data.labels[item.index] + '. Service level: ' + item.yLabel + ' %';
                            }
                        }
                    }
                }
            });
        }

    }).fail(function(error) {
        console.error(error);
    });
}

function omilia_history_data() {
    $.ajax({
        url: '/api/omilia/history',
        dataType: 'json',
        method: 'GET'
    }).
    done(function(data) {
        var info = data.main,
            step, nn,
            total_all = 0,
            total_success = 0,
            total_transfer = 0,
            total_success_prc = 0,
            total_transfer_prc = 0,
            total_far_hup = 0,
            total_near_hup = 0,
            p_far_hup,
            p_transfer,
            p_transfer_prc,
            p_near_hup;

        $("#z-omilia-offline-statistic").children().remove();
        document.getElementById("z-omilia-row-5").style.opacity = '1';

        for (step = 0; step < info.length; step++) {
            nn = step + 1;
            var doper = '"' + String(info[step].date) + '"',
                btnid = '"omilia_hst_btn_' + String(step) + '"',
                btnid1 = '"omilia_hst_btn_1' + String(step) + '"',
                transfers = '"transfers"',
                all = '"all"';

            if (typeof info[step]['FAR_HUP'] === "undefined") {
                p_far_hup = 0;
            } else {
                p_far_hup = info[step].FAR_HUP;
            }

            if (typeof info[step]['NEAR_HUP'] === "undefined") {
                p_near_hup = 0;
            } else {
                p_near_hup = info[step].NEAR_HUP;
            }

            if (typeof info[step]['TRANSFER'] === "undefined") {
                p_transfer = 0;
            } else {
                p_transfer = info[step].TRANSFER;
            }

            var p_all = p_far_hup + p_near_hup + p_transfer,
                p_success_prc = Math.round((p_far_hup + p_near_hup) / p_all * 100 * 100) / 100,
                p_transfer_prc = Math.round(p_transfer / p_all * 100 * 100) / 100,
                total_all = total_all + p_all;
                total_far_hup = total_far_hup + p_far_hup;
                total_near_hup = total_near_hup + p_near_hup;
                total_success = total_success + p_far_hup + p_near_hup;
                total_transfer = total_transfer + p_transfer;

            $("<tr>").html("<td style='text-align: center; vertical-align:middle'>" + nn + "</td>" +
                "<td style='text-align: center; vertical-align:middle; padding-top: 0px; padding-bottom: 0px;'>" +
                "<button class='border-0 btn-transition btn btn-outline-primary2' id='omilia_hst_btn_" + String(step) + "' onclick='double_tap(" + doper + ", " + btnid + ", " + all + ")' style='text-decoration: underline;'>" + (info[step].date) + "</td>" +
                "<td style='text-align: center; vertical-align:middle'>" + numberWithCommas(p_all) + "</td>" +
                "<td style='text-align: center; vertical-align:middle'>" + numberWithCommas(p_far_hup) + "</td>" +
                "<td style='text-align: center; vertical-align:middle'>" + numberWithCommas(p_near_hup) + "</td>" +
                "<td style='text-align: center; vertical-align:middle'>" + p_success_prc + " %</td>" +
                "<td style='text-align: center; vertical-align:middle; padding-top: 0px; padding-bottom: 0px;'>" + 
                "<button class='border-0 btn-transition btn btn-outline-primary2' id='omilia_hst_btn_1" + String(step) + "' onclick='double_tap(" + doper + ", " + btnid1 + ", " + transfers + ")' style='text-decoration: underline;'>" + numberWithCommas(p_transfer) + "</td>" +
                "<td style='text-align: center; vertical-align:middle'>" + p_transfer_prc + " %</td>"
            ).appendTo('#z-omilia-offline-statistic')
        }
          
        total_success_prc = Math.round(total_success / total_all * 100 * 100) / 100;
        total_transfer_prc = Math.round(total_transfer / total_all * 100 * 100) / 100;
        
        $("<tr style='border-top: 1px solid rgba(13, 27, 62, 0.7)'>").html("<td style='text-align: center; vertical-align:middle'>-</td>" +
            "<td style='text-align: center; vertical-align:middle; font-weight: bold;'>Итого</td>" +
            "<td style='text-align: center; vertical-align:middle; font-weight: bold;'>" + numberWithCommas(total_all) + "</td>" +
            "<td style='text-align: center; vertical-align:middle; font-weight: bold;'>" + numberWithCommas(total_far_hup) + "</td>" +
            "<td style='text-align: center; vertical-align:middle; font-weight: bold;'>" + numberWithCommas(total_near_hup) + "</td>" +
            "<td style='text-align: center; vertical-align:middle; font-weight: bold;'>" + total_success_prc + " %</td>" +
            "<td style='text-align: center; vertical-align:middle; font-weight: bold;'>" + numberWithCommas(total_transfer) + "</td>" +
            "<td style='text-align: center; vertical-align:middle; font-weight: bold;'>" + total_transfer_prc + " %</td>"
        ).appendTo('#z-omilia-offline-statistic');

        // Трансферы
        var info = data.transfers.result,
            total = data.transfers.total,
            omilia_transfer = document.getElementById("z-omilia-canvas-transfer-2gr"),
            omilia_skill_groups = [],
            omilia_skill_data = [],
            omilia_skill_data_prc = [];

        document.getElementById("z-omilia-column-tr-2gr").style.opacity = '1';

        // 2-й элемент общая сумма
        // 3-й элемент kz
        // 4-й элемент ru
        cards = ['Карточки','cards',0,0,0];
        homebank = ['Homebank','homebank',0,0,0];
        retail = ['Розница / Общие вопросы','retail',0,0,0];
        payments = ['Платежи и переводы','payments',0,0,0];
        credits = ['Новые кредиты (УТП)','credits',0,0,0];
        
        var total = 0,
        totalGetPrc = 0;
        for (index = 0; index < info.length; index++) {
            code = fgetVdnCode(info[index].point);
            cnt = info[index].cnt;

            if (code == 'cards_kz') {
                cards[2] += cnt;
                cards[3] = cnt;
                total += cnt
            } else if (code == 'cards_ru') {
                cards[2] += cnt;
                cards[4] = cnt;
                total += cnt;
            }

            if (code == 'retail_kz') {
                retail[2] += cnt;
                retail[3] = cnt;
                total += cnt
            } else if (code == 'retail_ru') {
                retail[2] += cnt;
                retail[4] = cnt;
                total += cnt
            }

            if (code == 'payments_kz') {
                payments[2] += cnt;
                payments[3] = cnt;
                total += cnt
            } else if (code == 'payments_ru') {
                payments[2] += cnt;
                payments[4] = cnt;
                total += cnt
            }

            if (code == 'homebank_kz') {
                homebank[2] += cnt;
                homebank[3] = cnt;
                total += cnt
            } else if (code == 'homebank_ru') {
                homebank[2] += cnt;
                homebank[4] = cnt;
                total += cnt
            }

            if (code == 'credits_kz') {
                credits[2] += cnt;
                credits[3] = cnt;
                total += cnt
            } else if (code == 'credits_ru') {
                credits[2] += cnt;
                credits[4] = cnt;
                total += cnt
            }
        }
        
        nList = [cards, homebank, retail, payments, credits];

        for (step = 0; step < nList.length; step++) {
            document.getElementById(nList[step][1] + '_cell_amount_ten').textContent = numberWithCommas(nList[step][2]);
            document.getElementById(nList[step][1] + '_kz_cell_amount_ten').textContent = numberWithCommas(nList[step][3]);
            document.getElementById(nList[step][1] + '_ru_cell_amount_ten').textContent = numberWithCommas(nList[step][4]);
            document.getElementById(nList[step][1] + '_cell_prc_ten').textContent = get_prc(nList[step][2], total) + '%';
            let prcReader = get_prc(nList[step][2], total);
            totalGetPrc += prcReader;
            
            $('#' + nList[step][1] + '_kz_span_ten').text('' + get_prc(nList[step][3], nList[step][2]) + '%' + '');
            $('#' + nList[step][1] + '_ru_span_ten').text('' + get_prc(nList[step][4], nList[step][2]) + '%' + '');
            $('#total_sum_prc_ten').text('' + totalGetPrc.toFixed(0) + '%' + '');

            omilia_skill_groups[step] = nList[step][0];
            omilia_skill_data[step] = nList[step][2];
            omilia_skill_data_prc[step] = prcReader;
        }

        document.getElementById('total_sum_count_ten').textContent = numberWithCommas(total);

        if (omilia_transfer) {
            
            new Chart(omilia_transfer, {
                type: "doughnut",
                data: {
                    datasets: [{
                        data: omilia_skill_data_prc,
                        backgroundColor: [window.chartColors.green, window.chartColors.orange, window.chartColors.red, window.chartColors.blue, window.chartColors.yellow, '#a51fc7', '#4510a8', '#17cc54', '#248596', '#8bd810'],
                        label: "Dataset 1"
                    }],
                    labels: omilia_skill_groups
                },
                options: {
                    responsive: !0,
                    legend: {
                        position: "left"
                    },
                    title: {
                        display: !1,
                        text: "Chart.js Doughnut Chart"
                    },
                    animation: {
                        animateScale: !0,
                        animateRotate: !0
                    },
                    tooltips: {
                        callbacks: {
                            title: function() {
                                return '';
                            },
                            label: function(item, data) {
                                return omilia_skill_groups[item.index] + ': ' + omilia_skill_data_prc[item.index] + ' %';
                            }
                        }
                    }
                }
            });
        }

        // Темы обращения
        var info = data.themes.result,
            total = data.themes.total,
            omilia_topic_element = document.getElementById("z-omilia-topic-of-appeal"),
            theme = [],
            omilia_themes_data = [],
            omilia_themes_data_prc = [],
            dynamic = 0,
            static = 0,
            other = 0,
            total_tem_dyn = 0,
            total_tem_sta = 0,
            total_tem_oth = 0,
            total_tem_dprc = 0,
            total_tem_sprc = 0,
            total_tem_oprc = 0;

        $("#z-omilia-themes-dyn").children().remove();
        $("#z-omilia-themes-sta").children().remove();
        $("#z-omilia-themes-oth").children().remove();
        document.getElementById("z-omilia-row-6").style.opacity = '1';

        for (step = 0; step < info.length; step++) {
            var themes_data = fget_intent_longname(info[step].intent);

            nn = step + 1;
            theme[step] = themes_data[1]
            omilia_themes_data[step] = info[step].cnt;
            omilia_themes_data_prc[step] = Math.round(info[step].cnt / total * 100 * 100) / 100
            
            if (themes_data[0] == 'Dynamic') {
                dynamic += 1;
                total_tem_dyn += info[step].cnt;
                total_tem_dprc += omilia_themes_data_prc[step];
            $("<tr>").html("<td style='text-align: center; vertical-align:middle; min-width: 40px; max-width: 40px;'>" + dynamic + "</td>" +
                "<td style='text-align: center; vertical-align:middle; min-width: 100px; max-width: 100px;'>" + themes_data[0] + "</td>" +
                "<td style='text-align: left; vertical-align:middle; min-width: 200px; max-width: 200px;'>" + theme[step] + "</td>" +
                "<td style='text-align: center; vertical-align:middle; min-width: 100px; max-width: 100px;'>" + numberWithCommas(omilia_themes_data[step]) + "</td>" +
                "<td style='text-align: center; vertical-align:middle; min-width: 200px; max-width: 200px;'>" + omilia_themes_data_prc[step] + " %</td>"
            ).appendTo('#z-omilia-themes-dyn')
            
            } else if (themes_data[0] == 'Static'){
                static += 1;
                total_tem_sta += info[step].cnt;
                total_tem_sprc += omilia_themes_data_prc[step];
            $("<tr>").html("<td style='text-align: center; vertical-align:middle; min-width: 40px; max-width: 40px;'>" + static + "</td>" +
                "<td style='text-align: center; vertical-align:middle; min-width: 100px; max-width: 100px;'>" + themes_data[0] + "</td>" +
                "<td style='text-align: left; vertical-align:middle; min-width: 200px; max-width: 200px;'>" + theme[step] + "</td>" +
                "<td style='text-align: center; vertical-align:middle; min-width: 100px; max-width: 100px;'>" + numberWithCommas(omilia_themes_data[step]) + "</td>" +
                "<td style='text-align: center; vertical-align:middle; min-width: 200px; max-width: 200px;'>" + omilia_themes_data_prc[step] + " %</td>"
            ).appendTo('#z-omilia-themes-sta')
            
            } else{
                other += 1; 
                total_tem_oth += info[step].cnt;
                total_tem_oprc += omilia_themes_data_prc[step];
            $("<tr>").html("<td style='text-align: center; vertical-align:middle; min-width: 40px; max-width: 40px;'>" + other + "</td>" +
                "<td style='text-align: center; vertical-align:middle; min-width: 100px; max-width: 100px;'>" + themes_data[0] + "</td>" +
                "<td style='text-align: left; vertical-align:middle; min-width: 200px; max-width: 200px;'>" + theme[step] + "</td>" +
                "<td style='text-align: center; vertical-align:middle; min-width: 100px; max-width: 100px;'>" + numberWithCommas(omilia_themes_data[step]) + "</td>" +
                "<td style='text-align: center; vertical-align:middle; min-width: 200px; max-width: 200px;'>" + omilia_themes_data_prc[step] + " %</td>"
            ).appendTo('#z-omilia-themes-oth')}
        }
        
        var total_th_sum = 0,
            total_th_sprc = 0;

        for (step = 0; step < info.length; step++) {
            var themes_data = fget_intent_longname(info[step].intent);

            total_th_sum += info[step].cnt;
            total_th_sprc += omilia_themes_data_prc[step];

            nn = step + 1;
            theme[step] = themes_data[1]
            omilia_themes_data[step] = info[step].cnt;
            omilia_themes_data_prc[step] = Math.round(info[step].cnt / total * 100 * 100) / 100

            $("<tr>").html("<td style='text-align: center; vertical-align:middle; min-width: 40px; max-width: 40px;'>" + nn + "</td>" +
                "<td style='text-align: center; vertical-align:middle; min-width: 100px; max-width: 100px;'>" + themes_data[0] + "</td>" +
                "<td style='text-align: left; vertical-align:middle; min-width: 200px; max-width: 200px;'>" + theme[step] + "</td>" +
                "<td style='text-align: center; vertical-align:middle; min-width: 100px; max-width: 100px;'>" + numberWithCommas(omilia_themes_data[step]) + "</td>" +
                "<td style='text-align: center; vertical-align:middle; min-width: 200px; max-width: 200px;'>" + omilia_themes_data_prc[step] + " %</td>"
            ).appendTo('#z-omilia-themes-all')
        }
        
            $("<tr style='border-top: 1px solid rgba(13, 27, 62, 0.7)'>").html("<td style='text-align: center; vertical-align:middle; min-width: 40px; max-width: 40px;'>-</td>" +
            "<td style='text-align: center; vertical-align:middle; font-weight: bold; min-width: 100px; max-width: 100px;'>Итого</td>" +
            "<td style='text-align: center; vertical-align:middle; font-weight: bold; min-width: 200px; max-width: 200px;'>&nbsp</td>"+
            "<td style='text-align: center; vertical-align:middle; font-weight: bold; min-width: 100px; max-width: 100px;'>" + numberWithCommas(total_tem_dyn) + "</td>" +
            "<td style='text-align: center; vertical-align:middle; font-weight: bold; min-width: 200px; max-width: 200px;'>" + total_tem_dprc.toFixed(0) + " %</td>"
            ).appendTo('#z-omilia-themes-dyn');
                       
            $("<tr style='border-top: 1px solid rgba(13, 27, 62, 0.7)'>").html("<td style='text-align: center; vertical-align:middle; min-width: 40px; max-width: 40px;'>-</td>" +
            "<td style='text-align: center; vertical-align:middle; font-weight: bold; min-width: 100px; max-width: 100px;'>Итого</td>" +
            "<td style='text-align: center; vertical-align:middle; font-weight: bold; min-width: 200px; max-width: 200px;'>&nbsp</td>" +
            "<td style='text-align: center; vertical-align:middle; font-weight: bold; min-width: 100px; max-width: 100px;'>" + numberWithCommas(total_tem_sta) + "</td>" +
            "<td style='text-align: center; vertical-align:middle; font-weight: bold; min-width: 200px; max-width: 200px;'>" + total_tem_sprc.toFixed(0) + " %</td>"
            ).appendTo('#z-omilia-themes-sta');

            $("<tr style='border-top: 1px solid rgba(13, 27, 62, 0.7)'>").html("<td style='text-align: center; vertical-align:middle; min-width: 40px; max-width: 40px;'>-</td>" +
            "<td style='text-align: center; vertical-align:middle; font-weight: bold; min-width: 100px; max-width: 100px;'>Итого</td>" +
            "<td style='text-align: center; vertical-align:middle; font-weight: bold; min-width: 200px; max-width: 200px;'>&nbsp</td>" +
            "<td style='text-align: center; vertical-align:middle; font-weight: bold; min-width: 100px; max-width: 100px;'>" + numberWithCommas(total_tem_oth) + "</td>" +
            "<td style='text-align: center; vertical-align:middle; font-weight: bold; min-width: 200px; max-width: 200px;'>" + total_tem_oprc.toFixed(0) + " %</td>"
            ).appendTo('#z-omilia-themes-oth');

            $("<tr style='border-top: 1px solid rgba(13, 27, 62, 0.7)'>").html("<td style='text-align: center; vertical-align:middle; min-width: 40px; max-width: 40px;'>-</td>" +
            "<td style='text-align: center; vertical-align:middle; font-weight: bold; min-width: 100px; max-width: 100px;'>Итого</td>" +
            "<td style='text-align: center; vertical-align:middle; font-weight: bold; min-width: 200px; max-width: 200px;'>&nbsp</td>" +
            "<td style='text-align: center; vertical-align:middle; font-weight: bold; min-width: 100px; max-width: 100px;'>" + numberWithCommas(total_th_sum) + "</td>" +
            "<td style='text-align: center; vertical-align:middle; font-weight: bold; min-width: 200px; max-width: 200px;'>" + total_th_sprc.toFixed(0) + " %</td>"
            ).appendTo('#z-omilia-themes-all');

            if (omilia_topic_element) {
                new Chart(omilia_topic_element, {
                    type: "doughnut",
                    data: {
                        datasets: [{
                            data: omilia_themes_data_prc,
                            backgroundColor: ['#008B8B',
                                window.chartColors.yellow,
                                window.chartColors.grey,
                                window.chartColors.red,
                                window.chartColors.blue,
                                window.chartColors.orange,
                                '#BA55D3',
                                '#FF69B4',
                                '#A52A2A',
                                '#008000',
                                '#8A2BE2',
                            ],
                            label: "Dataset 1"
                        }],
                        labels: theme
                    },
                    options: {
                        responsive: !0,
                        legend: {
                            position: "left"
                        },
                        animation: {
                            animateScale: !0,
                            animateRotate: !0
                        },
                        tooltips: {
                            callbacks: {
                                title: function() {
                                    return '';
                                },
                                label: function(item, data) {
                                    return theme[item.index] + ': ' + omilia_themes_data_prc[item.index] + ' %';
                                }
                            }
                        }
                    }
                });
            }

    }).fail(function(error) {
        console.error(error);
    });
}


function OmiliaPressBtn(value) {
    document.getElementById(OMILIA_BTN_LST).classList.remove('active');
    document.getElementById(OMILIA_BTN_LST).style.display='inherit';
    document.getElementById(value).style.display='None';
    OMILIA_BTN_LST = value;
    var text = $('#' + value).text();

    $('#btn_destr').text(text);    
}

function OmiliaPressBtnTen(value) {
    document.getElementById(OMILIA_BTN_LST_TEN).classList.remove('active');
    document.getElementById(OMILIA_BTN_LST_TEN).style.display='inherit';
    document.getElementById(value).style.display='None';
    OMILIA_BTN_LST_TEN = value;
    var text = $('#' + value).text();
    $('#btn_destr_ten').text(text);    
}

function myFunction() {
    document.getElementById("myDropdown").classList.toggle("show");
}

function myFunctionTen() {
    document.getElementById("myDropdownTen").classList.toggle("show");
}

window.onclick = function(event) {
  if (!event.target.matches('.dropbtn')) {

    var dropdowns = document.getElementsByClassName("dropdown-content");
    var i;
    for (i = 0; i < dropdowns.length; i++) {
      var openDropdown = dropdowns[i];
      if (openDropdown.classList.contains('show')) {
        openDropdown.classList.remove('show');
      }
    }
  }
}

function multiTap(idBtn) {
    let newLet,
    newHomebank,
    newRetail,
    newPayments,
    newCredits;
    
    newLet = document.getElementById('hide_field_cards_kz').style.display;
    newHomebank = document.getElementById('hide_field_hb_kz').style.display;
    newRetail = document.getElementById('hide_field_rt_kz').style.display;
    newPayments = document.getElementById('hide_field_pay_kz').style.display;
    newCredits = document.getElementById('hide_field_cr_kz').style.display;

    if (idBtn == 'cards_all') {
        document.getElementById('hide_field_cards_kz').style.display='';
        document.getElementById('hide_field_cards_ru').style.display='';
    } else if (idBtn == 'homebank_all') {
        document.getElementById('hide_field_hb_kz').style.display='';
        document.getElementById('hide_field_hb_ru').style.display='';
    } else if (idBtn == 'retail_all') {
        document.getElementById('hide_field_rt_kz').style.display='';
        document.getElementById('hide_field_rt_ru').style.display='';
    } else if (idBtn == 'payments_all') {
        document.getElementById('hide_field_pay_kz').style.display='';
        document.getElementById('hide_field_pay_ru').style.display='';
    } else if (idBtn == 'credits_all') {
        document.getElementById('hide_field_cr_kz').style.display='';
        document.getElementById('hide_field_cr_ru').style.display='';
    }

    if (newLet == '' && idBtn == 'cards_all') {
        document.getElementById('hide_field_cards_kz').style.display='none';
        document.getElementById('hide_field_cards_ru').style.display='none';
    } else if (newHomebank == '' && idBtn == 'homebank_all') {
        document.getElementById('hide_field_hb_kz').style.display='none';
        document.getElementById('hide_field_hb_ru').style.display='none';
    } else if (newRetail == '' && idBtn == 'retail_all') {
        document.getElementById('hide_field_rt_kz').style.display='none';
        document.getElementById('hide_field_rt_ru').style.display='none';
    } else if (newPayments == '' && idBtn == 'payments_all') {
        document.getElementById('hide_field_pay_kz').style.display='none';
        document.getElementById('hide_field_pay_ru').style.display='none';
    } else if (newCredits == '' && idBtn == 'credits_all') {
        document.getElementById('hide_field_cr_kz').style.display='none';
        document.getElementById('hide_field_cr_ru').style.display='none';
    }


    newLet = document.getElementById('hide_field_cards_kz_ten').style.display;
    newHomebank = document.getElementById('hide_field_hb_kz_ten').style.display;
    newRetail = document.getElementById('hide_field_rt_kz_ten').style.display;
    newPayments = document.getElementById('hide_field_pay_kz_ten').style.display;
    newCredits = document.getElementById('hide_field_cr_kz_ten').style.display;

    if (idBtn == 'cards_all_ten') {
        document.getElementById('hide_field_cards_kz_ten').style.display='';
        document.getElementById('hide_field_cards_ru_ten').style.display='';
    } else if (idBtn == 'homebank_all_ten') {
        document.getElementById('hide_field_hb_kz_ten').style.display='';
        document.getElementById('hide_field_hb_ru_ten').style.display='';
    } else if (idBtn == 'retail_all_ten') {
        document.getElementById('hide_field_rt_kz_ten').style.display='';
        document.getElementById('hide_field_rt_ru_ten').style.display='';
    } else if (idBtn == 'payments_all_ten') {
        document.getElementById('hide_field_pay_kz_ten').style.display='';
        document.getElementById('hide_field_pay_ru_ten').style.display='';
    } else if (idBtn == 'credits_all_ten') {
        document.getElementById('hide_field_cr_kz_ten').style.display='';
        document.getElementById('hide_field_cr_ru_ten').style.display='';
    }

    if (newLet == '' && idBtn == 'cards_all_ten') {
        document.getElementById('hide_field_cards_kz_ten').style.display='none';
        document.getElementById('hide_field_cards_ru_ten').style.display='none';
    } else if (newHomebank == '' && idBtn == 'homebank_all_ten') {
        document.getElementById('hide_field_hb_kz_ten').style.display='none';
        document.getElementById('hide_field_hb_ru_ten').style.display='none';
    } else if (newRetail == '' && idBtn == 'retail_all_ten') {
        document.getElementById('hide_field_rt_kz_ten').style.display='none';
        document.getElementById('hide_field_rt_ru_ten').style.display='none';
    } else if (newPayments == '' && idBtn == 'payments_all_ten') {
        document.getElementById('hide_field_pay_kz_ten').style.display='none';
        document.getElementById('hide_field_pay_ru_ten').style.display='none';
    } else if (newCredits == '' && idBtn == 'credits_all_ten') {
        document.getElementById('hide_field_cr_kz_ten').style.display='none';
        document.getElementById('hide_field_cr_ru_ten').style.display='none';
    }
}