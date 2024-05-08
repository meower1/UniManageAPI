<p align="center">
    <img src="images/project_logo.jpeg" alt="UniManageAPI" height="400" width="400">
</p>

# سیستم مدیریت دانشگاهی بر پایه FastAPI

## نحوه انجام عملیات های CRUD

### عملیات درج (Create)

ورودی: مشخصات دانشجو را به عنوان ورودی وارد میکنیم

<!-- <img src="images/meow1.jpg" width="500" height="700"> -->

```json
{
  "stid": "40211415035",
  "fname": " میو ماو",
  "lname": "احمد",
  "father": "رضااحمدی",
  "birth": "1401/1/30",
  "ids": "ب/12 123456",
  "address": "میو میو",
  "postalcode": "1234567890",
  "cphone": "09123456789",
  "hphone": "06633223358",
  "major": "مهندسی برق قدرت",
  "married": true,
  "id": "1850527296",
  "scourseids": [12342],
  "lids": [777335],
  "department": "فنی و مهندسی",
  "borncity": "سمنان"
}
```

روتر Post بر اساس Scheme مشخص شده ورودی را دریافت و پردازش میکند

داده ها قبل از ثبت در پایگاه داده طبق استاندارد های تایین شده صحت سنجی میشوند.
صحت سنجی ها در فایل datavalidation.py تعبیه شده و در روتر مربوطه مورد استفاده قرار میگیرند

```python
await DataValidation.duplicate_stid_check(student.stid)
```

در نمونه فوق صحت سنجی مربوط به تکراری نبودن شماره دانشجویی فراخوانی شده که بصورت زیر عمل میکند

```python
async def duplicate_stid_check(stid: str) -> None:
    """
    Check if a student with the given student ID already exists in the database.
    """
    student_stid = student_collection.find_one({"stid": stid})
    if student_stid:
        raise HTTPException(
            status_code=409, detail="Duplicate student id. Student already exists"
        )
```

همانطور که مشاهده میشود برای صحت سنجی در مثال بالا اگر شماره دانشجویی ای که میخواهیم ثبت کنیم در پایگاه داده وجود داشته باشد ارور مناسب را دریافت میکنیم

و درصورتی که به ارور بر نخوریم رکورد ورودی در پایگاه داده ثبت خواهد شد و طبق response model چهار فیلد اولیه بازگردانی خواهد شد

```python
course_data = student.model_dump()
student_collection.insert_one(course_data)

return course_data
```

```python
class StudentOut(BaseModel):
    stid: str
    fname: str
    lname: str
    father: str
```

### عملیات ثبت (Read)

ورودی: شماره دانشجویی

روتر Get بر اساس شماره دانشجویی به دیتابیس درخواست فرستاده و رکورد مربوط به دانشجو را دریافت میکند

```python
@router.get("/GetStu/{student_id}", response_model=schemas.StudentUpdate)
async def get_student(student_id: str) -> dict[str, Any]:

    record = student_collection.find_one({"stid": student_id})
    if not record:
        raise HTTPException(
            status_code=404, detail="Invalid student id. Student not found"
        )
    return record
```

### عملیات آپدیت (Update)

ورودی: شماره دانشجویی و پارامتر هایی که میخواهیم آپدیت کنیم

پارامتر های مدنظر بعد از دریافت شدن توسط روتر Patch به json تبدیل میشوند و مقادیر None از json حذف میشود

```python
student_data = student.model_dump(exclude_unset=True)
```

سپس صحت سنجی روی مقادیر ورودی انجام شده و درصورت نبود ارور مقادیر تمدید شده و به عنوان خروجی باز گردانده میشوند

```json
{
	"cid": "12342",
	"Updated values":  [
		{
            "credit": "2"
			"department": "دامپزشکی",
		}
	]
}
```

### عملیات حذف (Delete)

ورودی: شماره دانشجویی

شماره دانشجویی توسط روتر Delete دریافت شده و رکورد دانشجوی مدنظر از پایگاه داده حذف میشود و سپس پیام تایید به علاوه شماره دانشجوی مدنظر بازگردانده میشود

