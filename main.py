import flask, os
import logging, time
from functools import wraps
from pywa import WhatsApp, filters
from pywa.types import Message, SectionList, CallbackSelection, Section, SectionRow, CallbackButton, Button
from pywa.filters import text, callback
# from pywa.types import FlowCategory
from pywa.types import Template as Temp
from utilities import translate_text, get_coordinates, get_nearest_police_station

from googletrans import Translator


flask_app = flask.Flask(__name__)
translator = Translator()

session_context = {}
nl = '\n'
wa = WhatsApp(
    phone_id='',
    token='',
    server=flask_app,
    callback_url='https://69.ngrok-free.app',
    verify_token='',
    app_id=69,
    app_secret='',
    # business_account_id=,
)


# wrapper
def with_language(func):
    @wraps(func)
    def wrapper(client, clb):
        dest = session_context.get(clb.from_user.wa_id, 'en')
        return func(client, clb, dest)
    return wrapper



# translator.translate('Namaste', dest='hi').text
@wa.on_message(filters.text.matches('Hello', 'Hi', ignore_case=True))
def hello(client: WhatsApp, msg: Message):
    # print(client)
    # print(msg)
    # translation = 
    msg.reply_text(
        text=f'''{translate_text("Namaste", 'hi')}🙏\nNamaste 🙏\n{translate_text("Namaste", 'mr')}\n\n{translate_text("Deepcytes welcomes you", 'hi')} \nDeepcytes welcomes you\n{translate_text("Deepcytes welcomes you", 'mr')}\n\n{translate_text("To proceed, please select a language", 'hi')}\nTo proceed, please select a language\n{translate_text("To proceed, please select a language", 'mr')}''',
        buttons=[
            Button(
                title='english',
                callback_data='lang:en'
            ),
            Button(
                title=f'{translate_text("hindee", "hi")}',
                callback_data='lang:hi'
            ),
            Button(
                title=f'{translate_text("marathi", "mr")}',
                callback_data='lang:mr'
            )
        ]
    )

@wa.on_callback_button(callback.data_startswith('lang'))
def main_dailog(client: WhatsApp, clb: CallbackButton):
    # print(clb.from_user.wa_id)
    # print(session_context)
    # if clb.from_user.wa_id in session_context:
    #     dest = session_context[clb.from_user.wa_id]
    # else:
    #     dest = 'en'
    dest = clb.data.split(':')[1]
    text = f'''You have chosen:\n✅{dest} language\n\nWe are happy to connect with you.\nWhat would you like to explore today?\n\nour website - deepcytes.io'''
    
    msg_id = clb.reply_text(
        # text=f'''{translator.translate(f'You have chosen:{nl}{nl}', dest='hi').text}'''
        text=f'''{translator.translate(f'{text}', dest=dest).text}''',
        buttons=SectionList(
            button_title=f"{translator.translate(f'Select an option', dest=dest).text}",
            sections=[
                Section(
                    title="section 1",
                    rows=[
                        SectionRow(
                            title=f"{translator.translate(f'Cyber Crime', dest=dest).text}",
                            description=f"{translator.translate(f'How to Report a Cyber Crime Complaint', dest=dest).text}",
                            callback_data=f"section1:report_cc",
                        ),
                        SectionRow(
                            title=f"{translator.translate(f'Police Station', dest=dest).text}",
                            description=f"{translator.translate(f'Find Nearest Police Station', dest=dest).text}",
                            callback_data=f"section1:police_station",
                        ),
                        SectionRow(
                            title=f"{translator.translate(f'phone hacked?', dest=dest).text}",
                            description=f"{translator.translate(f'Check if your Phone has been hacked?', dest=dest).text}",
                            callback_data=f"section1:phone_hacked",
                        ),
                        SectionRow(
                            title=f"{translator.translate(f'check aadhar link?', dest=dest).text}",
                            description=f"{translator.translate(f'Check if your Aadhar is linked to other mobile numbers', dest=dest).text}",
                            callback_data=f"section1:aadhar_link",
                        ),
                        SectionRow(
                            title=f"{translator.translate(f'personal data leak?', dest=dest).text}",
                            description=f"{translator.translate(f'Check if your personal details are leaked on Dark Web', dest=dest).text}",
                            callback_data=f"section1:data_leak",
                        ),
                    ],
                ),
            ]
        )
    )
    print(msg_id)
    print(clb)

