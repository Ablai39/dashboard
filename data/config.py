from dashboard.data import splitsGroup
from dashboard.data.global_functions import list2str

sectorsDict = {
    'cards': {
        'longname': 'Карточки',
        'enableCallBack': 'Y',
        'enableIndexGraphic': 'Y',
        'enableInGraphicPage': 'Y',
        'splitsStr': list2str(splitsGroup.main_cards),
        'splitsLst': splitsGroup.main_cards,
        'splits_cbaStr': list2str(splitsGroup.cards_cba),
        'splits_cbaLst': splitsGroup.cards_cba,
        'graphicLineColor': '#FF4500',
        'archive': 'N'
    },
    # 'cardsLine': {
    #     'longname': 'Карточки (Line)',
    #     'enableCallBack': 'N',
    #     'enableIndexGraphic': 'N',
    #     'splitsStr': list2str(splitsGroup.cardsLine),
    #     'splitsLst': splitsGroup.cardsLine,
    #     'graphicLineColor': '',
    #     'archive': 'N'
    # },
    'retail': {
        'longname': 'Розница',
        'enableCallBack': 'Y',
        'enableIndexGraphic': 'Y',
        'enableInGraphicPage': 'Y',
        'splitsStr': list2str(splitsGroup.retail),
        'splitsLst': splitsGroup.retail,
        'splits_cbaStr': list2str(splitsGroup.retail_cba),
        'splits_cbaLst': splitsGroup.retail_cba,
        'graphicLineColor': '#808080',
        'archive': 'N'
    },
    # 'retailLine': {
    #     'longname': 'Розница (Line)',
    #     'enableCallBack': 'N',
    #     'enableIndexGraphic': 'N',
    #     'splitsStr': list2str(splitsGroup.retailLine),
    #     'splitsLst': splitsGroup.retailLine,
    #     'graphicLineColor': '',
    #     'archive': 'N'
    # },
    'homebank': {
        'longname': 'Homebank',
        'enableCallBack': 'Y',
        'enableIndexGraphic': 'Y',
        'enableInGraphicPage': 'Y',
        'splitsStr': list2str(splitsGroup.main_homebank),
        'splitsLst': splitsGroup.main_homebank,
        'splits_cbaStr': list2str(splitsGroup.homebank_cba),
        'splits_cbaLst': splitsGroup.homebank_cba,
        'graphicLineColor': '#3f6ad8',
        'archive': 'N'
    },
    'onlinebank': {
        'longname': 'Onlinebank',
        'enableCallBack': 'N',
        'enableIndexGraphic': 'Y',
        'enableInGraphicPage': 'Y',
        'splitsStr': list2str(splitsGroup.main_onlinebank),
        'splitsLst': splitsGroup.main_onlinebank,
        'graphicLineColor': '#008000',
        'archive': 'N'
    },
    'sales': {
        'longname': 'Sales',
        'enableCallBack': 'N',
        'enableIndexGraphic': 'Y',
        'splitsStr': list2str(splitsGroup.sales),
        'splitsLst': splitsGroup.sales,
        'graphicLineColor': '#d92550',
        'archive': 'N'
    },
    'soft': {
        'longname': 'Soft Collection',
        'enableCallBack': 'N',
        'enableIndexGraphic': 'Y',
        'splitsStr': list2str(splitsGroup.soft),
        'splitsLst': splitsGroup.soft,
        'graphicLineColor': '#8a2be2',
        'archive': 'N'
    },
    'posobie': {
        'longname': 'Пособие 42500',
        'enableCallBack': 'Y',
        'enableIndexGraphic': 'Y',
        'splitsStr': list2str(splitsGroup.posobie),
        'splitsLst': splitsGroup.posobie,
        'splits_cbaStr': list2str(splitsGroup.posobie_cba),
        'splits_cbaLst': splitsGroup.posobie_cba,
        'graphicLineColor': '#ffd700',
        'archive': 'Y'
    },
    'otdelenyaATM': {
        'longname': 'Адреса отделений и АТМ',
        'enableCallBack': 'N',
        'enableIndexGraphic': 'N',
        'splitsStr': list2str(splitsGroup.otdelenyaATM),
        'splitsLst': splitsGroup.otdelenyaATM,
        'graphicLineColor': '#66CDAA',
        'archive': 'N'
    },
    'onboarding': {
        'longname': 'Onboarding',
        'enableCallBack': 'N',
        'enableIndexGraphic': 'N',
        'splitsStr': list2str(splitsGroup.onboarding),
        'splitsLst': splitsGroup.onboarding,
        'graphicLineColor': '#BC8F8F',
        'archive': 'Y'
    },
    'tranOutsourcing': {
        'longname': 'Трансферы аутсорсинга',
        'enableCallBack': 'N',
        'enableIndexGraphic': 'N',
        'splitsStr': list2str(splitsGroup.tranOutsourcing),
        'splitsLst': splitsGroup.tranOutsourcing,
        'graphicLineColor': '#FF1493',
        'archive': 'Y'
    },
    'unknown': {
        'longname': 'Неизвестно',
        'enableCallBack': 'N',
        'enableIndexGraphic': 'N',
        'splitsStr': None,
        'splitsLst': [],
        'graphicLineColor': '',
        'archive': 'N'
    },
    'pension':{
        'longname': 'Пенсия',
        'enableCallBack': 'N',
        'enableIndexGraphic': 'N',
        'splitsStr': list2str(splitsGroup.pension),
        'splitsLst': splitsGroup.pension,
        'graphicLineColor': '#ffd700',
        'archive': 'N'
    }
}