```python
@router.delete("/DelStu/{student_id}", status_code=200)
async def delete_student(student_id: str):

    delete_record = student_collection.find_one_and_delete({"stid": student_id})
    if not delete_record:
        raise HTTPException(status_code=400, detail="Student was not deleted")
    return {"Student ID": student_id, "Deleted": True}
```

## داکرایز کردن پروژه (Containerization)

### بخش Fastapi

```Dockerfile
FROM python:latest
WORKDIR /app
COPY ./requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt
COPY ./app /app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
```

1- کانتینر با آخرین ورژن پایتون آماده میشود

2- مسیر اصلی پروژه را مشخص میکنیم /code

3- فایل نیازمندی های پروژه را در مسیر پروژه کپی میکنیم /code/requirements.txt

4- نیازمندی های پروژه را درون کانتینر نصب میکنیم

5- پروژه را از روی سیستم خود به داخل کانتینر میریزیم

6- پروژه را توسط uvicorn با پارامتر های مناسب اجرا میکنیم

### داکر کامپوز

فایل کامپوز پروژه رو برای اجرای همزمان دو سرویس mongodb و fastapi ایجاد میکنیم.

سرویس fastapi از فایل dockerfile پروژه کانتینر را ساخته و اجرا میکند و سپس پورت 80 را از هاست به کانتینر تخصیص میدهد

فایل کامپوز همچنین کانتینر شامل اخرین ورژن mongodb را دریافت کرده و اجرا میکند و ولوم mongodb را به مسیر /var/lib/mongodb/data درون کانتینر تخصیص میدهد

سپس هر دو سرویس را درون یک نتورک به نام main گذاشته و اجرا میکند
و همچنین هر دو سرویس تا وقتی که بصورت دستی متوقف نشوند در صورت کرش شدن خود به خود ری استارت میشوند

## تست نویسی

تست ها درون فولر tests نوشته شده اند و به دو دسته تقسیم میشوند

### تست های CRUD

بر روی هر روتر چهار عملیات CRUD انجام میشود

```python
def test_create_courses() -> None:
    """
    Test case for creating a new course
    """
    response = client.post("/RegCou/", json=Course_sample)
    assert response.status_code == 200
    assert response.json() == Course_sample
```

```python
def test_get_course() -> None:
    """
    Test case for getting a course
    """
    response = client.get("/GetCou/12342")
    assert response.status_code == 200
    assert response.json() == Course_sample
```

```python
def test_update_course() -> None:
    """
    Test case for updating a course
    """
    response = client.patch(
        "/UpdCou/12342",
        json={"cname": "میوععع", "department": "فنی و مهندسی", "credit": "2"},
    )
    assert response.status_code == 200
    assert response.json() == {
        "cid": "12342",
        "Updated values:": [
            {"cname": "میوععع", "department": "فنی و مهندسی", "credit": "2"}
        ],
    }
```

```python
def test_delete_course() -> None:
    """
    Test case for deleting a course
    """
    response = client.delete("/DelCou/12342")
    assert response.status_code == 200
    assert response.json() == {"Course ID": "12342", "Deleted": True}
```

### تست های صحت سنجی

تست های مرتبط با صحت سنجی روی داده های ورودی مرتبط با datavalidations.py

```python

def test_create_duplicate_course() -> None:
    """
    Test case for creating a duplicate course
    """
    response = client.post("/RegCou/", json=Course_sample)
    assert response.status_code == 409
    assert response.json() == {"detail": "Duplicate course id. Course already exists"}
```

## راه اندازی روی سرور

در اینجا از سیستم عامل ubuntu 20 استفاده شده است ولی رویکرد در ورژن های دیگر اوبانتو و توضیع های مبتنی بر دبیان مشابه است

ابتدا وارد سرور شده و پکیچ های سیستم را اپدیت و آپگرید میکنیم

```shell
sudo apt update && apt upgrade -y
```

با استفاده از اسکریپت نصب اتوماتیک داکر اقدام به نصب آن میکنیم

```shell
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh
```

پس از نصب داکر ابزار git را نصب میکنیم

```shell
sudo apt install git -y
```

سپس مخزن پروژه را از گیتهاب با استفاده از ابزار گیت کپی میکنیم

```shell
git clone https://github.com/meower1/UniManageAPI.git
```

