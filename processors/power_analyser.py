from processors.graph_creater import make_chart
from users import users_data, nl


def get_power_statistics(power_data: list, user_id: int):
    ftp = int(users_data[f'{user_id}']['ftp'])

    # zone_1_by_power = [0, ftp * 0.56]
    # zone_2_by_power = [ftp * 0.56, ftp * 0.75]
    # zone_3_by_power = [ftp * 0.75, ftp * 0.90]
    # zone_4_by_power = [ftp * 0.90, ftp * 1.05]
    # zone_5_by_power = [ftp * 1.05, ftp * 1.20]
    # zone_6_by_power = [ftp * 1.21, ftp * 1.50]
    # zone_7_by_power = [ftp * 1.50, 5000]

    zone_1_by_power = [ftp * 0.5, ftp * 0.65]
    zone_2_by_power = [ftp * 0.66, ftp * 0.75]
    zone_3_by_power = [ftp * 0.76, ftp * 0.92]
    zone_4_by_power = [ftp * 0.93, ftp * 1.00]
    zone_5_by_power = [ftp * 1.01, 2000]

    list_of_zone = {
        'zone_1_by_power': f'Восстановление {nl}{int(zone_1_by_power[0])} – {int(zone_1_by_power[1])}',
        'zone_2_by_power': f'Выносливость {nl}{int(zone_2_by_power[0])} – {int(zone_2_by_power[1])}',
        'zone_3_by_power': f'Темповая {nl}{int(zone_3_by_power[0])} – {int(zone_3_by_power[1])}',
        'zone_4_by_power': f'FTP {nl}{int(zone_4_by_power[0])} – {int(zone_4_by_power[1])}',
        'zone_5_by_power': f'Анаэробная {nl}{int(zone_5_by_power[0])} – ∞',
        # 'zone_6_by_power': f'Анаэробная {nl}{int(zone_6_by_power[0])} – {int(zone_6_by_power[1])}',
        # 'zone_7_by_power': f'Мощность {nl}{int(zone_7_by_power[0])} – ∞',
    }

    dicts_of_zones = {}

    i = 1
    while i <= len(list_of_zone):
        keyword = f'time_in_zone_' + str(i) + '_by_power'
        value = 0
        dicts_of_zones[keyword] = value
        i += 1

    all_power_items = 0

    seconds = power_data.size
    for _ in range(0, seconds):
        power = power_data[_]
        if power != 0:
            all_power_items += 1

            for i in range(1, len(list_of_zone) + 1):
                start_range = eval(f'zone_' + str(i) + '_by_power')[0]
                finish_range = eval(f'zone_' + str(i) + '_by_power')[1]
                key = f'time_in_zone_' + str(i) + '_by_power'

                if start_range <= power <= finish_range:
                    new_value = dicts_of_zones[key] + 1
                    dicts_of_zones.update({key: new_value})

    list_of_percents = []

    for i in range(1, len(dicts_of_zones) + 1):
        keyword = f'time_in_zone_' + str(i) + '_by_power'
        new_value = round((dicts_of_zones[keyword] / all_power_items * 100), 1)
        list_of_percents.append(new_value)
        dicts_of_zones.update({keyword: new_value})

    option = 'power'

    make_chart(list_of_zone, dicts_of_zones, option)
