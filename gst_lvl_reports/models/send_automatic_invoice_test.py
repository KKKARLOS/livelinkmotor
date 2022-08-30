# Available variables:
#  - env: Odoo Environment on which the action is triggered
#  - model: Odoo Model of the record on which the action is triggered; is a void recordset
#  - record: record on which the action is triggered; may be void
#  - records: recordset of all records on which the action is triggered in multi-mode; may be void
#  - time, datetime, dateutil, timezone: useful Python libraries
#  - float_compare: Odoo function to compare floats based on specific precisions
#  - log: log(message, level='info'): logging function to record debug information in ir.logging table
#  - Warning: Warning Exception to use with raise
# To return an action, assign: action = {...}

if record.invoice_payment_state == 'paid':
    # env.ref('account.email_template_edi_invoice').send_mail(record.id)

    invoice_object = record
    for a in record.invoice_line_ids:
        if 'FR' in a.product_id.name:
            template = env.ref('account.email_template_edi_invoice_fr', raise_if_not_found=False)
            lang = False

        if 'FR' not in a.product_id.name:
            template = env.ref('account.email_template_edi_invoice', raise_if_not_found=False)
            lang = False

    # if template:
    #   lang = template._render_lang(invoice_object.ids)[invoice_object.id]

    # if not lang:
    # lang = get_lang(record.env).code

    ctx = dict(
        mark_invoice_as_sent=True,
        active_ids=invoice_object.ids,  # Use  ids  and  not  id  (it  has  to  be  a  list)
        custom_layout="mail.mail_notification_paynow",
        model_description=invoice_object.with_context(lang=lang).type_name,
        force_email=True,
        default_res_model='account.move',
        default_use_template=bool(template),
    )
    values = {
        'model': 'account.move',
        'res_id': invoice_object.id,
        'template_id': template and template.id or False,
        'composition_mode': 'comment',
    }

    wizard = env['account.invoice.send'].with_context(ctx).create(values)
    wizard._compute_composition_mode()
    wizard.onchange_template_id()
    wizard.onchange_is_email()

    # If you want to send without printing the invoice use this function

    wizard._send_email()

    # If you want to send and print use this function
    # wizard.send_and_print_action()


