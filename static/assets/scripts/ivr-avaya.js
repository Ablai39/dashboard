function getIvrDetailData(doper, btnid) {
    if (IVR_HST_BTN != '') {
        document.getElementById(IVR_HST_BTN).classList.remove('active');
    }

    document.getElementById(btnid).classList.add('active');
    IVR_HST_BTN = btnid;
    ivr2020_history_detail(doper);
}

function ivr_online(step) {
    $.ajax({
        url: '/api/ivr/online',
        method: 'GET'
    }).
    done(function(data) {
        if (typeof data['status'] == 'undefined') {
            console.log('Ошибка в сервисе: /api/ivr/online');
        }

        else {
            if (data.status != 'successful') {
                console.log('Ошибка в сервисе: /api/ivr/online: ' + String(data.status));
            }

            else {
                var info = data.result

                $('#z-ivr-curr-date-time').text(getTime());

                $('.zdk-success').text(numberWithCommas(info.successful));
                if (step == 'first') {
                    $('.zdk-success').spincrement({
                        thousandSeparator: ",",
                        duration: 1200
                    });
                }

                $('.zdk-success-progress').text(numberWithCommas(info.successful) + ' из ' + numberWithCommas(info.all));
                $('.zdk-success-progress-prc').text(info.successful_prc + '%');
                document.getElementById('progress-bar-success-id').style.width = info.successful_prc + '%';

                $('.zdk-transfer').text(numberWithCommas(info.transfered));
                if (step == 'first') {
                    $('.zdk-transfer').spincrement({
                        thousandSeparator: ",",
                        duration: 1200
                    });
                }

                $('.zdk-transfer-progress').text(numberWithCommas(info.transfered) + ' из ' + numberWithCommas(info.all));
                $('.zdk-transfer-progress-prc').text(info.transfered_prc + '%');
                document.getElementById('progress-bar-transfer-id').style.width = info.transfered_prc + '%';

                $('.zdk-break').text(numberWithCommas(info.breaked));
                if (step == 'first') {
                    $('.zdk-break').spincrement({
                        thousandSeparator: ",",
                        duration: 1200
                    });
                }

                $('.zdk-break-progress').text(numberWithCommas(info.breaked) + ' из ' + numberWithCommas(info.all));
                $('.zdk-break-progress-prc').text(info.breaked_prc + '%');
                document.getElementById('progress-bar-break-id').style.width = info.breaked_prc + '%';
            }
        }
    }).
    fail(function(error) {
        console.warn(error);
    });
}

function ivr_history_data() {
    $.ajax({
        url: '/api/ivr/history',
        dataType: 'json',
        method: 'GET'
    }).
    done(function(data) {
        if (typeof data['status'] == 'undefined') {
            console.log('Ошибка в сервисе: /api/ivr/history');
        }

        else {
            if (data.status != 'successful') {
                console.log('Ошибка в сервисе: /api/ivr/history: ' + String(data.status));
            }

            else {
                var info = data.result,
                step, nn;
                $("#z-ivr-offline-statistic").children().remove();
                document.getElementById("z-ivr-row-4").style.opacity = '1';
        
                for (step = 0; step < info.length; step++) {
                    nn = step + 1;
                    var doper = String(info[step].date), 
                        btnid = 'ivr_hst_btn_' + String(step),
                        doperFrmt = '"' + doper +'"',
                        btnidFrmt = '"' + btnid + '"';
        
                    $("<tr>").html("<th scope='row' style='font-weight: normal;'>" + nn + "</th>" +
                        "<td style='text-align: center; vertical-align:middle; padding-top: 0px; padding-bottom: 0px;'>" +
                        "<button class='border-0 btn-transition btn btn-outline-primary2' id='ivr_hst_btn_" + String(step) + "' onclick='getIvrDetailData(" + doperFrmt + ", " + btnidFrmt + ")' style='text-decoration: underline; cursor: pointer; font-size: .88rem'>" + (info[step].date) + "</td>" +
                        "<td style='text-align: center; vertical-align:middle'>" + numberWithCommas(info[step].all) + "</td>" +
                        "<td style='text-align: center; vertical-align:middle'>" + numberWithCommas(info[step].successful) + "</td>" +
                        "<td style='text-align: center; vertical-align:middle'>" + info[step].successful_prc + " %</td>" +
                        "<td style='text-align: center; vertical-align:middle'>" + numberWithCommas(info[step].break) + "</td>" +
                        "<td style='text-align: center; vertical-align:middle'>" + numberWithCommas(info[step].transfer) + "</td>" +
                        "<td style='text-align: center; vertical-align:middle'>" + info[step].transfer_prc + " %</td>"
                    ).appendTo('#z-ivr-offline-statistic')
                
                    if (step == 0) {
                        if (IVR_HST_BTN == '') {
                            getIvrDetailData(doper, btnid);
                        }
                    }
                }
            }
        }
    }).fail(function(error) {
        console.error(error);
    });
}

