
from twilio.rest import Client
def Send_message(
    account_sid = 'twilio API sid',  # copy and paste API sid
    auth_token = 'twilio API token',   # copy and paste API token
    twilio_active_number = '+area code and number',  # api ActiveNumber (virtual twilio number)
    to = '+area code and number',
    body = '\n python alerta',
    ):
    
    client = Client(account_sid, auth_token)  # Autenticación de cuenta
    message = client.messages.create(
        from_ = twilio_active_number,
        to = to,  # area code + receiver number
        body = body,   #Contenido SMS personalizado
        )
    
if __name__ == '__main__':
    Send_message()

