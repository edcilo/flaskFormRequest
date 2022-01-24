from datetime import datetime
from email import message
from flaskFormRequest.validators import (
    Accepted,
    After,
    AfterOrEqual,
    Alpha,
    AlphaDash,
    AlphaNum,
    Before,
    BeforeOrEqual,
    Between,
    Boolean,
    Confirmed,
    CurrentPassword,
    Date,
    DateEquals,
    Declined,
    Different,
    Digits,
    DigitsBetween,
    Email,
    ValidationError,
    StopValidation
)


request = []


def test_accepted():
    accepted = Accepted()
    assert accepted(True, '', {}, request) == True
    assert accepted(1, '', {}, request) == True
    assert accepted("yes", '', {}, request) == True
    assert accepted("on", '', {}, request) == True

    message = 'Este campo debe estar aceptado'

    accepted = Accepted(message, parse=False)
    assert accepted(True, '', {}, request) == True
    assert accepted(1, '', {}, request) == 1
    assert accepted("yes", '', {}, request) == "yes"
    assert accepted("on", '', {}, request) == "on"

    try:
        accepted(False, '', {}, request)
        assert False
    except ValidationError as err:
        assert str(err) == message


def test_after():
    future = datetime.strptime('2022-01-01 00:00:00', '%Y-%m-%d %H:%M:%S')
    after = After(future)
    assert isinstance(after('2022-01-19 21:00:00', 'datetime', {}, request), datetime)

    message = "Esta fecha es incorrecta"
    date = After(future, format='%d/%m/%Y %H:%M:%S', message=message)
    assert isinstance(date("12/01/2022 13:00:00", 'datetime', {}, request), datetime)

    after = After(future)
    try:
        assert isinstance(date("01/01/2021 13:00:00", 'datetime', {}, request), datetime)
        assert False
    except ValidationError as err:
        assert str(err) == message


def test_after_or_equal():
    future = datetime.strptime('2022-01-01 00:00:00', '%Y-%m-%d %H:%M:%S')
    after = AfterOrEqual(future)
    assert isinstance(after('2022-01-01 00:00:00', 'datetime', {}, request), datetime)

    message = "Esta fecha es incorrecta"
    date = AfterOrEqual(future, format='%d/%m/%Y %H:%M:%S', message=message)
    assert isinstance(date("01/01/2022 00:00:00", 'datetime', {}, request), datetime)
    assert isinstance(date("02/01/2022 00:00:00", 'datetime', {}, request), datetime)

    after = AfterOrEqual(future)
    try:
        assert isinstance(date("01/01/2021 13:00:00", 'datetime', {}, request), datetime)
        assert False
    except ValidationError as err:
        assert str(err) == message


def test_alpha():
    alpha = Alpha()
    assert alpha("justletters", '', {}, request) == "justletters"

    message = 'Este campo solo puede contener letras'

    alpha = Alpha(message)

    try:
        alpha("./?", '', {}, request)
        assert False
    except ValidationError as err:
        assert str(err) == message


def test_alpha_dash():
    alpha_dash = AlphaDash()
    assert alpha_dash("letters_123-", '', {}, request) == "letters_123-"

    message = 'Este campo solo puede contener letras, numeros y guiones bajos o medios'

    alpha_dash = AlphaDash(message)

    try:
        alpha_dash("*?.", '', {}, request)
        assert False
    except ValidationError as err:
        assert str(err) == message


def test_alpha_num():
    alpha_num = AlphaNum()
    assert alpha_num("letters123", '', {}, request) == "letters123"

    message = 'Este campo solo puede contener letras y numeros'
    alpha_num = AlphaNum(message)

    try:
        alpha_num("_-/", '', {}, request)
        assert False
    except ValidationError as err:
        assert str(err) == message


def test_before():
    past = datetime.strptime('2022-01-01 00:00:00', '%Y-%m-%d %H:%M:%S')
    before = Before(past)
    assert isinstance(before('2021-12-01 00:00:00', 'datetime', {}, request), datetime)

    message = "Esta fecha es incorrecta"
    before = Before(past, format='%d/%m/%Y %H:%M:%S', message=message)
    assert isinstance(before("01/12/2021 00:00:00", 'datetime', {}, request), datetime)

    try:
        assert isinstance(before("02/01/2022 13:00:00", 'datetime', {}, request), datetime)
        assert False
    except ValidationError as err:
        assert str(err) == message


def test_before_or_equal():
    past = datetime.strptime('2022-01-01 00:00:00', '%Y-%m-%d %H:%M:%S')
    before = BeforeOrEqual(past)
    assert isinstance(before('2022-01-01 00:00:00', 'datetime', {}, request), datetime)
    assert isinstance(before('2021-12-31 00:00:00', 'datetime', {}, request), datetime)

    message = "Esta fecha es incorrecta"
    before = BeforeOrEqual(past, format='%d/%m/%Y %H:%M:%S', message=message)
    assert isinstance(before("01/01/2022 00:00:00", 'datetime', {}, request), datetime)

    try:
        assert isinstance(before("02/01/2022 00:00:00", 'datetime', {}, request), datetime)
        assert False
    except ValidationError as err:
        assert str(err) == message