function IvrCloseModal() {
    document.getElementById("IvrModal").style.display = 'none';
}

function ivr2020_history_detail(doper) {
    document.getElementById("IvrModalLoader").style.display = 'block';

    $.ajax({
        url: '/api/ivr2020/history?doper=' + doper,
        dataType: 'json',
        method: 'GET'
    }).
    done(function(data) {
        document.getElementById("IvrModalLoader").style.display = 'none';

        if (typeof data['status'] == 'undefined') {
            console.log('Ошибка в сервисе: /api/ivr2020/history');
        }

        else {
            if (data.status != 'successful') {
                console.log('Ошибка в сервисе: /api/ivr2020/history: ' + String(data.status));
            }

            else {
                var info = data.data,
                    SelfServices = data.data.SelfServices,
                    Languages = data.data.Languages,
                    CallStatus = data.data.CallStatus,
                    PhoneFL = data.data.PhoneFL,
                    MenuTree_MM = data.data.MenuTree_MM,
                    MenuTree_MCS = data.data.MenuTree_MCS,
                    index, nn, prc, dictCode;

                if (CallStatus.Total == 0) {
                    document.getElementById("z-ivr-row-5").style.opacity = '0';
                    document.getElementById("z-ivr-row-6").style.opacity = '0';
                    document.getElementById("IvrModalDoper").textContent = doper;
                    document.getElementById("IvrModal").style.display = 'block';
                
                } else {
                    function getSelfServiceLongname(code) {
                        if (code == 'infoCardBalance') return 'Баланс по карте'
                        else if (code == 'infoCredits') return 'Информация по кредиту'
                        else if (code == 'infoAccountBalance') return 'Баланс по текущему счету'
                        else if (code == 'infoArrests') return 'Информация по арестам'
                        else if (code == 'infoOverdueCredits') return 'Информация по просроченному кредиту'
                        else if (code == 'CardBlock') return 'Блокировка карты'
                        else if (code == 'infoOverdueCreditCards') return 'Информация по просроченной кредитной карте'
                        else if (code == 'CardRemoveLimits') return 'Снятие лимитов по карте'
                        else if (code == 'CardClearPinAttempts') return 'Обнуление попыток ввода PIN кода по карте'
                        else if (code == 'CardGetEPin') return 'Получение временного PIN кода по карте'
                        else if (code == 'infoCreditCards') return 'Информация по кредитной карте'
                        else if (code == 'OtsroshkaSiteURLSendSMS') return 'Получение SMS с ссылкой на сайт по отсрочке кредитов'
                        else return code;
                    };
    
                    function getLanguageLongname(code) {
                        if (code == 'kaz') return 'На казахском'
                        else if (code == 'rus') return 'На русском'
                        else if (code == 'eng') return 'На английском'
                        else return code;
                    };
    
                    function getPhoneTypeLongname(code) {
                        if (code == 'FL_Mobile') return 'Мобильных номеров'
                        else if (code == 'FL_TrustedNumber') return 'Доверенных номеров'
                        else return code;
                    }
    
                    function getMMLongname(code) {
                        if (code == 'MM_InfoArrests') return 'Информация по арестам, нажмите 1'
                        else if (code == 'MM_InfoOvdCreditsCredCards') return 'Информация по просроченному кредиту/кредитной карте, нажмите 2'
                        else if (code == 'MM_CardServices') return 'Сервисы по карте, нажмите 3'
                        else if (code == 'MM_OtsroshkaCredits') return 'Отсрочка по кредиту, нажмите 4'
                        else if (code == 'MM_InfoCreditsCredCards') return 'Информация по действующему кредиту/кредитной карте, нажмите 5'
                        else if (code == 'MM_SalesCredit') return 'Оформление нового кредита/кредитной карты, нажмите 6'
                        else if (code == 'MM_InfoCardBalance') return 'Баланс по карте, нажмите 7'
                        else if (code == 'MM_InfoAccBalance') return 'Баланс по текущему счету, нажмите 8'
                        else if (code == 'MM_ConnToOperator') return 'Соединение с консультантом, нажмите 0'
                        else if (code == 'MM_InfoCredits') return 'Информация по действующему кредиту'
                        else if (code == 'MM_InfoCreditCards') return 'Информация по действующей кредитной карте'
                        else if (code == 'MM_InfoOvdCreditCards') return 'Информация по просроченной кредитной карте'
                        else if (code == 'MM_InfoOvdCredits') return 'Информация по просроченному кредиту'
                        else return code;
                    }
    
                    function getMCSLongname(code) {
                        if (code == 'MCS_CardBlock') return 'Блокировка карты, нажмите 1'
                        else if (code == 'MCS_CardGetEPin') return 'Получение временного PIN кода по карте, нажмите 2'
                        else if (code == 'MCS_CardDostavka') return 'Информация по доставке карт, нажмите 3'
                        else if (code == 'MCS_CardClearPinAtt') return 'Обнуление попыток ввода PIN кода по карте, нажмите 4'
                        else if (code == 'MCS_CardRemoveLimits') return 'Снятие лимитов по карте, нажмите 6'
                        else if (code == 'MCS_CardBalance') return 'Баланс по карте, нажмите 7'
                        else if (code == 'MCS_CardZabytayaATM') return 'Информация по забытым картам в АТМ, нажмите 8'
                        else return code;
                    }
                    
                    $("#ivr-detail-data").children().remove();
                    $("#ivrDetail-MenuTree-MM").children().remove();
                    $("#ivrDetail-MenuTree-MCS").children().remove();
                    document.getElementById("z-ivr-row-5").style.opacity = '1';
                    document.getElementById("z-ivr-row-6").style.opacity = '1';
                    document.getElementById('ivr-detail-doper').textContent = info.Doper;
    
                    nn = 0;
                    for (index = 0; index < Object.keys(SelfServices).length; index++) {
                        dictCode = Object.keys(SelfServices)[index];
                        prc = get_prc(SelfServices[dictCode], SelfServices['Total']);
    
                        if (dictCode == 'Total') continue;
                        nn += 1;
    
                        $("<tr>").html("<th scope='row' style='text-align: center; font-weight: normal;'>" + nn + "</th>" +
                            "<td style='text-align: left; vertical-align:middle'>" + getSelfServiceLongname(dictCode) + "</td>" +
                            "<td style='text-align: center; vertical-align:middle'>" + numberWithCommas(SelfServices[dictCode]) + "</td>" +
                            "<td style='text-align: center; vertical-align:middle'>" + prc + " %</td>"
                        ).appendTo('#ivr-detail-data')
                    }
    
                    document.getElementById('ivrDetail-CallStatusTotal').textContent = numberWithCommas(CallStatus['Total']);
                    $('#ivrDetail-CallStatusTotal').spincrement({
                        thousandSeparator: ",",
                        duration: 1200
                    });
    
                    for (index = 0; index < Object.keys(CallStatus).length; index++) {
                        dictCode = Object.keys(CallStatus)[index];
    
                        if (dictCode == 'Total') continue;
                        prc = get_prc(CallStatus[dictCode], CallStatus.Total);
                        
                        document.getElementById('ivrDetail-CallStatus'+dictCode+'Prc').textContent = prc;
                        $('#ivrDetail-CallStatus'+dictCode+'Prc').spincrement({
                            thousandSeparator: ",",
                            duration: 1200
                        });
                        document.getElementById('ivrDetail-CallStatus'+dictCode).textContent = numberWithCommas(CallStatus[dictCode]) + ' из ' + numberWithCommas(CallStatus.Total);
                        document.getElementById('ivrDetail-pBar-CallStatus'+dictCode).style.width = prc + '%';
                    }
    
                    var TrustedPhonePrc = get_prc(PhoneFL.FL_TrustedNumber, CallStatus.Total);
                    document.getElementById('ivrDetail-TrustedPhonePrc').textContent = TrustedPhonePrc;
                    $('#ivrDetail-TrustedPhonePrc').spincrement({
                        thousandSeparator: ",",
                        duration: 1200
                    });
                    document.getElementById('ivrDetail-TrustedPhone').textContent = numberWithCommas(PhoneFL.FL_TrustedNumber) + ' из ' + numberWithCommas(CallStatus.Total);
                    document.getElementById('ivrDetail-pBar-TrustedPhone').style.width = TrustedPhonePrc + '%';
    
                    var MobilePhonePrc = get_prc(PhoneFL.FL_Mobile, CallStatus.Total);
                    document.getElementById('ivrDetail-MobilePhonePrc').textContent = MobilePhonePrc;
                    $('#ivrDetail-MobilePhonePrc').spincrement({
                        thousandSeparator: ",",
                        duration: 1200
                    });
                    document.getElementById('ivrDetail-MobilePhone').textContent = numberWithCommas(PhoneFL.FL_Mobile) + ' из ' + numberWithCommas(CallStatus.Total);
                    document.getElementById('ivrDetail-pBar-MobilePhone').style.width = MobilePhonePrc + '%';
                                  
                    for (index = 0; index < Object.keys(Languages).length; index++) {
                        dictCode = Object.keys(Languages)[index];
                        prc = get_prc(Languages[dictCode], CallStatus.Total);
    
                        document.getElementById('ivrDetail-'+dictCode+'LangPrc').textContent = prc;
                        $('#ivrDetail-'+dictCode+'LangPrc').spincrement({
                            thousandSeparator: ",",
                            duration: 1200
                        });
                        document.getElementById('ivrDetail-'+dictCode+'Lang').textContent = numberWithCommas(Languages[dictCode]) + ' из ' + numberWithCommas(CallStatus.Total);
                        document.getElementById('ivrDetail-pBar-'+dictCode+'Lang').style.width = prc + '%';
                    }
    
                    nn = 0;
                    for (index = 0; index < Object.keys(MenuTree_MM).length; index++) {
                        dictCode = Object.keys(MenuTree_MM)[index];
                        prc = get_prc(MenuTree_MM[dictCode], MenuTree_MM['Total']);
    
                        if (dictCode == 'Total') continue;
                        nn += 1;
    
                        $("<tr>").html("<th scope='row' style='text-align: center; font-weight: normal;'>" + nn + "</th>" +
                            "<td style='text-align: left; vertical-align:middle'>" + getMMLongname(dictCode) + "</td>" +
                            "<td style='text-align: center; vertical-align:middle'>" + numberWithCommas(MenuTree_MM[dictCode]) + "</td>" +
                            "<td style='text-align: center; vertical-align:middle'>" + prc + " %</td>"
                        ).appendTo('#ivrDetail-MenuTree-MM')
                    }
    
                    nn = 0;
                    for (index = 0; index < Object.keys(MenuTree_MCS).length; index++) {
                        dictCode = Object.keys(MenuTree_MCS)[index];
                        prc = get_prc(MenuTree_MCS[dictCode], MenuTree_MCS['Total']);
    
                        if (dictCode == 'Total') continue;
                        nn += 1;
    
                        $("<tr>").html("<th scope='row' style='text-align: center; font-weight: normal;'>" + nn + "</th>" +
                            "<td style='text-align: left; vertical-align:middle'>" + getMCSLongname(dictCode) + "</td>" +
                            "<td style='text-align: center; vertical-align:middle'>" + numberWithCommas(MenuTree_MCS[dictCode]) + "</td>" +
                            "<td style='text-align: center; vertical-align:middle'>" + prc + " %</td>"
                        ).appendTo('#ivrDetail-MenuTree-MCS')
                    }
                }
            }   
        }
    }).fail(function(error) {
        console.error(error);
    });
}