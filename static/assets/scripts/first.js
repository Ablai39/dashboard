var page,
    upravlenie = 'upib',
    time_of_update_index_graphic,
    INDEX_OPERATORS_DATA,
    ACD_ABN_REPORTS,
    ACD_ABN_UTP_REPORTS,
    OmiliaTran,
    a,
    b,
    reBtnTwo,
    OmiliaMedTran,
    OMILIA_HST_BTN = '',
    IVR_HST_BTN = '',
    OMILIA_BTN_LST = 'btn_destr_all',
    OMILIA_BTN_LST_TEN = 'btn_destr_all_ten',
    index_chLine = '0',
    menuStatus = 0;

// settings
var timer_2_second = 2000,
    timer_5_second = 5000,
    timer_7_second = 7000,
    timer_10_second = 10000,
    timer_15_second = 15000,
    timer_60_second = 60000,
    timer_5_minute = 300000;
window.isActive = true;

$(function() {
    window.isActive = true;
    $(window).focus(function() {
        this.isActive = true;
    });
    $(window).blur(function() {
        this.isActive = false;
    });
    showIsActive();
});

function showIsActive() {
    window.setTimeout("showIsActive()", 2000);
}

function f_upravlenie(value) {
    upravlenie = value;

    if (page == 'wallboard') {
        wallboard_index_info();
        wallboard_online();
        wallboard_best_top5();
    }
}

function nvl(value1, value2) {
    if (value1 == null) {
        return value2;
    } else {
        return value1;
    }
}

function getDateTime() {
    var now = new Date();
    var year = now.getFullYear();
    var month = now.getMonth() + 1;
    var day = now.getDate();
    var hour = now.getHours();
    var minute = now.getMinutes();
    var second = now.getSeconds();
    if (month.toString().length == 1) {
        month = '0' + month;
    }
    if (day.toString().length == 1) {
        day = '0' + day;
    }
    if (hour.toString().length == 1) {
        hour = '0' + hour;
    }
    if (minute.toString().length == 1) {
        minute = '0' + minute;
    }
    if (second.toString().length == 1) {
        second = '0' + second;
    }
    var dateTime = day + '.' + month + '.' + year + ' ' + hour + ':' + minute + ':' + second;
    return dateTime;
}

function getTime() {
    var now = new Date();
    var hour = now.getHours();
    var minute = now.getMinutes();
    var second = now.getSeconds();

    if (hour.toString().length == 1) {
        hour = '0' + hour;
    }
    if (minute.toString().length == 1) {
        minute = '0' + minute;
    }
    if (second.toString().length == 1) {
        second = '0' + second;
    }
    var dateTime = hour + ':' + minute + ':' + second;
    return dateTime;
}

function getHHMM() {
    var now = new Date();
    var hour = now.getHours();
    var minute = now.getMinutes();
    var second = now.getSeconds();

    if (hour.toString().length == 1) {
        hour = '0' + hour;
    }
    if (minute.toString().length == 1) {
        minute = '0' + minute;
    }
    if (second.toString().length == 1) {
        second = '0' + second;
    }
    var dateTime = hour + ':' + minute;
    return dateTime;
}

function getHour() {
    var now = new Date();
    var hour = now.getHours();
    return hour;
}

function getMinute() {
    var now = new Date();
    var minute = now.getMinutes();
    return minute;
}

function parseTime(s) {
    var c = s.split(':');
    return parseInt(c[0]) * 60 + parseInt(c[1]);
}

function unParseTime(minute) {
    var hour = parseInt(minute / 60 ^ 0);
    var minute = parseInt(minute) - (hour * 60);
    return hour + ':' + minute;
}

function numberWithCommas(x) {
    var parts = x.toString().split(".");
    parts[0] = parts[0].replace(/\B(?=(\d{3})+(?!\d))/g, ",");
    return parts.join(".");
}

function numberWithCommas_space(x) {
    var parts = x.toString().split(".");
    parts[0] = parts[0].replace(/\B(?=(\d{3})+(?!\d))/g, " ");
    return parts.join(".");
}

function fullScreen(element) {
    if (element.requestFullscreen) {
        element.requestFullscreen();
    } else if (element.webkitrequestFullscreen) {
        element.webkitRequestFullscreen();
    } else if (element.mozRequestFullscreen) {
        element.mozRequestFullScreen();
    }
}

function fullScreenCancel() {
    if (document.requestFullscreen) {
        document.requestFullscreen();
    } else if (document.webkitRequestFullscreen) {
        document.webkitRequestFullscreen();
    } else if (document.mozRequestFullscreen) {
        document.mozRequestFullScreen();
    }
}

function pad(str, max) {
    str = str.toString();
    return str.length < max ? pad("0" + str, max) : str;
}

body_width = $('.app-container').width();

