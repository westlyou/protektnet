# -*- coding: utf-8 -*-
##########################################################################
# Author      : Webkul Software Pvt. Ltd. (<https://webkul.com/>)
# Copyright(c): 2017-Present Webkul Software Pvt. Ltd.
# All Rights Reserved.
#
#
#
# This program is copyright property of the author mentioned above.
# You can`t redistribute it and/or modify it.
#
#
# You should have received a copy of the License along with this program.
# If not, see <https://store.webkul.com/license.html/>
##########################################################################


{
    "name":  "Mass Mailing With Other Outgoing Server",
    "summary":  " This module enables the user to select different outgoing mail servers for each mass mailing records rather than using the default server which is configured for Odoo.",
    "category":  "Marketing",
    "version":  "1.0.1",
    "sequence":  1,
    "author":  "Webkul Software Pvt. Ltd.",
    "license":  "Other proprietary",
    "website":  "https://store.webkul.com/Odoo-Mass-Mailing-With-Other-Outgoing-Server.html",
    "description":  """ This module enables the user to select different outgoing mail servers for each mass mailing records rather than using the default server which is configured for Odoo.""",
    "live_test_url":  "http://odoodemo.webkul.com/?module=mass_mailing_outgoing_mailserver&version=11.0",
    "depends":  ['mass_mailing'],
    "data":  [
        'views/res_config_view.xml',
        'views/mass_mailing_view.xml',
    ],
    "images":  ['static/description/Banner.png'],
    "application":  True,
    "installable":  True,
    "auto_install":  False,
    "price":  10,
    "currency":  "EUR",
    "pre_init_hook":  "pre_init_check",
}
