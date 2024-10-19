# from hareefa.utils.helper import validate_email,valid_phone_number,validate_password
# import pytest



# @pytest.mark.skip
# def test_validate_email():
#     valid_mail = validate_email("jane-doe+123@example.co.uk")
#     assert valid_mail == True
#     valid_mail = validate_email("first.last@subdomain.example.org")
#     assert valid_mail == True
#     valid_mail = validate_email("john.doe..example@example.com")
#     assert valid_mail == False
#     valid_mail = validate_email("john..doe@example.com")
#     assert valid_mail == False
#     valid_mail = validate_email(".jane@example.com")
#     assert valid_mail == False
#     valid_mail = validate_email("john.@example.com")
#     assert valid_mail == False
#     valid_mail = validate_email("jane@-example.com")
#     assert valid_mail == False
#     valid_mail = validate_email("john.doe@example,com")
#     assert valid_mail == False
#     valid_mail = validate_email("john_doe@ex@ample.co")
#     assert valid_mail == False
#     valid_mail = validate_email("john<>doe@example.com")
#     assert valid_mail == False


# @pytest.mark.parametrize("phone_number",[
#     "+201002290644",
#     "+201002290634",
#     "+201002290644",
# ])
# @pytest.mark.skip
# def test_validate_phone_number(phone_number):
#     assert valid_phone_number(phone_number) == True
    

# @pytest.mark.skip
# @pytest.mark.parametrize("phone_number",[
#     "+20002290644",
#     "20100229034",
#     "+01002290644",
# ])
# def test_validate_phone_number(phone_number):
#     assert valid_phone_number(phone_number) == False


# @pytest.mark.parametrize("password",[
#     "1234567899",
#     "1234",
#     "12345698mos",
#     "12345698mosMOS",
#     "12345698mos$",
#     "12345698mos@",
#     "12345698$",
#     "12345698*",

# ])
# def test_validate_password(password):
#     assert validate_password(password) == False


# @pytest.mark.parametrize("password",[
#     "mosssssssMOS11@",
#     "kkkkkmosMOS11@",
# ])
# def test_validate_password(password):
#     assert validate_password(password) == True