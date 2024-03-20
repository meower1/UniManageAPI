from fastapi import HTTPException
from persiantools.jdatetime import JalaliDate
from datetime import date
from re import search, match
from database import student_collection, lecturer_collection, course_collection

iran_city_list = [
    "اراک",
    "اردبیل",
    "تبریز",
    "اصفهان",
    "اهواز",
    "ایلام",
    "بجنورد",
    "بندرعباس",
    "بوشهر",
    "بیرجند",
    "ارومیه",
    "تهران",
    "خرم آباد",
    "رشت",
    "زاهدان",
    "زنجان",
    "ساری",
    "سمنان",
    "سنندج",
    "شهرکرد",
    "شیراز",
    "قزوین",
    "قم",
    "کرج",
    "کرمان",
    "کرمانشاه",
    "گرگان",
    "مشهد",
    "همدان",
    "یاسوج",
    "یزد",
]

lu_department_list = [
    "فنی و مهندسی",
    "علوم پایه",
    "ادبیات و علوم انسانی",
    "مدیریت و اقتصاد",
    "کشاورزی",
    "منابع طبیعی",
    "دامپزشکی",
    "شیمی",
]

lu_major_list = [
    "مهندسی کامپیوتر",
    "مهندسی برق الکترونیک",
    "مهندسی برق قدرت",
    "مهندسی مکانیک و پلیمر",
    "مهندسی معدن",
    "مهندسی عمران",
    "مهندسی شهرسازی",
]

current_gregorian_date = date.today()
solar_date = JalaliDate.to_jalali(
    current_gregorian_date.year,
    current_gregorian_date.month,
    current_gregorian_date.day,
)

current_time = str(solar_date).split("-")
current_year, current_month, current_day = (
    int(current_time[0]),
    int(current_time[1]),
    int(current_time[2]),
)


def contains_specialchar_num(text):
    contains_specialcharacter_or_number = any(
        chr.isdigit() or (not chr.isalnum() and chr != " ") for chr in text
    )
    return contains_specialcharacter_or_number


def contains_specialchar(text):
    contains_specialcharacter = any(not chr.isalnum() for chr in text)
    return contains_specialcharacter


# def is_persian(text):
#     is_it_persian = langid.classify(text)[0] in ["fa", "ar"]
#     return is_it_persian


def is_persian(input_string: str) -> bool:
    pattern = r"[\u0600-\u06FF\u0750-\u077F\u08A0-\u08FF\uFB50-\uFDFF\uFE70-\uFEFF ]"
    if search(pattern, input_string):
        return True
    return False


def is_national_id(input_string: str) -> bool:
    pattern = r"([\u0627][\u0644][\u0641]|[\u0628-\u06CC])[/][0-9]{2}\s{1}[0-9]{6}"
    if search(pattern, input_string):
        return True
    return False


# Checks for every character in the string to be an integer
# We do this so we can do all the regex operations on the string yet still making sure
# Its a number.
def is_digit(num):
    return all(char.isdigit() for char in num)


def is_iranian_phone_number(phone_number):
    # Remove the leading '+' sign if present
    phone_number = phone_number.lstrip("+")

    # Define the regex pattern for an Iranian phone number
    pattern = r"^09[0-9]{9}$"

    # Check if the phone_number matches the pattern
    return bool(match(pattern, phone_number))


def is_valid_iranian_home_phone(phone_number):
    # valid_area_codes = [
    #     '021', '026', '031', '038', '051', '058', '061', '071', '077', '084',
    #     '086', '087', '011', '013', '017', '023', '024', '025', '028', '034',
    #     '035', '054', '056', '074', '076', '081'
    # ]

    pattern = r"^0[0-9]{2,}[0-9]{7,}$"
    matches = bool(match(pattern, phone_number))

    # if matches:
    #     area_code = phone_number[0:3]
    #     if area_code in valid_area_codes:
    #         return True

    # return False
    return matches


# definently written by myself
def is_national_code(text):
    if (
        len(text) != 10
        or text.isdigit() is False
        or text == "0000000000"
        or text[0] * 10 == text
    ):
        return False

    n = sum(int(text[i]) * (10 - i) for i in range(9))
    lastChar = int(text[9])
    remain = n % 11

    return (
        (remain == 0 and lastChar == 0)
        or (remain == 1 and lastChar == 1)
        or (remain > 1 and lastChar == 11 - remain)
    )