splitItemsDict = {
    'inqueue': {
        'calcMonth': 'N',
        'useCBA': 'Y'
    },
    'anstime': {
        'calcMonth': 'N',
        'useCBA': 'N'
    },
    'acdtime': {
        'calcMonth': 'N',
        'useCBA': 'N'
    },
    'oldest': {
        'calcMonth': 'N',
        'useCBA': 'Y'
    },
    'callsoffered': {
        'calcMonth': 'Y',
        'useCBA': 'N'
    },
    'acdcalls': {
        'calcMonth': 'Y',
        'useCBA': 'N'
    },
    'abncalls': {
        'calcMonth': 'Y',
        'useCBA': 'N'
    },
    'outflowcalls': {
        'calcMonth': 'Y',
        'useCBA': 'N'
    },
    'acceptable': {
        'calcMonth': 'Y',
        'useCBA': 'N'
    },
    'slvlabns': {
        'calcMonth': 'Y',
        'useCBA': 'N'
    }
}

def getMainSector(sector):
    if 'archive' in sectorsDict[sector]:
        if sectorsDict[sector]['archive'] == 'Y':
            return None
    
    return sector

depsDict = {
    'uprk': {
        'longname': 'Упр. поддержки розничных клиентов',
        'mainSector': getMainSector('cards'),
        'highDepCode': 'ContactCenter',
        'directSplitsLst': ['144'],
        'icon': 'pe-7s-angle-right-circle'
    },
    'rubs': {
        'longname': 'Региональное упр. банковского сервиса',
        'mainSector': getMainSector('retail'),
        'highDepCode': 'ContactCenter',
        'directSplitsLst': ['109'],
        'icon': 'pe-7s-angle-right-circle'
    },
    'upib': {
        'longname': 'Упр. поддержки интернет банкинга',
        'mainSector': getMainSector('homebank'),
        'highDepCode': 'ContactCenter',
        'directSplitsLst': ['108'],
        'icon': 'pe-7s-angle-right-circle'
    },
    'videobank': {
        'longname': 'Упр. видеобанкинга',
        'mainSector': getMainSector('cards'),
        'highDepCode': 'ContactCenter',
        'directSplitsLst': ['120'],
        'icon': 'pe-7s-angle-right-circle'
    },
    'utp': {
        'longname': 'Упр. телефонных продаж',
        'mainSector': getMainSector('sales'),
        'highDepCode': 'ContactCenter',
        'directSplitsLst': ['102'],
        'icon': 'pe-7s-angle-right-circle'
    },
    'usc': {
        'longname': 'Упр. Soft Collection',
        'mainSector': getMainSector('soft'),
        'highDepCode': 'ContactCenter',
        'directSplitsLst': ['67'],
        'icon': 'pe-7s-angle-right-circle'
    },
    'filial': {
        'longname': 'Филиалы',
        'mainSector': getMainSector('posobie'),
        'highDepCode': 'Bank',
        'directSplitsLst': ['110'],
        'icon': 'pe-7s-angle-right-circle'
    },
    'unknown': {
        'longname': 'Подразделение не определено',
        'mainSector': '',
        'highDepCode': 'unknown',
        'directSplitsLst': [],
        'icon': 'pe-7s-attention'
    }
}