@wa.on_callback_selection(callback.data_startswith('section1'))
@with_language
def main_dailog_response(client: WhatsApp, clb: CallbackSelection, dest: str):
    if clb.data == 'section1:report_cc':
        text = 'Steps on how to report a cyber crime\nstay safe\nblah blah blah\n\n\nDo you require our assistance?'
        clb.reply_text(
            text=f"{translator.translate(text, dest=dest).text}",
            buttons=[
                Button(
                    title=f'{translator.translate("yes", dest=dest).text}',
                    callback_data='assistance:yes'
                ),
                Button(
                    title=f'{translator.translate("no", dest=dest).text}',
                    callback_data='exit'
                ),
            ]
        )
    elif clb.data == 'section1:police_station':
        clb.reply_text(
            text=f"{translator.translate('Search police station based on:', dest=dest).text}",
            buttons=[
                Button(
                    title=f'{translator.translate("pincode", dest=dest).text}',
                    callback_data='ps:pincode'
                ),
                Button(
                    title=f'{translator.translate("location", dest=dest).text}',
                    callback_data='ps:location'
                ),
            ]
        )
    elif clb.data == 'section1:phone_hacked':
        re = clb.reply_template(
            template=Temp(
                name='phone_hacked',
                language=Temp.Language.ENGLISH,
            ),
        )
        print(f"\n\n\nre - {re}\n\n\n")
        time.sleep(0.3)
        take_email(client, clb)
        # clb.reply_text(text='please provide your email address')
    elif clb.data == 'section1:aadhar_link':
        clb.reply_template(
            template=Temp(
                name='aadhar_link',
                language=Temp.Language.ENGLISH,
            ),
        )
        time.sleep(0.3)
        handle_fir_resoponse(client, clb)
    elif clb.data == 'section1:data_leak':
        clb.reply_template(
            template=Temp(
                name='data_leak',
                language=Temp.Language.ENGLISH,
            ),
        )
        time.sleep(0.3)
        handle_fir_resoponse(client, clb)

@wa.on_callback_button(callback.data_startswith('assistance'))
@with_language
def assistance(client: WhatsApp, clb: CallbackButton, dest: str):
    clb.reply_text(
        text='Select Nature of Issue:\n',
        buttons=SectionList(
            button_title='Select an option',
            sections=[
                Section(
                    title="section 1",
                    rows=[
                        SectionRow(
                            title=f" ",
                            description=f"Suspicious transactions/Financial Frauds",
                            callback_data=f"email:ff",
                        ),
                        SectionRow(
                            title=f" ",
                            description=f"Impersonation/Identity Theft",
                            callback_data=f"email:it",
                        ),
                        SectionRow(
                            title=f" ",
                            description=f"Malware/Virus",
                            callback_data=f"email:mv",
                        ),
                        SectionRow(
                            title=f" ",
                            description=f"Unauthorized access to your social media accounts",
                            callback_data=f"email:ua",
                        ),
                        SectionRow(
                            title=f" ",
                            description=f"Report stolen phone/sim card",
                            callback_data=f"email:sp",
                        ),
                        SectionRow(
                            title=f" ",
                            description=f"Stop scam messages",
                            callback_data=f"email:sm",
                        ),
                        SectionRow(
                            title=f" ",
                            description=f"Other concerns",
                            callback_data=f"email:oc",
                        ),
                    ],
                ),
            ]
        )
    )

@wa.on_callback_selection(callback.data_startswith('email'))
@with_language
def take_email(client: WhatsApp, clb: CallbackSelection, dest: str):
    clb.reply_text(
        text='Please provide your email address\n',
    )

