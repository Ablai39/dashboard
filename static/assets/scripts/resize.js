function index_row_operators() {
    
    // Этап 1. Выравниваем высоту div "Общий SL за месяц"
    var rowMainSL = $('#index-row-main-sl').height(),
        rowMainMounthSL = $('#index-sl-shadow-month').height();
    
    if (rowMainMounthSL < rowMainSL) {
        document.getElementById("index-sl-shadow-month").style.height = String(rowMainSL) + 'px';
    }

    // Этап 2. Выравниваем высоту div "По всем секторам ВКЦ" / "Количество операторов в разрезе управлений"
    var rowMainInformation = $('#index-row-main-information').height(),
        rowindexAllSectors = $('#index-all-sectors').height(),
        rowLeftColumn = rowMainInformation + rowindexAllSectors + 10,

        rowGraphic = $('#index-row-graphic').height(),
        rowPlanFact = $('#index-row-plan-fact').height(),
        rowRightColumn = rowGraphic + rowPlanFact + 10;

        if (rowLeftColumn < rowRightColumn) {
        document.getElementById("index-all-sectors-body").style.height = String(rowindexAllSectors + (rowRightColumn - rowLeftColumn - 2)) + 'px';
    } else if (rowLeftColumn > rowRightColumn) {
        document.getElementById("index-row-plan-fact-body").style.height = String(rowPlanFact + (rowLeftColumn - rowRightColumn - 2)) + 'px';
    }

    // Этап 3. Выравниваем высоту div "Список операторов"
    var indexOperatorsStatus =  $('#index-operators-status').height(),
        indexRowStatistic =  $('#index-row-statistic').height(),
        indexRowOperators =  $('#index-row-operators').height(),
        indexOperatorsListData = $('#index-operators-list-data').height(),
        delta = indexOperatorsStatus - (indexRowStatistic + indexRowOperators + 10),

        rowOperatorsShapka = $('#index-operators-list-shapka').height();
    
    if (delta > 0) {
        document.getElementById("index-row-operators-body").style.height = String(indexRowOperators + delta) + 'px'
        document.getElementById("index-operators-list-data").style.height = String(indexOperatorsListData + delta) + 'px'
    }
}

function omilia_resize() {
    var omilia_offstat = $('#omilia-cbody-offstat').height(),
        omilia_trans = $('#omilia-cbody-trans').height(),
        omilia_trans_lst = $('#omilia-cbody-trans-lst').height(),
        //     row_online_stat = $('#omilia-row-online-stat').height(),
        //     row_online_dop = $('#z-omilia-time').height(),
        //     row_graphic = $('#omilia-row-graphic').height();


        row_online_main1 = $('#omilia-row-main1').height(),
        row_online_tran = $('#omilia-row-online-transfers2gr-body').height(),
        delta = row_online_main1 - row_online_tran;

    if (delta != 0) {
        document.getElementById("omilia-row-online-transfers2gr-body").style.height = (row_online_tran + delta) + 'px';
    }

    delta = omilia_offstat - (omilia_trans + omilia_trans_lst + 15);

    if (delta > 0) {
        document.getElementById("omilia-cbody-trans-lst").style.minHeight = (omilia_trans_lst + delta) + 'px';
    } else if (delta < 0) {
        document.getElementById("omilia-cbody-offstat").style.minHeight = (omilia_offstat - delta) + 'px';
    }

    var omilia_themes_h = $('#omilia-cbody-themes-graphic').height(),
        omilia_themes_lst_h = $('#omilia-cbody-themes-lst').height();

    delta = omilia_themes_h - omilia_themes_lst_h;

    if (delta > 0) {
        document.getElementById("omilia-cbody-themes-lst").style.minHeight = (omilia_themes_lst_h + delta) + 'px';
    } else if (delta < 0) {
        document.getElementById("omilia-cbody-themes-graphic").style.minHeight = (omilia_themes_h - delta + 20) + 'px';
    }

    // if (row_online_dop != row_online_stat) {
    //     document.getElementById("z-omilia-time").style.height = row_online_stat + 'px';
    // }

    // delta = row_online_main1 - row_online_tran - 15;

    // if (row_graphic != delta) {
    //     document.getElementById("omilia-row-graphic").style.height = delta + 'px';
    // }
}