widgetOperatorsItemsDict = {
    'inqueue2': {
        'longname': 'Очередь',
        'agentAction': '-',
        'icon': 'z-pe-7s-users',
        'iconEnable': 'N',
        'onClickEnable': 'N',
        'isAgentStatus': 'N'
    },
    'available': {
        'longname': 'Готов',
        'agentAction': 'Готов',
        'icon': 'pe-7s-call',
        'iconEnable': 'N',
        'onClickEnable': 'Y',
        'isAgentStatus': 'Y'
    },
    'acd': {
        'longname': 'Обслуживают вызов',
        'agentAction': 'Обслуживание',
        'icon': 'pe-7s-headphones',
        'iconEnable': 'N',
        'onClickEnable': 'Y',
        'isAgentStatus': 'Y'
    },
    'cba': {
        'longname': 'Call back',
        'agentAction': 'Обслуживание',
        'icon': 'pe-7s-next-2',
        'iconEnable': 'N',
        'onClickEnable': 'Y',
        'isAgentStatus': 'N'
    },
    'acw': {
        'longname': 'ПВО',
        'agentAction': 'ПВО',
        'icon': 'pe-7s-hourglass',
        'iconEnable': 'N',
        'onClickEnable': 'Y',
        'isAgentStatus': 'Y'
    },
    'break': {
        'longname': 'Перерыв',
        'agentAction': 'Перерыв',
        'icon': 'pe-7s-wristwatch',
        'iconEnable': 'N',
        'onClickEnable': 'Y',
        'isAgentStatus': 'Y'
    },
    'lunch': {
        'longname': 'Обед',
        'agentAction': 'Обед',
        'icon': 'pe-7s-clock',
        'iconEnable': 'N',
        'onClickEnable': 'Y',
        'isAgentStatus': 'Y'
    },
    'training': {
        'longname': 'Обучение',
        'agentAction': 'Обучение',
        'icon': 'pe-7s-study',
        'iconEnable': 'N',
        'onClickEnable': 'Y',
        'isAgentStatus': 'Y'
    },
    'supervisorCons': {
        'longname': 'Консульт. с супервизором',
        'agentAction': 'Консультация',
        'icon': 'pe-7s-comment',
        'iconEnable': 'N',
        'onClickEnable': 'Y',
        'isAgentStatus': 'Y'
    },
    'technicalBreak': {
        'longname': 'Технический перерыв',
        'agentAction': 'Тех. перерыв',
        'icon': 'pe-7s-tools',
        'iconEnable': 'N',
        'onClickEnable': 'Y',
        'isAgentStatus': 'Y'
    },
    'supervisorWork': {
        'longname': 'Супервизор',
        'agentAction': 'Супервизор',
        'icon': 'pe-7s-id',
        'iconEnable': 'N',
        'onClickEnable': 'Y',
        'isAgentStatus': 'Y'
    },
    'system': {
        'longname': 'Авторизован',
        'agentAction': 'Авторизован',
        'icon': 'pe-7s-upload',
        'iconEnable': 'N',
        'onClickEnable': 'Y',
        'isAgentStatus': 'Y'
    },
    'manualDial': {
        'longname': 'Ручной обзвон',
        'agentAction': 'Ручной обзвон',
        'icon': 'pe-7s-upload',
        'iconEnable': 'N',
        'onClickEnable': 'Y',
        'isAgentStatus': 'Y'
    },
    'operatorsCC': {
        'longname': 'Количество операторов КЦ:',
        'agentAction': '-',
        'icon': 'pe-7s-add-user',
        'iconEnable': 'N',
        'onClickEnable': 'N',
        'isAgentStatus': 'N'
    },
    'operatorsFilial': {
        'longname': 'Количество операторов ФИЛИАЛОВ:',
        'agentAction': '-',
        'icon': 'pe-7s-add-user',
        'iconEnable': 'N',
        'onClickEnable': 'N',
        'isAgentStatus': 'N'
    },
    'operatorsUnknown': {
        'longname': 'Количество операторов (Подразделение не определено):',
        'agentAction': '-',
        'icon': 'pe-7s-add-user',
        'iconEnable': 'N',
        'onClickEnable': 'N',
        'isAgentStatus': 'N'
    },
    'asa': {
        'longname': 'Среднее время ожидания ответа оператора (ASA)',
        'agentAction': '-',
        'icon': 'pe-7s-repeat',
        'iconEnable': 'N',
        'onClickEnable': 'N',
        'isAgentStatus': 'N'
    },
    'att': {
        'longname': 'Среднее время разговора (ATT)',
        'agentAction': '-',
        'icon': 'pe-7s-repeat',
        'iconEnable': 'N',
        'onClickEnable': 'N',
        'isAgentStatus': 'N'
    },
    'acr': {
        'longname': 'Средняя оценка клиента (ACR)',
        'agentAction': '-',
        'icon': 'pe-7s-repeat',
        'iconEnable': 'N',
        'onClickEnable': 'N',
        'isAgentStatus': 'N'
    }
}