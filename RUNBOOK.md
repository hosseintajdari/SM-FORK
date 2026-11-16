# راهنمای توسعه و نگهداری اسمارت‌تیوب

مرجع سورس: hosseintajdari/SM-FORK. مخزن اصلی: yuliskov/SmartTube. فورک زیرماژول: hosseintajdari/MediaServiceCore. Windows برای توسعه و آزمون تلویزیون است. GitHub Actions برای بررسی و ساخت بستهٔ آزمایشی است. ct برای ساخت دستی از یک کامیت مشخص است.

## شروع هر نوبت

- ویندوز: C:\Users\hosse\AndroidTools\SM-FORK
- سرور: ~/AndroidTools/SM-FORK؛ ورود با ssh ct و کلید میزبان تأییدشده.
- ابتدا دستورهای زیر را در پوشهٔ پروژه اجرا کن. اگر تغییر موجود یا زیرماژول با علامت +، - یا U دیدی، پیش از تغییر منشأ آن را پیدا کن. فایل‌های کاربر را پاک نکن.

~~~text
git status --short --branch
git remote -v
git rev-parse HEAD
git submodule status --recursive
~~~

برای باگ ابتدا بازتولید و لاگ حداقلی بگیر و از ECC orch-fix-defect استفاده کن. برای قابلیت جدید از orch-add-feature و برای تغییر رفتار از orch-change-feature استفاده کن. بعد از بررسی، diff و نتیجهٔ ساخت را ثبت کن. تأیید کامیت و انتشار را طبق درخواست کاربر بگیر. قبل از همگام‌سازی، نسخهٔ پایدار upstream و تغییرات اختصاصی فورک را مشخص کن. ابتدا تغییرهای فارسی MediaServiceCore را روی مبنای جدید منتقل و کامیت زیرماژول را در فورک آن قابل دریافت کن، سپس gitlink را در SM-FORK ثبت کن.

## ساخت و دریافت APK

پیش‌نیاز: Git، Python 3، JDK 17 و SDK اندروید با API 34، Build Tools 30.0.3، NDK 21.0.6113669 و Platform Tools. نسخهٔ Gradle از Wrapper مخزن می‌آید. در ویندوز از نصب موجود زیر AndroidTools استفاده کن. در PowerShell:

~~~powershell
$env:JAVA_HOME = 'C:\Users\hosse\AndroidTools\store-shortcut\jdk\jdk-17.0.21.0.2+1'
$env:ANDROID_HOME = 'C:\Users\hosse\AndroidTools\smarttube-android-sdk'
git submodule update --init --recursive
python tools/build_test_apk.py --checks
~~~

برای اولین راه‌اندازی ct روی Linux x86_64، یک JDK 17 و Android SDK Command-line Tools رسمی در فضای کاربر آماده کن. از sudo یا تغییر سرویس‌های میزبان استفاده نکن. پس از تطبیق کلید میزبان و بررسی فضای دیسک، در مسیر انتخاب‌شده:

~~~bash
mkdir -p ~/AndroidTools
git clone https://github.com/hosseintajdari/SM-FORK.git ~/AndroidTools/SM-FORK
cd ~/AndroidTools/SM-FORK
export JAVA_HOME="$HOME/AndroidTools/toolchains/jdk-17"
export ANDROID_HOME="$HOME/AndroidTools/toolchains/android-sdk"
"$ANDROID_HOME/cmdline-tools/latest/bin/sdkmanager" "platforms;android-34" "build-tools;30.0.3" "ndk;21.0.6113669" "platform-tools"
~~~

اگر پروژه موجود است، به‌جای clone منشأ و تمیزی همان checkout را بررسی کن. برای ساخت، SHA را از نسخهٔ بررسی‌شدهٔ گیت‌هاب بردار. اگر git status تغییر نشان داد قبل از تعویض نسخه توقف کن.

~~~bash
git fetch origin --tags
read -r -p "Approved commit SHA: " approved_sha
[[ "$approved_sha" =~ ^[0-9a-f]{40}$ ]] || exit 1
git switch --detach "$approved_sha"
git submodule update --init --recursive
python3 tools/build_test_apk.py --checks
~~~

خروجی در build/maintenance است: APK، SHA256SUMS و build-info.json. اگر dirty=true است، فایل را ساخت محلی معرفی کن. برای ساخت قابل بازتولید، کامیت و تمام gitlinkها باید از GitHub قابل دریافت باشند. امضای دیباگ و زمان ساخت ممکن است بین میزبان‌ها فرق کند. هش را با فایل همان اجرا مقایسه کن. در GitHub، workflow «SmartTube maintenance» را در Actions باز کن و artifact اجرای SHA موردنظر را بگیر. برای اجرای دستی روی شاخهٔ موردنظر، گزینهٔ Run workflow پس از قرار گرفتن تعریف workflow روی شاخهٔ پیش‌فرض قابل استفاده است.

## آزمون تلویزیون و رفع خطا

در پروفایل تازه، منوی پیش‌فرض باید به ترتیب Home، Shorts، Gaming، Music، Subscriptions، History و Settings باشد. برای بررسی پیش‌فرض از پروفایل تازه استفاده کن و داده‌های پروفایل فعلی را پاک نکن.

برای آزمون روی باکس، اول فایل ARMv7 و امضا را بررسی کن. بسته org.smarttube.beta است و با نسخهٔ پایدار شناسهٔ جدا دارد. اگر همین شناسه از قبل با امضای دیگر نصب است، قبل از هر حذف از کاربر اجازه بگیر. آدرس فعلی باکس را از تنظیمات شبکه یا adb mdns services پیدا کن و مدل را با adb shell getprop ro.product.model تأیید کن. نصب فقط با درخواست کاربر. ابتدا بدون VPN یک ویدیو و زیرنویس فارسی را امتحان کن. سپس با هرکدام از Hiddify، Karing و Proton به‌صورت جداگانه همان سناریو را اجرا کن و تنظیم «عمومی ← شبکه ← موتور شبکه ← خودکار» را بررسی کن. زمان شروع، ادامهٔ پخش، وضعیت تونل و نتیجه را جدا از موفقیت بیلد ثبت کن.

- خطای زیرماژول: اول gitlink ثبت‌شده و دسترسی خواندن به fork را بررسی کن. با نسخهٔ شناور جایگزین نکن.
- خطای SDK: مسیرهای محیط و وجود نسخه‌های دقیق را بررسی کن. نسخهٔ پروژه را برای رفع مشکل محلی تغییر نده.
- تداخل امضا: نسخهٔ نصب‌شده و شناسه را بررسی کن. کلید انتشار را وارد پایپ‌لاین آزمایشی نکن.
- خطای ct: اگر SSH پیش از ورود بسته شد، نسخهٔ ویندوز و CI را ادامه بده و وضعیت ct را ثبت کن. کلید میزبان را دور نزن. روی ct هیچ runner یا زمان‌بندی خودکار لازم نیست.
- قطع VPN: جداگانه اتصال خود تونل و پخش برنامه را بررسی کن. گزینهٔ موتور شبکه داخل اسمارت‌تیوب مسئول برقراری مجدد تونل VPN نیست.