class DataValidation:
    async def duplicate_stid_check(stid):
        # Duplicate stid check
        student_stid = student_collection.find_one({"stid": stid})
        if student_stid:
            raise HTTPException(
                status_code=409, detail="Duplicate student id. Student already exists"
            )

    def stid_check(stid):
        if len(stid) != 11 or stid[3:9] != "114150":
            raise HTTPException(
                status_code=400,
                detail=f"Invalid student id. ex: {str(solar_date.year)[1:4]}11415001",
            )

    def name_check(name):
        if len(name) > 10:
            raise HTTPException(
                status_code=400, detail="Your name must be shorter than 10 characters"
            )

        if not is_persian(name):
            raise HTTPException(status_code=400, detail="Your name must be in persian")

        if contains_specialchar_num(name):
            raise HTTPException(
                status_code=400,
                detail="Name must not contain digits or special characters",
            )

    def birth_check(date):
        try:
            date_list = date.split("/")
            input_year = int(date_list[0])
            input_month = int(date_list[1])
            input_day = int(date_list[2])

            if input_month >= 1 and input_month <= 6:
                if not (input_day >= 1 and input_day <= 31):
                    raise HTTPException(
                        status_code=400, detail="Day value must be between 1-31"
                    )

            if input_month >= 7 and input_month <= 11:
                if not (input_day >= 1 and input_day <= 30):
                    raise HTTPException(
                        status_code=400,
                        detail="Day value must be between 1-30 ex: 1383/11/01",
                    )

            if input_month == 12:
                if not (input_day >= 1 and input_day <= 29):
                    raise HTTPException(
                        status_code=400,
                        detail="Day value must be between 1-29 ex: 1383/11/01",
                    )

            if input_year <= (current_year - 120) or (input_year >= current_year):
                raise HTTPException(
                    status_code=400,
                    detail=f"Year value must be between {current_year - 120} and {current_year} ex: 1383/11/01",
                )

        except (IndexError, ValueError):
            raise HTTPException(
                status_code=400, detail="Invalid birthdate. ex: 1383/11/01"
            )

    def ids_check(ids):
        if not is_national_id(ids):
            raise HTTPException(
                status_code=400, detail="Incorrect national id format. ex: ب/12 123456"
            )

        # if ids[4] not in persian_char_list:
        #     raise HTTPException(status_code=400, detail="The fourth digit of the National id must be a persian character")

        # if contains_specialchar(ids):
        #     raise HTTPException(status_code=400, detail="National id should not contain special characters")

    def borncity_check(borncity):
        if borncity not in iran_city_list:
            raise HTTPException(
                status_code=400, detail="Borncity must be a valid iranian city"
            )

    def address_check(addr):
        if len(addr) > 100:
            raise HTTPException(
                status_code=400, detail="Address lenght must not surpass 100 characters"
            )

    def postalcode_check(postalcode):
        if (
            len(str(postalcode)) != 10
            or not is_digit(postalcode)
            or contains_specialchar(postalcode)
        ):
            raise HTTPException(
                status_code=400,
                detail="Invalid postal code. Postal code must be 10 digits and not contain any special characters or letters",
            )

    def phonenum_check(phonenum):
        phonenum = phonenum.lstrip("+")
        if (
            not is_iranian_phone_number(phonenum)
            or not is_digit(phonenum)
            or contains_specialchar(phonenum)
        ):
            raise HTTPException(
                status_code=400,
                detail="Phone number must be a valid Iranian number. ex: 989123456789",
            )

    def homenum_check(homenum):
        if not is_valid_iranian_home_phone(homenum):
            raise HTTPException(
                status_code=400, detail="Incorrect home number format. ex: 0211234567"
            )

    def department_check(department):
        if department not in lu_department_list:
            raise HTTPException(
                status_code=400,
                detail=f"Department must be one of the following : {lu_department_list}",
            )

    def major_check(major):
        if major not in lu_major_list:
            raise HTTPException(
                status_code=400,
                detail=f"Major must be one of the following : {lu_major_list}",
            )

    # def married_check(married):
    #     if married not in ['مجرد', 'متاهل']:
    #         raise HTTPException(status_code=400, detail="Married status must be one of the following ['متاهل', 'مجرد']")

    def id_check(id):
        if not is_national_code:
            raise HTTPException(status_code=400, detail="Invalid national code")

    async def student_lid_exists(lids):
        # Checks to see if lecturers assigned to a student exist in lecturer list
        if lids is not None:
            for i in lids:
                lecturer_exists = lecturer_collection.find_one({"lid": str(i)})
                if lecturer_exists == None:
                    raise HTTPException(
                        status_code=404,
                        detail=f"Invalid lecturer id. Lecturer id: {i} doesn't exist",
                    )

    async def student_course_exists(scourseids):
        # Checks to see if courses assigned to a student exist in courses list
        if scourseids is not None:
            for i in scourseids:
                course_exists = course_collection.find_one({"cid": str(i)})
                if course_exists is None:
                    raise HTTPException(
                        status_code=404,
                        detail=f"Invalid course id. course id: {i} doesn't exist",
                    )

    async def student_duplicate_lids(lids):
        # Duplicate LIDs check: checks so the same lid doesn't exist twice in lids list
        if lids is not None:
            if len(lids) != len(set(lids)):
                raise HTTPException(
                    status_code=409, detail=f"Duplicate lecturer id. lids: {lids}"
                )

    async def student_duplicate_scourseids(scourseids):
        # Duplicate ScourseIDs check: checks so the same course id doesn't exist twice in scourseids list after update
        if scourseids is not None:
            if len(scourseids) != len(set(scourseids)):
                raise HTTPException(
                    status_code=409,
                    detail=f"Duplicate student courses id. scourseid: {scourseids}",
                )

    # --- Lecturer validation functions

    def lid_check(lid):
        if len(lid) != 6 or not is_digit(lid) or contains_specialchar(lid):
            raise HTTPException(status_code=400, detail="Invalid lecturer id")

    async def duplicate_lid_check(lid):
        lecturer_lid = lecturer_collection.find_one({"lid": lid})
        if lecturer_lid:
            raise HTTPException(
                status_code=409, detail="Duplicate lecturer id. lecturer already exists"
            )

    async def lcourseids_exist(lcourseids):
        # Checks to see if courses assigned to a lecturer exist in courses list
        if lcourseids is not None:
            for i in lcourseids:
                course_exists = course_collection.find_one({"cid": str(i)})
                if course_exists == None:
                    raise HTTPException(
                        status_code=404,
                        detail=f"Invalid course id. Course id: {i} doesn't exist",
                    )

    # --- Courses validation functions

    def cid_check(cid):
        if len(cid) != 5 or not is_digit(cid) or contains_specialchar(cid):
            raise HTTPException(
                status_code=400,
                detail="Invalid course id. Course id must be 5 digits and not contain any speical characters",
            )

    def name_check_courses(name):
        if len(name) > 25 or not is_persian(name) or contains_specialchar_num(name):
            raise HTTPException(
                status_code=400,
                detail="Course name must be in Persian, shorter than 25 characters, and not contain any special characters or numbers",
            )

    def credit_check(credit):
        if (
            not (int(credit) >= 1 and int(credit) < 4)
            or not is_digit(credit)
            or contains_specialchar(credit)
        ):
            raise HTTPException(
                status_code=400,
                detail="Course credit must be between 1-3 and not contain any letter or special character",
            )

    async def duplicate_cid_check(cid, table):
        # Course duplication check based on CID
        course_cid = table.find_one({"cid": cid})
        if course_cid:
            raise HTTPException(
                status_code=409, detail="Duplicate course id. Course already exists"
            )

    async def cid_exists(cid):
        # Checks to see if presentedcourses cid exists in courses cid list
        if cid is not None:
            course_exists = course_collection.find_one({"cid": cid})
            if course_exists == None:
                raise HTTPException(
                    status_code=404,
                    detail=f"Invalid course id. Course id: {cid} doesn't exist in the courses collection",
                )

    async def stid_exists(sid):
        # Checks if courseregister.sid exists in STID's of student table
        if sid is not None:
            for i in sid:
                student_exists = student_collection.find_one({"stid": str(i)})
                if student_exists == None:
                    raise HTTPException(
                        status_code=404,
                        detail=f"Invalid student id. Student id: {i} doesn't exist",
                    )
