import datetime


adif_field = {
    'address': 'M',
    'address_intl': 'G',
    'age': 'N',
    'a_index': 'N',
    'ant_az': 'N',
    'ant_el': 'N',
    'ant_path': 'E',
    'arrl_sect': 'E',
    'award_submitted': 'P',
    'award_granted': 'P',
    'band': 'E',
    'band_rx': 'E',
    'call': 'S',
    'check': 'S',
    'class': 'S',
    'clublog_qso_upload_date': 'D',
    'clublog_qso_upload_status': 'E',
    'cnty': 'E',
    'comment': 'S',
    'comment_intl': 'I',
    'cont': 'E',
    'contacted_op': 'S',
    'contest_id': 'S',
    'country': 'S',
    'country_intl': 'I',
    'cqz': 'N',
    'credit_submitted': 'C',
    'credit_granted': 'C',
    'distance': 'N',
    'dxcc': 'E',
    'email': 'S',
    'eq_call': 'S',
    'eqsl_qslrdate': 'D',
    'eqsl_qslsdate': 'D',
    'eqsl_qsl_rcvd': 'E',
    'eqsl_qsl_sent': 'E',
    'fists': 'S',
    'fists_cc': 'S',
    'force_init': 'B',
    'freq': 'N',
    'freq_rx': 'N',
    'gridsquare': 'S',
    'guest_op': 'S',
    'hrdlog_qso_upload_date': 'D',
    'hrdlog_qso_upload_status': 'E',
    'iota': 'S',
    'iota_island_id': 'S',
    'ituz': 'N',
    'k_index': 'N',
    'lat': 'L',
    'lon': 'L',
    'lotw_qslrdate': 'D',
    'lotw_qslsdate': 'D',
    'lotw_qsl_rcvd': 'E',
    'lotw_qsl_sent': 'E',
    'max_bursts': 'N',
    'mode': 'E',
    'ms_shower': 'S',
    'my_city': 'S',
    'my_city_intl': 'I',
    'my_cnty': 'E',
    'my_country': 'S',
    'my_country_intl': 'I',
    'my_cq_zone': 'N',
    'my_dxcc': 'E',
    'my_fists': 'S',
    'my_gridsquare': 'S',
    'my_iota': 'S',
    'my_iota_island_id': 'S',
    'my_itu_zone': 'N',
    'my_lat': 'L',
    'my_lon': 'L',
    'my_name': 'S',
    'my_name_intl': 'I',
    'my_postal_code': 'S',
    'my_postal_code_intl': 'I',
    'my_rig': 'S',
    'my_rig_intl': 'I',
    'my_sig': 'S',
    'my_sig_intl': 'I',
    'my_sig_info': 'S',
    'my_sig_info_intl': 'I',
    'my_sota_ref': 'S',
    'my_state': 'E',
    'my_street': 'S',
    'my_street_intl': 'I',
    'my_usaca_counties': 'S',
    'my_vucc_grids': 'S',
    'name': 'S',
    'name_intl': 'I',
    'notes': 'M',
    'notes_intl': 'G',
    'nr_bursts': 'N',
    'nr_pings': 'N',
    'operator': 'S',
    'owner_callsign': 'S',
    'pfx': 'S',
    'precedence': 'S',
    'prop_mode': 'E',
    'public_key': 'S',
    'qrzcom_qso_upload_date': 'D',
    'qrzcom_qso_upload_status': 'E',
    'qslmsg': 'M',
    'qslmsg_intl': 'G',
    'qslrdate': 'D',
    'qslsdate': 'D',
    'qsl_rcvd': 'E',
    'qsl_rcvd_via': 'E',
    'qsl_sent': 'E',
    'qsl_sent_via': 'E',
    'qsl_via': 'S',
    'qso_complete': 'E',
    'qso_date': 'D',
    'qso_date_off': 'D',
    'qso_random': 'B',
    'qth': 'S',
    'qth_intl': 'I',
    'rig': 'M',
    'rig_intl': 'G',
    'rst_rcvd': 'S',
    'rst_sent': 'S',
    'rx_pwr': 'N',
    'sat_mode': 'S',
    'sat_name': 'S',
    'sfi': 'N',
    'sig': 'S',
    'sig_intl': 'I',
    'sig_info': 'S',
    'sig_info_intl': 'I',
    'silent_key': 'B',
    'skcc': 'S',
    'sota_ref': 'S',
    'srx': 'N',
    'srx_string': 'S',
    'state': 'E',
    'station_callsign': 'S',
    'stx': 'N',
    'stx_string': 'S',
    'submode': 'S',
    'swl': 'B',
    'ten_ten': 'N',
    'time_off': 'T',
    'time_on': 'T',
    'tx_pwr': 'N',
    'usaca_counties': 'S',
    'uksmg': 'N',
    've_prov': 'S',
    'vucc_grids': 'S',
    'web': 'S'
}

adif_utf_field = {
    'address_intl': 'address',
    'comment_intl': 'comment',
    'country_intl': 'country',
    'my_city_intl': 'my_city',
    'my_country_intl': 'my_country',
    'my_name_intl': 'my_name',
    'my_postal_code_intl': 'my_postal_code',
    'my_rig_intl': 'my_rig',
    'my_sig_intl': 'my_sig',
    'my_sig_info_intl': 'my_sig_info',
    'my_street_intl': 'my_street',
    'name_intl': 'name',
    'notes_intl': 'notes',
    'qslmsg_intl': 'qslmsg',
    'qth_intl': 'qth',
    'rig_intl': 'rig',
    'sig_intl': 'sig',
    'sig_info_intl': 'sig_info'
}

adif_rev_utf_field = {v: k for k,v in adif_utf_field.items()}


def convert_field_date(date_type, data):
    if date_type == 'B':
        return bool(data)
    elif date_type == 'N':
        return float(data)
    elif date_type == 'D':
        return datetime.date(int(data[0:4]), int(data[4:6]), int(data[6:8]))
    elif date_type == 'T':
        if len(data) == 6:
            return datetime.time(int(data[0:2]), int(data[2:4]), int(data[4:6]))
        return datetime.time(int(data[0:2]), int(data[2:4]))
    else:
        return data


def convert_field(name, data, date_type):
    if date_type:
        return convert_field_date(date_type, data)
    elif name in adif_field:
        return convert_field_date(adif_field[name], data)
    else:
        return convert_field_date('S', data)


class ParseError(Exception):
    def __init__(self, line, msg):
        self.line = line
        self.msg = msg

    def __str__(self):
        return 'Parse error: %s, in line: %d' % (self.msg, self.line)


class WriteError(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return 'Write error: %s' % self.msg