def test_between():
    between = Between(min=3, max=6)
    assert between("foo", '', {}, request) == "foo"
    assert between("foobar", '', {}, request) == "foobar"
    assert between(3, '', {}, request) == 3
    assert between(6, '', {}, request) == 6
    assert between(['a', 'b', 'c'], '', {}, request) == ['a', 'b', 'c']
    assert between(['a', 'b', 'c', 'd', 'e', 'f'], '', {}, request) == ['a', 'b', 'c', 'd', 'e', 'f']

    message = 'Este campo solo puede contener letras y numeros'
    between = Between(min=3, max=6, message=message)

    try:
        between(0, '', {}, request)
        assert False
    except ValidationError as err:
        assert str(err) == message


def test_boolean():
    boolean = Boolean()
    assert boolean(True, '', {}, request) == True
    assert boolean("true", '', {}, request) == True
    assert boolean(1, '', {}, request) == True
    assert boolean("1", '', {}, request) == True
    assert boolean(False, '', {}, request) == False
    assert boolean("false", '', {}, request) == False
    assert boolean(0, '', {}, request) == False
    assert boolean("0", '', {}, request) == False

    message = 'Este campo solo puede ser true o false'
    boolean = Boolean(message=message, parse=False)
    assert boolean(True, '', {}, request) == True
    assert boolean("true", '', {}, request) == "true"
    assert boolean(1, '', {}, request) == 1
    assert boolean("1", '', {}, request) == "1"
    assert boolean(False, '', {}, request) == False
    assert boolean("false", '', {}, request) == "false"
    assert boolean(0, '', {}, request) == 0
    assert boolean("0", '', {}, request) == "0"

    try:
        boolean("foo", '', {}, request)
        assert False
    except ValidationError as err:
        assert str(err) == message


def test_confirmed():
    confirmed = Confirmed()
    assert confirmed('secret', 'password', {'password_confirmation': 'secret'}, request) == 'secret'

    message = 'Este campo no coincide con password_confirmacion'
    confirmed = Confirmed(suffix='_confirmacion', message=message)
    assert confirmed('secret', 'password', {'password_confirmacion': 'secret'}, request) == 'secret'

    try:
        confirmed("secret", 'password', {}, request)
        assert False
    except ValidationError as err:
        assert str(err) == message


def test_current_password():
    class User:
        def verify_password(self, password):
            return "secret" == password
    user = User()

    cp = CurrentPassword(user)
    assert cp("secret", "password", {}, request) == "secret"

    message = 'La contraseña es incorrecta'
    cp = CurrentPassword(user, message=message)

    try:
        cp("secreto", 'password', {}, request)
        assert False
    except ValidationError as err:
        assert str(err) == message


def test_date():
    date = Date()
    assert isinstance(date('2022-01-18', 'date', {}, request), datetime)

    message = 'Este campo no es una fecha valida'
    date = Date(format='%d/%m/%Y', message=message)
    assert isinstance(date("12/01/2022", 'date', {}, request), datetime)

    try:
        date("2022-01-12", 'date', {}, request)
        assert False
    except ValidationError as err:
        assert str(err) == message


def test_date_equals():
    date0 = datetime.strptime('2022-01-01 00:00:00', '%Y-%m-%d %H:%M:%S')
    equals = DateEquals(date0)
    assert isinstance(equals('2022-01-01 00:00:00', 'datetime', {}, request), datetime)

    message = "Esta fecha es incorrecta"
    equals = DateEquals(date0, format='%d/%m/%Y %H:%M:%S', message=message)
    assert isinstance(equals("01/01/2022 00:00:00", 'datetime', {}, request), datetime)

    try:
        assert isinstance(equals("02/01/2022 00:00:00", 'datetime', {}, request), datetime)
        assert False
    except ValidationError as err:
        assert str(err) == message


def test_declined():
    declined = Declined()
    assert declined(False, '', {}, request) == False
    assert declined(0, '', {}, request) == False
    assert declined("no", '', {}, request) == False
    assert declined("off", '', {}, request) == False

    message = 'Este campo debe estar aceptado'

    declined = Declined(message, parse=False)
    assert declined(False, '', {}, request) == False
    assert declined(0, '', {}, request) == 0
    assert declined("no", '', {}, request) == "no"
    assert declined("off", '', {}, request) == "off"

    try:
        declined(True, '', {}, request)
        assert False
    except ValidationError as err:
        assert str(err) == message


def test_different():
    different = Different(field='foo')
    assert different('zoo', '', {"foo": "bar"}, request) == 'zoo'

    message = 'Este campo debe ser distinto a foo'
    different = Different(field='foo', message=message)

    try:
        different('bar', '', {"foo": "bar"}, request)
        assert False
    except ValidationError as err:
        assert str(err) == message


def test_digits():
    digits = Digits(length=3)
    assert digits("123", "", {}, request) == 123

    message = "Este campo debe ser un numero de 3 digitos"
    digits = Digits(length=3, message=message)

    try:
        digits('bar', '', {}, request)
        assert False
    except ValidationError as err:
        assert str(err) == message


def test_digits_between():
    digits = DigitsBetween(min=3, max=6)
    assert digits("123", "", {}, request) == 123
    assert digits("123456", "", {}, request) == 123456

    message = "Este campo debe ser un numero entre 3 y 6 digitos"
    digits = DigitsBetween(min=3, max=6, message=message)

    try:
        digits('12', '', {}, request)
        assert False
    except ValidationError as err:
        assert str(err) == message


def test_email():
    email = Email()
    assert email('me@example.com', "", {}, request) == 'me@example.com'

    message = "Este campo debe ser un email valido"
    digits = Email(message=message)

    try:
        digits('12', '', {}, request)
        assert False
    except ValidationError as err:
        assert str(err) == message