// if (body_width < 1500) {
//     $('.app-container').addClass("closed-sidebar-mobile closed-sidebar")
// }

function get_prc(value1, total) {
    return Math.round(value1 / total * 100 * 100) / 100
}

var index_fcr_acr_dict = {
    "acr": {
        "all": '-',
        "cards": '-',
        "retail": '-',
        "homebank": '-',
        "onlinebank": '-',
        "sales": '-'
    },
    "fcr": '-',
    "incalls": '-',
    "rated_calls": '-',
    "rated_calls_prc": '-',
    "callsoffered": '-',
    "double_rings": '-',
    "status": '-'
}

function get_hour(sec) {
    if (sec > 3600) {
        return Math.trunc(sec/3600);
    } else {
        return 0;
    }
}

function get_min(sec) {
    var hour = get_hour(sec),
        cleanSec = sec - (hour * 3600);

    if (cleanSec > 60) {
        return Math.trunc(cleanSec/60);
    } else {
        return 0;
    }
}

function set_min_sec(sec) {
    var pMin = get_min(sec),
        pHour = get_hour(sec),
        pHourStr = '',
        pMinStr = '';

    if (pHour != 0) {
        pHourStr = String(pHour) + 'ч'
    }

    if (pMin != 0) {
        pMinStr = String(pMin) + 'м'
    }

    return pHourStr + ' ' + pMinStr + ' ' + String(sec - (pHour * 3600) - (pMin * 60)) + 'с'
}

function set_sl_color(value, page) {
    if ((value >= 80)) {
        if (page == 'wallboard') {
            return 'white';
        } else {
            return 'success';
        }
    } else if ((value >= 60) && (value <= 79)) {
        return 'warning';
    } else if (value <= 59) {
        return 'danger';
    } else {
        return 'info';
    }
}

function set_inqueue_color(value, page) {
    if (value <= 10) {
        if (page == 'wallboard') {
            return 'white';
        } else {
            return 'success';
        }
    } else if ((value >= 11) && (value <= 30)) {
        return 'warning';
    } else if (value > 30) {
        return 'danger';
    } else {
        return 'info';
    }
}

function set_chats_inqueue_color(value, page) {
    if (value <= 100) {
        if (page == 'wallboard') {
            return 'white';
        } else {
            return 'success';
        }
    } else if ((value >= 110) && (value <= 300)) {
        return 'warning';
    } else if (value > 300) {
        return 'danger';
    } else {
        return 'info';
    }
}

function set_asa_color(value, page) {
    if (value <= 15) {
        if (page == 'index') {
            return 'z-success';
        } else if (page == 'wallboard') {
            return 'white';            
        } else {
            return 'success';
        }
    } else if ((value > 15) && (value <= 40)) {
        return 'warning';
    } else if (value > 40) {
        return 'danger';
    } else {
        return 'info';
    }
}

function set_att_color(value) {
    if (value < 180) {
        if (page == 'index') {
            return 'z-success';
        } else {
            return 'success';
        }
    } else if ((value >= 180) && (value <= 300)) {
        return 'warning';
    } else if (value > 300) {
        return 'danger';
    } else {
        return 'info';
    }
}

function set_oldest_color(value) {
    if (value < 60) {
        return 'success';
    } else if ((value >= 60) && (value <= 300)) {
        return 'warning';
    } else if (value > 300) {
        return 'danger';
    } else {
        return 'info';
    }
}

function set_oldest_cba_color(value) {
    if (value < 300) {
        return 'success';
    } else if ((value >= 300) && (value <= 600)) {
        return 'warning';
    } else if (value > 600) {
        return 'danger';
    } else {
        return 'info';
    }
}

function set_acr_color(value) {
    if (value == '-') {
        return ''
    } else if (value >= 4) {
        if (page == 'index') {
            return 'z-success';
        } else {
            return 'success';
        }
    } else if ((value >= 3) && (value < 4)) {
        return 'warning';
    } else if (value < 3) {
        return 'danger';
    } else {
        return 'info';
    }
}

function set_fcr_color(value) {
    if (value >= 90) {
        return 'success';
    } else if ((value >= 50) && (value < 90)) {
        return 'warning';
    } else if (value < 50) {
        return 'danger';
    } else {
        return 'info';
    }
}

function set_arrow(prc_before, prc_after) {
    if (prc_before > prc_after) {
        return '';
    } else if (prc_before < prc_after) {
        return '';
    } else
        return '-';
}

// Выход из полноэкранного режима
function cancelFullscreen() {
    if(document.cancelFullScreen) {
      document.cancelFullScreen();
    } else if(document.mozCancelFullScreen) {
      document.mozCancelFullScreen();
    } else if(document.webkitCancelFullScreen) {
      document.webkitCancelFullScreen();
    }
  }