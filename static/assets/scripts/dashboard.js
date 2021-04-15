// console.log('page => ' + page);
// --------- Первоначальный запуск ---------
if (page == 'index') {
    index_online();
    index_graphic();
    index_operators();
    index_chats();
    index_fcr_acr();

} else if (page == 'ivr') {
    ivr_online('first');
    ivr_history_data();

} else if (page == 'graphics') {
    graphics_sl(); 

} else if (page == 'omilia') {
    omilia_online('first');
    omilia_history_data();

} else if (page == 'wallboard') {
    wallboard_online();
    wallboard_index_info();
    wallboard_best_top5();

} else if (page == 'reports') {
    reports_acd_abn_calls_upd();
    reports_acd_abn_utp_calls_upd();

} else if (page == 'logs') {
    getLogs();
}

// --------- Циклы ---------
// циклы по 5 секунд
// служебные функции
setTimeout(function run() {
    if (window.isActive) {
        if (page == 'index') {
            index_row_operators();
        } else if (page == 'omilia') {
            omilia_resize();
        } else if (page == 'logs') {
            getLogs();
        }
    }
    setTimeout(run, timer_5_second);
}, timer_5_second);

// циклы по 10 секунд
setTimeout(function run() {
    if (window.isActive) {
        if (page == 'index') {
            index_online();
            index_chats();

        } else if (page == 'ivr') {
            ivr_online();

        } else if (page == 'omilia') {
            omilia_online('repeat');
            
        } else if (page == 'wallboard') {
            wallboard_index_info();
        }
    }
    setTimeout(run, timer_10_second);
}, timer_10_second);

// циклы по 15 секунд
setTimeout(function run() {
    if (window.isActive) {
        if (page == 'index') {
            index_operators();
            
        } else if (page == 'wallboard') {
            wallboard_online();
        }
    }
    setTimeout(run, timer_15_second);
}, timer_15_second);

// циклы по 60 секунд
setTimeout(function run_sixty_sec() {
    if (window.isActive) {
        if (page == 'index') {

            var now = new Date(),
                p_update_hour = time_of_update_index_graphic.getHours(),
                p_update_day = time_of_update_index_graphic.getDate();

            var now_hour = now.getHours(),
                now_minute = now.getMinutes(),
                now_day = now.getDate();

            if (p_update_day != now_day) {
                index_graphic();
            } else if (p_update_hour != now_hour) {
                if (now_minute >= 10){
                    index_graphic();
                }
            }
        }
    }
    setTimeout(run_sixty_sec, timer_60_second);
}, timer_60_second);

// циклы по 5 минут
setTimeout(function run_five_min() {
    if (window.isActive) {
        if (page == 'index') {
            index_fcr_acr();
        } else if (page == 'wallboard') {
            wallboard_best_top5();
        }
    }
    setTimeout(run_five_min, timer_5_minute);
}, timer_5_minute);