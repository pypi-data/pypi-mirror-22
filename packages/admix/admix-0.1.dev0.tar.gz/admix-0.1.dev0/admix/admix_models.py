#!/usr/bin/env python
# -*- coding: utf-8 -*-

# all models
def models():
    return ['K7b']

# population names for all models
def populations(model):
    if model == 'K7b':
        return [('South Asian','南亚'),
                ('West Asian','西亚'),
                ('Siberian','西伯利亚'),
                ('African','非洲'),
                ('Southern','地中海－中东'),
                ('Atlantic Baltic','大西洋波罗的海'),
                ('East Asian','东亚')]
    elif model == 'K12b':
        return [('Gedrosia','格德罗西亚'),
                ('Siberian','西伯利亚'),
                ('Northwest African','西北非'),
                ('Southeast Asian','东南亚'),
                ('Atlantic Med','大西洋地中海'),
                ('North European','北欧'),
                ('South Asian','南亚'),
                ('East African','东非'),
                ('Southwest Asian','西南亚'),
                ('East Asian','东亚'),
                ('Caucasus','高加索'),
                ('Sub Saharan','撒哈拉以南非洲')]
    elif model == 'E11':
        return [('African','非洲'),
                ('European','欧洲'),
                ('India','印度'),
                ('Malay','马来'),
                ('South Chinese Dai','傣族'),
                ('Southwest Chinese Yi','彝族'),
                ('East Chinese','华东'),
                ('Japanese','日本'),
                ('North Chinese Oroqen','鄂伦春'),
                ('Yakut','雅库特'),
                ('American','美洲')]
    elif model == 'globe13':
        return [('Siberian','西伯利亚'),
                ('Amerindian','美洲印第安'),
                ('West African','西非'),
                ('Palaeo African','旧非洲'),
                ('Southwest Asian','西南亚'),
                ('East Asian','东亚'),
                ('Mediterranean','地中海'),
                ('Australasian','澳大拉西亚'),
                ('Artic','北极'),
                ('West Asian','西亚'),
                ('North European','北欧'),
                ('South Asian','南亚'),
                ('East African','东非')]
    elif model == 'globe10':
        return [('Ameriandian','美洲印第安'),
                ('West Asian','西亚'),
                ('Australasian','澳大拉西亚'),
                ('Palaeo African','旧非洲'),
                ('Neo African','新非洲'),
                ('Siberian','西伯利亚'),
                ('Southern','地中海－中东'),
                ('East Asian','东亚'),
                ('Atlantic Baltic','大西洋波罗的海'),
                ('South Asian','南亚')]
    elif model == 'world9':
        return [('Amerindian','美洲印第安'),
                ('East Asian','东亚'),
                ('African','非洲'),
                ('Atlantic Baltic','大西洋波罗的海'),
                ('Australasian','澳大拉西亚'),
                ('Siberian','西伯利亚'),
                ('Caucasus Gedrosia','高加索－格德罗西亚'),
                ('Southern','地中海－中东'),
                ('South Asian','南亚')]
    elif model == 'Eurasia7':
        return [('Sub Saharan','撒哈拉以南非洲'),
                ('West Asian','西亚'),
                ('Atlantic Baltic','大西洋波罗的海'),
                ('East Asian','东亚'),
                ('Southern','地中海－中东'),
                ('South Asian','东亚'),
                ('Siberian','西伯利亚')]
    elif model == 'Africa9':
        return [('Europe','欧洲'),
                ('Northwest Africa','西北非'),
                ('Southwest Asia','西南亚'),
                ('East Africa','东非'),
                ('South Africa','南非'),
                ('Mbuti','姆布蒂人'),
                ('West Africa','西非'),
                ('Biaka','比亚卡人'),
                ('San','桑人')]
    elif model == 'weac2':
        return [('Palaeoafrican','旧非洲'),
                ('Atlantic Baltic','大西洋波罗的海'),
                ('Northeast Asian','东北亚'),
                ('Near East','近东'),
                ('Sub Saharan','撒哈拉以南非洲'),
                ('South Asian','南亚'),
                ('Southeast Asian','东南亚')]
    elif model == 'K36':
        return [('Amerindian','美洲印第安'),
                ('Arabian','阿拉伯'),
                ('Armenian','亚美尼亚'),
                ('Basque','巴斯克'),
                ('Central African','中非'),
                ('Central Euro','中欧'),
                ('East African','东非'),
                ('East Asian','东亚'),
                ('East Balkan','东巴尔干'),
                ('East Central Asian','中东亚'),
                ('East Central Euro','中东欧'),
                ('East Med','东地中海'),
                ('Eastern Euro','东欧'),
                ('Fennoscandian','芬诺斯坎底亚'),
                ('French','法国'),
                ('Iberian','伊比利亚'),
                ('Indo-Chinese','印度支那'),
                ('Italian','意大利'),
                ('Malayan','马来亚'),
                ('Near Eastern','近东'),
                ('North African','北非'),
                ('North Atlantic','北大西洋'),
                ('North Caucasian','北高加索'),
                ('North Sea','北海'),
                ('Northeast African','东北非'),
                ('Oceanian','大洋洲'),
                ('Omotic','奥摩人'),
                ('Pygmy','俾格米人'),
                ('Siberian','西伯利亚'),
                ('South Asian','南亚'),
                ('South Central Asian','中南亚'),
                ('South Chinese','华南'),
                ('Volga-Ural','伏尔加－乌拉尔'),
                ('West African','西非'),
                ('West Caucasian','西高加索'),
                ('West Med','西地中海')]
    elif model == 'EUtest13':
        return [('South Baltic','南波罗的海'),
                ('East Euro','东欧'),
                ('North-Central Euro','中北欧'),
                ('Atlantic','大西洋'),
                ('West Med','西地中海'),
                ('East Med','东地中海'),
                ('West Asian','西亚'),
                ('Middle Eastern','中东'),
                ('South Asian','南亚'),
                ('East African','东非'),
                ('East Asian','东亚'),
                ('Siberian','西伯利亚'),
                ('West African','西非')]
    elif model == 'Jtest14':
        return [('South Baltic','南波罗的海'),
                ('East Euro','东欧'),
                ('North-Central Euro','中北欧'),
                ('Atlantic','大西洋'),
                ('West Med','西地中海'),
                ('Ashkenazim','德系犹太人'),
                ('East Med','东地中海'),
                ('West Asian','西亚'),
                ('Middle Eastern','中东'),
                ('South Asian','南亚'),
                ('East African','东非'),
                ('East Asian','东亚'),
                ('Siberian','西伯利亚'),
                ('West African','西非')]
    elif model == 'HarappaWorld':
        return [('South-Indian','南印度'),
                ('Baloch','俾路支人'),
                ('Caucasian','高加索人'),
                ('Northeast-Euro','东北欧'),
                ('Southeast-Asian','东南亚'),
                ('Siberian','西伯利亚'),
                ('Northeast-Asian','东北亚'),
                ('Papuan','巴布亚人'),
                ('American','美洲原住民'),
                ('Beringian','白令陆桥'),
                ('Mediterranean','地中海'),
                ('Southwest-Asian','西南亚'),
                ('San','桑人'),
                ('East-African','东非'),
                ('Pygmy','俾格米人'),
                ('West-African','西非')]
    elif model == 'TurkicK11':
        return [('Southeast European','东南欧'),
                ('West Asian','西亚'),
                ('Southeast Asian','东南亚'),
                ('Sub-Saharan African','撒哈拉以南非洲'),
                ('Northeast European','东北欧'),
                ('Indian','印度'),
                ('Northwest European','西北欧'),
                ('Turkic','突厥'),
                ('Mongol','蒙古'),
                ('Papuan','巴布亚'),
                ('Northeast Asian','东北亚')]
    elif model == 'KurdishK10':
        return [('Kurdish','库尔德人'),
                ('Southeast-European','东南欧'),
                ('Norhteast-European','东北欧'),
                ('Indian','印度'),
                ('East-Asian','东亚'),
                ('Northwest-European','西北欧'),
                ('Siberian','西伯利亚'),
                ('Sardinian','撒丁'),
                ('Southwest-Asian','西南亚'),
                ('Sub-Saharan','撒哈拉以南非洲')]
    elif model == 'AncientNearEast13':
        return [('Southeast Asian','东南亚'),
                ('Anatolia Neolithic','新石器时代安纳托利亚'),
                ('CHG-EEF','高加索狩猎采集者－早期欧洲农人'),
                ('Polar','极地'),
                ('EHG','欧洲狩猎采集者'),
                ('Sub-Saharan','撒哈拉以南非洲'),
                ('Iran-Neolithic','新石器时代伊朗'),
                ('Karitiana','卡利吉亚纳'),
                ('Ancestral-Indian','原始印度人'),
                ('Natufian','纳吐夫'),
                ('Siberian','西伯利亚'),
                ('Papuan','巴布亚'),
                ('SHG-WHG','斯堪的纳维亚－西欧狩猎采集者')]
    elif model == 'K7AMI':
        return [('Sub-Saharan','撒哈拉以南非洲'),
                ('Oceanian','大洋洲'),
                ('Amerindian','美洲印第安人'),
                ('Euro Hunter-Gatherer','欧洲狩猎采集者'),
                ('Siberian','西伯利亚'),
                ('Southeast Asian','东南亚'),
                ('Near Eastern','近东')]
    elif model == 'K8AMI':
        return [('Amerindian','美洲印第安人'),
                ('Siberian','西伯利亚'),
                ('Euro Hunter-Gatherer','欧洲狩猎采集者'),
                ('Oceanian','大洋洲'),
                ('Sub-Saharan','撒哈拉以南非洲'),
                ('Southeast Asian','东南亚'),
                ('Linearbandkeramik','线纹陶文化'),
                ('South-Central Asian','中南亚')]
    elif model == 'MDLPK27':
        return [('Nilotic-Omotic','尼罗－奥摩'),
                ('Ancestral-South-Indian','原始南印度人'),
                ('North-European-Baltic','北欧－波罗的海'),
                ('Uralic','乌拉尔'),
                ('Australo-Melanesian','澳美'),
                ('East-Siberean','东西伯利亚'),
                ('Ancestral-Yayoi','原始弥生人'),
                ('Caucasian-Near-Eastern','高尔索－近东'),
                ('Tibeto-Burman','藏缅'),
                ('Austronesian','南岛'),
                ('Central-African-Pygmean','中非俾格米人'),
                ('Central-African-Hunter-Catherers','中非狩猎采集者'),
                ('Nilo-Sahrian','尼罗－撒哈拉'),
                ('North-African','北非'),
                ('Gedrosia-Caucasian','格德罗西亚－高加索'),
                ('Cushitic','库施特'),
                ('Congo-Pygmean','刚果俾格米人'),
                ('Bushmen','布须曼人'),
                ('South-Meso-Amerindian','中南美洲印第安人'),
                ('South-West-European','西南欧'),
                ('North-Amerindian','北美洲印第安人'),
                ('Arabic','阿拉伯'),
                ('North-Circumpolar','北极圈'),
                ('Kalash','卡拉什人'),
                ('Papuan-Australian','巴布亚－澳大利亚'),
                ('Baltic-Finnic','波罗的海－芬兰'),
                ('Bantu','班图人')]
    elif model == 'puntDNAL':
        return [('EHG-Steppe','欧洲狩猎采集者－大草原'),
                ('Oceanian','大洋洲'),
                ('East Eurasian','东欧亚'),
                ('Iran Neolithic','新石器时代伊朗'),
                ('Siberian','西伯利亚'),
                ('Sub-Saharan','撒哈拉以南非洲'),
                ('African HG','非洲狩猎采集者'),
                ('South Eurasian','南欧亚'),
                ('Western HG','西方狩猎采集者'),
                ('Natufian HG','纳吐夫狩猎采集者'),
                ('Amerinidian','美洲印第安人'),
                ('Anatolian Neolithic','新石器时代安纳托利亚')]
    else:
        print('Model does not exist!')
        return None

# number of populations in all models
def n_populations(model):
    return len(populations(model))

# model alleles file names
def snp_file_name(model):
    return model + '.alleles'

# model frequency matrix file names
def frequency_file_name(model):
    return model + '.' + str(n_populations(model)) + '.F'
