from datetime import datetime
from uuid import UUID as UUIDHelper
from flaskFormRequest.validators import (
    Accepted,
    After,
    AfterOrEqual,
    Alpha,
    AlphaDash,
    AlphaNum,
    Array,
    Before,
    BeforeOrEqual,
    Between,
    Boolean,
    Callable,
    Confirmed,
    CurrentPassword,
    Date,
    DateEquals,
    Declined,
    Different,
    Digits,
    DigitsBetween,
    Distinct,
    Email,
    Exists,
    File,
    Filled,
    Float,
    Gt,
    Gte,
    In,
    Integer,
    IP,
    Json,
    Lt,
    Lte,
    MacAddress,
    Max,
    Min,
    NotIn,
    NotRegex,
    Nullable,
    Prohibited,
    Numeric,
    Regex,
    Required,
    Same,
    Size,
    String,
    Unique,
    UUID,
    CollectionErrors,
    NoneValueException,
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


def test_array():
    array = Array()
    assert array([0, 1,], 'listfield', {}, request) == [0, 1,]
    array = Array(rules=[Nullable(), Boolean()])
    assert array([0, 1,], 'listfield', {}, request) == [False, True]
    assert array([0, True, None], 'listfield', {}, request) == [False, True, None]

    message = 'Este campo debe ser una lista o una tupla'
    array = Array(message)
    try:
        array("foo", 'stringfield', {}, request)
        assert False
    except ValidationError as err:
        assert str(err) == message

    array = Array(rules=[Nullable(), Boolean()])
    try:
        array([True, "foo", False, "bar", None], 'listfield', {}, request)
        assert False
    except CollectionErrors as err:
        assert isinstance(err.errors, dict)


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


def test_callable():
    def custom_rule(value, field, request):
        return True
    call = Callable(custom_rule)
    assert call("foo", "", {}, request) == "foo"

    def custom_rule(value, field, request):
        return False
    message = "Este campo es incorrecto"
    call = Callable(custom_rule, message=message)

    try:
        call("foo", "", {}, request)
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

    message = 'La contrase??a es incorrecta'
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


def test_distinct():
    distinct = Distinct()
    assert distinct([1, 2, 3, 4, 5], "", {}, request) == [1, 2, 3, 4, 5]

    message = "Los elementos en la lista deben ser unicos"
    distinct = Distinct(message=message)

    try:
        distinct([1, 2, 1, 2, 1, 3, 4], '', {}, request)
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


def test_float():
    floatRule = Float()
    assert floatRule("3.14", '', {}, request) == 3.14
    assert floatRule(3.14, '', {}, request) == 3.14
    assert floatRule(1, '', {}, request) == 1.0

    message = "Este campo deber ser de tipo flotante"
    floatRule = Float(message=message, parse=False)
    assert floatRule("3.14", '', {}, request) == "3.14"

    try:
        floatRule('foo', '', {}, request)
        assert False
    except StopValidation as err:
        assert str(err) == message


def test_filled():
    filled = Filled()
    assert filled('foo', '', {}, request) == 'foo'
    assert filled([0, 1, 2], '', {}, request) == [0, 1, 2]
    assert filled((0, 1, 2), '', {}, request) == (0, 1, 2)
    assert filled({"foo": "bar"}, '', {}, request) == {"foo": "bar"}

    message = "Este campo debe tener un valor"
    filled = Filled(message=message)

    try:
        filled([], '', {}, request)
        assert False
    except StopValidation as err:
        assert str(err) == message


def test_gt():
    gt = Gt(length=2)
    assert gt('foo', '', {}, request) == 'foo'
    assert gt(3, '', {}, request) == 3
    assert gt([1,2,3], '', {}, request) == [1,2,3]

    message = "Este campo debe tener mas de 3 caracteres"
    gt = Gt(length=2, message=message)

    try:
        gt([], '', {}, request)
        assert False
    except ValidationError as err:
        assert str(err) == message


def test_gte():
    gte = Gte(length=3)
    assert gte('foo', '', {}, request) == 'foo'
    assert gte(3, '', {}, request) == 3
    assert gte(4, '', {}, request) == 4
    assert gte([1,2,3], '', {}, request) == [1,2,3]

    message = "Este campo debe tener 3 o m??s caracteres"
    gte = Gte(length=3, message=message)

    try:
        gte([1, 2], '', {}, request)
        assert False
    except ValidationError as err:
        assert str(err) == message


def test_in():
    inrule = In(('foo', 'bar'))
    assert inrule('foo', '', {}, request) == 'foo'

    message = "Este atributo debe ser foo o bar"
    inrule = In(('foo', 'bar'), message=message)

    try:
        inrule('zoo', '', {}, request)
        assert False
    except ValidationError as err:
        assert str(err) == message


def test_integer():
    integer = Integer()
    assert integer('1', '', {}, request) == 1
    assert integer('-1', '', {}, request) == -1
    assert integer(2, '', {}, request) == 2

    integer = Integer(parse=False)
    assert integer('2', '', {}, request) == '2'

    message = "Este atributo debe ser un numero entero"
    integer = Integer(message=message)

    try:
        integer(3.1416, '', {}, request)
        assert False
    except StopValidation as err:
        assert str(err) == message


def test_ip():
    ip = IP()
    assert ip("192.168.1.0", '', {}, request) == "192.168.1.0"
    assert ip("0.0.0.0", '', {}, request) == "0.0.0.0"
    assert ip("255.255.255.255", '', {}, request) == "255.255.255.255"

    ip = IP('v6')
    assert ip("2001:db8:85a3:8d3:1319:8a2e:370:7348", '', {}, request) == "2001:db8:85a3:8d3:1319:8a2e:370:7348"

    message = "Este atributo debe ser una IP valida"
    ip = IP(version='v4', message=message)
    try:
        ip("300.0.0.0", '', {}, request)
        assert False
    except ValidationError as err:
        assert str(err) == message

    message = "Este atributo debe ser una IP v6 valida"
    ip = IP(version='v6', message=message)
    try:
        ip("127.0.0.1", '', {}, request)
        assert False
    except ValidationError as err:
        assert str(err) == message


def test_json():
    jsonVal = Json()
    assert jsonVal("{}", '', {}, request) == {}
    assert jsonVal('{"foo": "bar"}', '', {}, request) == {"foo": "bar"}

    try:
        jsonVal = Json(rules={
            "foo": [Required(), Integer()],
            "bar": [Required()],
            "zoo": [Json(rules={
                "zing": [Required(), Integer()],
                "foo": [Json(rules={
                    "bar": [Required(), Integer()]
                })]
            })]
        })
        jsonVal('{"foo": "0", "bar": "world", "zoo": {"zing": "1", "foo": {"bar": "3"}}}', '', {}, request) == {"foo": "bar"}
    except CollectionErrors as err:
        assert False

    jsonVal = Json(parse=False)
    assert jsonVal("{}", '', {}, request) == "{}"
    assert jsonVal('{"foo": "bar"}', '', {}, request) == '{"foo": "bar"}'

    message = "Este campo debe ser un json valido"
    jsonVal = Json(message=message)
    try:
        jsonVal('{"foo": "bar",}', '', {}, request)
        assert False
    except ValidationError as err:
        assert str(err) == message


def test_lt():
    lt= Lt(length=4)
    assert lt('foo', '', {}, request) == 'foo'
    assert lt(3, '', {}, request) == 3
    assert lt([1,2,3], '', {}, request) == [1,2,3]

    message = "Este campo debe tener menos de 1 caracteres"
    lt = Lt(length=1, message=message)

    try:
        lt([0], '', {}, request)
        assert False
    except ValidationError as err:
        assert str(err) == message


def test_lte():
    lte = Lte(length=3)
    assert lte('foo', '', {}, request) == 'foo'
    assert lte(3, '', {}, request) == 3
    assert lte(2, '', {}, request) == 2
    assert lte([1,2], '', {}, request) == [1,2]

    message = "Este campo debe tener 2 o menos caracteres"
    lte = Lte(length=2, message=message)

    try:
        lte([1, 2, 3], '', {}, request)
        assert False
    except ValidationError as err:
        assert str(err) == message


def test_mac_address():
    macAddress = MacAddress()
    assert macAddress("AA:BB:CC:DD:EE:FF", '', {}, request) == "AA:BB:CC:DD:EE:FF"
    assert macAddress("AA-BB-CC-DD-EE-FF", '', {}, request) == "AA-BB-CC-DD-EE-FF"

    message = "Este atributo debe ser una MacAddress"
    macAddress = MacAddress(message=message)
    try:
        macAddress("abc", '', {}, request)
        assert False
    except ValidationError as err:
        assert str(err) == message


def test_max():
    max = Max(3)
    assert max('foo', '', {}, request) == 'foo'
    assert max([1,2,3], '', {}, request) == [1,2,3]
    assert max((1,2,3), '', {}, request) == (1,2,3)
    assert max({"foo": 0, "bar": 1, "zoo": 2}, '', {}, request) == {"foo": 0, "bar": 1, "zoo": 2}
    assert max(3, '', {}, request) == 3
    assert max(3.0, '', {}, request) == 3.0

    message = "Este campo debe tener maximo 5 caracteres"
    max = Max(5, message=message)

    try:
        max('foobar', '', {}, request)
        assert False
    except ValidationError as err:
        assert str(err) == message


def test_min():
    min = Min(3)
    assert min('foo', '', {}, request) == 'foo'
    assert min([1,2,3], '', {}, request) == [1,2,3]
    assert min((1,2,3), '', {}, request) == (1,2,3)
    assert min({"foo": 0, "bar": 1, "zoo": 2}, '', {}, request) == {"foo": 0, "bar": 1, "zoo": 2}
    assert min(3, '', {}, request) == 3
    assert min(3.0, '', {}, request) == 3.0

    message = "Este campo debe tener minimo 5 caracteres"
    min = Min(5, message=message)

    try:
        min('foo', '', {}, request)
        assert False
    except ValidationError as err:
        assert str(err) == message


def test_not_in():
    notinrule = NotIn(('foo', 'bar'))
    assert notinrule('zoo', '', {}, request) == 'zoo'

    message = "Este atributo no debe ser foo o bar"
    notinrule = NotIn(('foo', 'bar'), message=message)

    try:
        notinrule('foo', '', {}, request)
        assert False
    except ValidationError as err:
        assert str(err) == message


def test_not_regex():
    regex = NotRegex(r'\d{9,15}$')
    assert  regex('abc', '', {}, request) == 'abc'

    message = "Este campo debe ser un numero de telefono valido"
    regex = NotRegex(r'\d{9,15}$', message=message)

    try:
        regex('123123123', '', {}, request)
        assert False
    except ValidationError as err:
        assert str(err) == message


def test_nullable():
    nullable = Nullable()
    assert nullable('foo', '', {}, request) == 'foo'

    try:
        assert nullable(None, '', {}, request) == None
        assert False
    except NoneValueException:
        assert True


def test_prohibited():
    prohibited = Prohibited()
    assert prohibited(None, '', {}, request) == None
    assert prohibited("", '', {}, request) == ""
    assert prohibited([], '', {}, request) == []
    assert prohibited(tuple(), '', {}, request) == tuple()
    assert prohibited({}, '', {}, request) == {}

    message = "Este campo debe estar vac??o"
    prohibited = Prohibited(message=message)
    try:
        prohibited(True, '', {}, request)
        assert False
    except StopValidation as err:
        assert str(err) == message


def test_numeric():
    numeric = Numeric()
    assert numeric("3", '', {}, request) == 3
    assert numeric("3.14", '', {}, request) == 3.14

    message = "Este campo debe ser numerico"
    numeric = Numeric(message=message)

    try:
        numeric('foo', '', {}, request)
        assert False
    except ValidationError as err:
        assert str(err) == message


def test_regex():
    regex = Regex(r'\d{9,15}$')
    assert  regex('123123123', '', {}, request) == '123123123'

    message = "Este campo debe ser un numero de telefono valido"
    regex = Regex(r'\d{9,15}$', message=message)

    try:
        regex('bar', '', {}, request)
        assert False
    except ValidationError as err:
        assert str(err) == message


def test_same():
    same = Same("foo")
    assert same('foo', '', {}, request) == 'foo'

    message = "Este campo debe ser igual a bar"
    same_ = Same("bar", message=message)

    try:
        same_('foo', '', {}, request)
        assert False
    except ValidationError as err:
        assert str(err) == message


def test_size():
    size = Size(3)
    assert size('foo', '', {}, request) == 'foo'
    assert size([1,2,3], '', {}, request) == [1,2,3]
    assert size((1,2,3), '', {}, request) == (1,2,3)
    assert size({"foo": 0, "bar": 1, "zoo": 2}, '', {}, request) == {"foo": 0, "bar": 1, "zoo": 2}
    assert size(3, '', {}, request) == 3
    assert size(3.0, '', {}, request) == 3.0

    message = "Este campo debe tener 5 caracteres"
    size = Size(5, message=message)

    try:
        size('bar', '', {}, request)
        assert False
    except ValidationError as err:
        assert str(err) == message


def test_string():
    string = String()
    assert string('foo', '', {}, request) == "foo"
    assert string(None, '', {}, request) == "None"
    assert string(True, '', {}, request) == "True"
    assert string(123, '', {}, request) == "123"
    assert string(12.3, '', {}, request) == "12.3"
    assert string((1,2,), '', {}, request) == "(1, 2)"
    assert string([1,2,], '', {}, request) == "[1, 2]"
    assert string({"foo": 0,}, '', {}, request) == "{'foo': 0}"

    string = String(parse=False)
    assert string(1, '', {}, request) == 1

    message = "Este atributo debe ser un numero entero"
    string = String(message=message)

    # try:
    #     string(test_size, '', {}, request)
    #     assert False
    # except StopValidation as err:
    #     assert str(err) == message


def test_uuid():
    uuidRule = UUID()
    assert isinstance(
        uuidRule('553adce2-2261-458f-aa6c-9b766ccb7a49', '', {}, request),
        UUIDHelper
    )

    message = "Este campo debe ser un UUID valido"
    uuidRule = UUID(message=message, parse=False)

    assert uuidRule('553adce2-2261-458f-aa6c-9b766ccb7a49', '', {}, request) == '553adce2-2261-458f-aa6c-9b766ccb7a49'

    try:
        uuidRule('bar', '', {}, request)
        assert False
    except StopValidation as err:
        assert str(err) == message