به مسیر کپی شده رفته و فایل داکر کامپوز رو اجرا میکنیم

```shell
cd UniManageAPI
docker compose up -d
```

دستور اول (cd) به معنای change directory یا همان تغییر مسیر هست و برای تغییر مسیر از پوشه ای به پوشه دیگر استفاده میشود

دستور دوم فایل docker-compose.yaml را که درون مخزن پروژه قرار دارد را اجرا میکند
این فایل شامل 3 سرویس میشود.

### سرویس اول (MongoDB)

```yaml
services:
  mongo:
    container_name: mongodb
    image: mongo:latest
    restart: unless-stopped
    networks:
      - main
    ports:
      - 27017:27017
    volumes:
      - mongodb:/var/lib/mongodb/data
```

سرویس اول کانتینری با نام mongo اجرا میکند
از این نام برای فرا خواندن این سرویس بجای ایپی محلی سرویس استفاده میشود.
برای مثال در فایل database.py پروژه از این نام برای ادرس دهی به محل دیتابیس استفاده شده است
[اموزش و توضیحات بیشتر](https://www.youtube.com/watch?v=y_XFIidjtEs)

سپس آن را درون شبکه main گذاشته و پورت 27017 را از دستگاه هاست یعنی vps فعلی که روی آن هستیم به کانتینر مپ میکنیم. در این حالت تمام درخواست ها به پورت 27107 ما به پورت 27017 کانتینر میرود

با دستور

```yaml
restart: unless-stopped
```

به داکر میگوییم که تا وقتی بصورت دستی کانتینر را متوقف نکردیم آنرا استاپ نکن (یعنی در صورت کرش شدن بصورت خود به خود کانتینر رو ری استارت کند)

سپس در بخش

```yaml
volumes:
  - mongodb:/var/lib/mongodb/data
```

به داکر میگوییم که یک ولوم برای کانتینر mongo به اسم mongodb ساخته و آن را به مسیر /var/lib/mongodb/data متصل کند

در این صورت تمام اطلاعات مرتبط با این کانتینر درون ولوم mongodb ذخیره شده و درصورت تغییرات نظیر پاک شدن یا اپدیت شدن کانتینر این اطلاعات ثابت باقی میماند و حتی میتوانیم ولوم را به کانتینر های دیگر متصل کنیم. اجرای این عمل برای دیتابیس ها ضروری است

### سرویس دوم (FastAPI)

```yaml
fastapi:
  build: .
  command: ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
  ports:
    - 8080:8080
  environment:
    - PORT=8080
  volumes:
    - ./app:/app/
  depends_on:
    - mongo
  networks:
    - main
  restart: unless-stopped
```

در این سرویس fastapi با استفاده از فایل Dockerfile که در مسیر اصلی پروژه قرار دارد ساخته شده و پورت 8080 به آن تخصیص داده میشود

در اینجا (.) به معنای این است که فایل Dockerfile که کانتینر قرار است از روی آن ساخته شود هم در مسیر فعلی (یعنی مسیری که docker-compose.yaml در آن اجرا میشود) قرار دارد

محتوی Dockerfile:

```Dockerfile
FROM python:latest
WORKDIR /app
COPY ./requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt
COPY ./app /app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
```

```Dockerfile
FROM python:latest
```

در اینجا کانتینری آماده شامل آخرین ورژن python را نصب میکنیم
این کانتینر ابزار های پایه مورد استفاده مانند pip را بطور پیشفرض درون خود دارد

```Dockerfile
WORKDIR /app
```

در اینجا مسیر اصلی کاری پروژه را /app قرار میدهیم. با این کار داکر متوجه میشود که دستور های پروژه مانند COPY, RUN را در این مسیر اجرا کند.

```Dockerfile
COPY ./requirements.txt /app/requirements.txt
```

سپس فایل requirements.txt که شامل پکیج های پایتون مورد استفاده پروژه میشوند را از مسیر اصلی پروژه (root) به مسیر پروژه درون کانتینر /app/requirements.txt کپی میکنیم

- پارامتر --no-cache-dir به pip میگوید که پکیج هایی را که نصب میکند را در cache نکند که به کوچک تر شدن فضای اشتغالی docker image کمک میکند

- پارامتر --upgrade به pip میگوید پکیج هارا بعد از نصب به اخرین ورژن ارتقا دهد

```Dockerfile
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt
```

در این مرحله نیازمندی های پروژه را که کپی کردیم داخل کانتینر نصب میکنیم

```Dockerfile
COPY ./app /app
```

در این مرحله تمامی فایل های مرتبط با پروژه که درون مسیر /app قرار دارند را به مسیر /app درون کانتینر کپی میکنیم

```Dockerfile
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
```

سپس پروژه را با استفاده از uvicorn اجرا میکنیم
در اینجا به uvicorn میگوییم که app را که همان

```python
app = Fastapi()
```

است را در فایل main پیدا کند
سپس مسیر هاست را 0.0.0.0 مشخص میکنیم. در این حالت برنامه از هر آیپی ای قابل دسترس است درصورتی که این پارامتر را مشخص نکنیم این برنامه بطور پیشفرض از لوکال هاست (127.0.0.1) استفاده میکند و فقط از سیستم خودمان قابل دسترس خواهد بود

و همچنین پورت 8080 را به برنامه تخصیص میدهیم

در نتیجه تمامی درخواست ها به
vps_ip:8080

به برنامه میرود. که البته جلو تر با تنظیمات nginx آدرس ورودی تغییر میکند

```yaml
depends_on:
  - mongo
```

در اینجا به داکر میگوییم که این کانتینر مبتکی به سرویس mongo است و تا وقتی که کانتینر آن اجرا نشده است این سرویس را اجرا نکن

### سرویس سوم (Nginx)

```yaml
nginx:
  build: nginx
  ports:
    - 80:80
    - 443:443
  depends_on:
    - fastapi
  networks:
    - main
  restart: unless-stopped
```

در این سرویس یک کانتینر شامل nginx را نصب کرده و پورت 80,443 که بترتیب مربوط به https و http هستند را به آن تخصیص میدهیم

به آن میگوییم که مبتکی به سرویس fastapi هست و درون نتورک main قرار بگیرد و تا وقتی که بصورت دستی استاپ نشده است آنرا استاپ نکن

در نهایت درون فایل docker-compose.yaml مشخص میکنیم که سرویس های درون این فایل همگی درون شبکه main قرار دارند و این فایل شامل ولوم mongo میشود

```yaml
networks:
  main:
volumes:
  mongodb:
```

## Nginx

ابزاری با کاربرد های متنوع است که ما در اینجا از این ابزار برای Reverse proxy, Static file serving, SSL/TLS Management و HTTP to HTTPS Redirection استفاده میکنیم

### Static File Serving

```nginx
location /static/ {
    alias /app/static/;
}
```

در این بخش فایل های استاتیک پروژه (فایل هایی که ثابت هستند و تغییر نمیکنند مثل کد های css/javascript و عکس ها) توسط nginx توضیع میشوند.
Fastapi خود توانایی توضیع فایل های استاتیک را دارد ولی مزیت استفاده از nginx در سرعت و بهبود عملکردش در این حیطه است

در این بخش به nginx میگوییم که هروقت کاربر مسیر /static را فرا خواند به مسیر /app/static هدایت شود

### Reverse Proxy

```nginx
  upstream app_server {
    server fastapi:8080 fail_timeout=0;
  }
```

در این بخش به nginx گفته میشود که درخواست هایی که به app می آید را به کانتینر fastapi پورت 8080 بفرستد

### SSL/TLS Manamgement

```nginx
server {
    listen 443 ssl;
    ssl_certificate /etc/letsencrypt/live/uk1.meower1.tech/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/uk1.meower1.tech/privkey.pem;
    include /etc/letsencrypt/options-ssl-nginx.conf;
    ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem;
}
```

این بخش مربوط به مدیریت مجوز ssl است که بطور اتوماتیک توسط certbot گرفته شده است

### HTTP to HTTPS Redirection

```nginx
server {
  if ($host = uk1.meower1.tech) {
    return 301 https://$host$request_uri;
  }

  listen 80;
  server_name uk1.meower1.tech;
  return 404;
}
```

در این بخش nginx درخواست های http به سرور را به https منتقل میکند
