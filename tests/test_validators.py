from flaskFormRequest.validators import (
    Accepted,
    Alpha,
    AlphaDash,
    AlphaNum,
    Between,
    Boolean,
    Confirmed,
    CurrentPassword,
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