@wa.on_message(filters.text.regex(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'))
@with_language
def handle_email(client: WhatsApp, msg: Message, dest: str):
    msg.reply_text(
        text='Have filed an FIR or any complaint on cyber portal?',
        buttons=[
            Button(
                title='yes',
                callback_data='fir:yes'
            ),
            Button(
                title='no',
                callback_data='fir:no'
            ),
        ]
    )

@wa.on_callback_button(callback.data_startswith('fir'))
@with_language
def handle_fir_resoponse(client: WhatsApp, clb: CallbackButton, dest: str):
    if hasattr(clb, 'data') and clb.data == 'fir:yes': # for message
        clb.reply_text('Please enter your FIR Number')
    else: # ['section1:data_leak','section1:aadhar_link','fir:no']
        clb.reply_text(
            text="Anything specific you'd like to discuss/any questions (long text type)\nyou can ask the question or click on the exit button",
            footer="your question will be recorded and we will get back to you",
            # tracker='a32k',
            buttons=[
                Button(
                    title='exit',
                    callback_data='exit'
                ),
            ]
        )

@wa.on_message(filters.text.regex(r'^\d{10}$')) #regex to check if the message is 10 characters numeric. just a workaroud. use wp flows instead
@with_language
def fir_number(client: WhatsApp, msg: Message, dest: str):
    msg.reply_text(text='we have recorded your FIR number. our team will verify and get back to you')
    time.sleep(0.2)
    print(f"msg - {msg}")
    handle_fir_resoponse(client,msg)

@wa.on_message(filters.text.regex(r'.{21,}')) #regex to check if the message is above 20 characters. just a workaroud. use wp flows instead
@with_language
def large_question(client: WhatsApp, msg: Message, dest: str):
    msg.reply_text(
        text='thanks!\nyour response has been recorded and we will get back to you.\n\ndo you need extra help?',
        buttons=[
            Button(
                title='yes',
                callback_data='lang:en'
            ),
            Button(
                title='no',
                callback_data='exit'
            ),
        ]
    )

@wa.on_callback_button(callback.data_startswith('ps')) 
@with_language
def handle_ps_response(client: WhatsApp, clb: CallbackButton, dest: str):
    # return
    if clb.data == 'ps:location':
        clb.reply_text(
            text=translate_text('Please provide a location\n',dest)
        )
    else:
        clb.reply_text(
            text=translate_text('Please provide a pincode\n',dest)
        )

@wa.on_message(filters.text.regex(r'^\d{6}$'))
@with_language
def handle_pincode(client: WhatsApp, msg: Message, dest: str):
    pincode = msg.text
    lat, lng = get_coordinates(pincode)
    nl = '\n'
    if lat and lng:
        results = get_nearest_police_station(f"{lat}, {lng}")
        msg.reply_text(
            text=translate_text(f'{results[:4000]}',dest)
        )
    else:
        msg.reply_text(
            text=translate_text(f'pincode not found!',dest)
        )
    time.sleep(0.1)
    exit(client, msg)

@wa.on_message(filters.location.any)
@with_language
def handle_location(client:WhatsApp, location:Message, dest: str):
    lat, lng = location.location.latitude, location.location.longitude
    if lat and lng:
        results = get_nearest_police_station(f"{lat}, {lng}")
        # print(results)
        # return
        nl = "\n"
        location.reply_text(
            text=translate_text(f'{results[:4000].replace("9999","*").replace("1111",f"{nl}")}',dest)
        )
    else:
        location.reply_text(
            text=translate_text(f'pincode not found from location!',dest)
        )
    time.sleep(0.1)
    exit(client, location)


# exit
@wa.on_callback_button(callback.data_startswith('exit'))
@with_language
def exit(client: WhatsApp, clb: CallbackButton, dest: str):
    clb.reply_text(text=translate_text("Tips to Stay Safe and Updates regarding recent cyber crimes\n\nthank you ",dest))


# for testing
@wa.on_raw_update()
def raw_update_handler(_: WhatsApp, update: dict):
    try:
        # print(f"\nupdate-{update['entry'][0]['changes'][0]['value']['contacts'][0]['wa_id']}")
        if not update['entry'][0]['changes'][0]['value']['contacts'][0]['wa_id'] in session_context:
            session_context[update['entry'][0]['changes'][0]['value']['contacts'][0]['wa_id']] = (update['entry'][0]['changes'][0]['value']['messages'][0]['interactive']['button_reply']['id']).split(':')[1]
    except KeyError as e:
        # print(e)
        # print(f"\nupdate-{update}")
        pass
    # print(update)
    finally:
        # pass
        print(session_context)


flask_app.run(port=7000, debug=True)



#TODO
# whatsapp flows
# remove time sleep, instead use a solid method (read receipt)
# have to use database
# logging

