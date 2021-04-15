from dashboard.data.global_functions import list2str

# ------------- Variables -------------
list_of_skills = ['cards','retail','homebank','onlinebank','all']
all_skills_list = []
skills_of_upravlenie = []

# ---------------------- УПИБ ----------------------
homebank = ['homebank','14','15','16']
onlinebank = ['onlinebank','26','27','28']
vip_onlinebank = ['vip_onlinebank','65','66']
payments = ['payments','30','31','32']
homebank_cba = ['homebank_cba','62']

upib = [homebank, payments, onlinebank, vip_onlinebank]
# ---------------------- УПРК ----------------------
vip = ['vip','36']
premium = ['premium','2','3','4']
amex = ['amex','5','6','7']
vip_pos = ['vip_pos','8','64']
pos = ['pos','17','18','19']
minipos = ['minipos','37','38','39']
hm = ['hm','40']
cards = ['cards','11','12','13','112'] # 112 - Card_Line_2
cards_cba = ['cards_cba','10']
card_of_block = ['card_of_block','78'] # блокировка карт по звонкам из одтелений
# -- по своему усмотрению
pos_modified = ['pos',]
for skills in [vip_pos, pos, minipos, hm]:
    for index, skills_id in enumerate(skills):
        if index != 0:
            pos_modified.append(skills_id)

uprk = [vip, premium, amex, pos_modified, cards]

# ---------------------- РУБС ----------------------
retail = ['retail','20','21','22','111'] # 111 -  Retail_Line_2
retail_cba = ['retail_cba','29']
rubs = [retail]
# ---------------------- ИКЦ ----------------------
sales = ['sales','33','34','35']
utp = [sales]
sales_str = list2str(sales[1:])
# ----------------- Soft -------------------
soft = ['soft','42','43']
# ------------------------------------------
posobie = ['posobie','114','115']
# ------------------------------------------
otdelenyaATM = ['otdelenyaATM','116','117']
# ------------------------------------------
onboarding = ['onboarding','118','119'] 
# ------------------------------------------
tranOutsourcing = ['tranOutsourcing','201']
# ---------------------- Для основного дашборда ----------------------
main_cards = ['cards',]
for skills in [cards, amex, pos, minipos, vip_pos, hm, vip, premium, card_of_block]:
    for index, skills_id in enumerate(skills):
        if index != 0:
            main_cards.append(skills_id)

main_onlinebank = ['onlinebank',]
for skills in [onlinebank, vip_onlinebank]:
    for index, skills_id in enumerate(skills):
        if index != 0:
            main_onlinebank.append(skills_id)

main_retail = retail

main_homebank = ['homebank',]
for skills in [homebank, payments]:
    for index, skills_id in enumerate(skills):
        if index != 0:
            main_homebank.append(skills_id)

main_dashboard = [main_cards, cards_cba, main_retail, retail_cba, main_homebank, homebank_cba, main_onlinebank, sales, soft, posobie, otdelenyaATM, onboarding, tranOutsourcing]
# ---------------------- Для отчетов ----------------------
allSkillsDepart = [main_cards, main_retail, main_homebank, main_onlinebank, sales, soft, posobie, otdelenyaATM, onboarding, tranOutsourcing]

all_depart_skills = []
for skills_lst in main_dashboard:
    for index, skills_id in enumerate(skills_lst):
        if index != 0:
            all_depart_skills.append(skills_id)

all_depart_skills_str = list2str(all_depart_skills)