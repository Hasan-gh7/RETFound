> Updated 2026-11-05: connection.json now supplies BOTH base_url and the RETFound access key. Put a private current copy beside run_demo.py on another computer, then run `python run_demo.py --connection-file connection.json` using Python with backend/requirements.txt installed. No OpenRouter key or model weights are needed on the demo computer. Earlier loopback-only defaults below are historical. Host two-app instructions: ../docs/TWO_APPS_AR.md.

# عينك AI — واجهة مستقلة لخادم RETFound

هذا المجلد وحده عُدّل. نظام RETFound الحالي والأوزان والبيئة لم تُعدّل.
الديمو لا يحمّل نموذجًا ولا يستخدم ONNX أو نتائج محاكاة.

## التشغيل على جهازك

اترك خادم RETFound الحالي يعمل على المنفذ 8000، ثم شغّل `start_windows.bat`.
يستخدم المشغّل Python الموجود في ml-homework ومكتبات `.runtime/web` الموجودة
في المشروع الأب للقراءة فقط. لا ينشئ بيئة ولا يثبت أو يحدّث أي حزمة.

أو من PowerShell داخل RETFound:

```powershell
& "$env:USERPROFILE\.conda\envs\ml-homework\python.exe" -B .\eye-ai-demo\run_demo.py
```

افتح http://127.0.0.1:8001 . فتح ملف index.html مباشرة لا يشغّل التحليل.
الخادم الجديد مستقل؛ إيقافه لا يوقف RETFound. التشغيل اليدوي يتوقف بـCtrl+C.
لا تشغّل نسخة ثانية على المنفذ نفسه. إذا سبق تشغيل الديمو في الخلفية، انظر
`.runtime/session-*/server.json` لمعرفة PID، وتحقق من هوية العملية قبل إيقافها.

## الاتصال والمفتاح

الافتراضي `http://127.0.0.1:8000`. يقرأ الديمو مفتاح Bearer من
`../.runtime/tunnel/connection.json` عند بدء التشغيل، إذا كان الملف موجودًا.
المفتاح يبقى في الخادم ولا يُرسل إلى JavaScript أو localStorage أو الصادرات.
لا يقرأ الديمو مفتاح OpenRouter ولا يطلبه؛ يبقى ذلك ضمن خادم RETFound الحالي.
إذا تجددت جلسة RETFound ومفتاحها، أعد تشغيل الديمو لقراءة المفتاح الجديد.

بدائل اختيارية في بيئة عملية الديمو فقط:

- `RETFOUND_API_URL`: عنوان أصل الخدمة دون `/api/predict`. الاتصال البعيد يتطلب HTTPS.
- `RETFOUND_API_KEY`: مفتاح Bearer دون كلمة Bearer، وله الأولوية على ملف الاتصال.
- `RETFOUND_CONNECTION_FILE`: ملف connection.json خاص يحتوي `authorization: Bearer ...`.

يمكن استخدام `--api-url` و`--connection-file` و`--port` و`--no-browser`.
ملف الاتصال يوفّر المفتاح فقط؛ لا يغيّر عنوان الخدمة تلقائيًا إلى النفق العام.
لا تضع المفاتيح في frontend/config.js أو سطر الأوامر أو ملفات المشاركة.

## مسار الصورة والنتيجة

المتصفح ←رفع الصورة→ خادم الديمو:8001 → POST /api/predict في RETFound:8000.
يمرّر الديمو بايتات الصورة الأصلية دون إعادة ترميز أو معالجة مسبقة.
يتولى الخادم الحالي فحص Jev الخارجي ثم معالجة RETFound المعتمدة والاستدلال.
الاسم والعمر ورقم الملف لا تُرسل مع طلب التحليل.

يعرض الديمو درجة DR من 0 إلى 4 وكل درجات softmax الخمس، وهي غير معايرة.
يحفظ هوية النموذج وبصمة الصورة ومعرّف الطلب والاستجابة الأصلية في تصدير JSON.
الملخص والتقرير يخصان DR فقط. AMD والجلوكوما غير مقيّمين ولا يحصلان على
نتائج سالبة أو احتمالات افتراضية. ظهور اتصال جاهز لا يثبت صلاحية Jev أو
نجاح طلب صورة؛ يثبت فقط جاهزية خدمة RETFound وقراءة هويتها.

الأخطاء ورفض Jev وانقطاع الاتصال تنتهي برسالة خطأ دون محاكاة أو إعادة محاولة
تلقائية. المهلة 150 ثانية للخادم و165 ثانية للمتصفح؛ انتهاء المهلة لا يثبت
أن الطلب لم يُنفّذ. تقدّم الواجهة ليس قياسًا لمراحل التنفيذ داخل الخادم.

## السجل والخصوصية

الحفظ اختياري داخل localStorage على نفس المتصفح، ويضم بيانات الحالة ونسخة
معاينة من الصورة والنتيجة. السجل غير مشفر تطبيقيًا؛ استخدم بيانات عرض وهمية.
السجل الجديد منفصل عن سجل المحاكاة القديم؛ لا يُحذف القديم ولا يُعرض كحقيقي.
فحص السطوع والتباين محلي وتقريبي، وليس كاشفًا للشبكية أو درجة صلاحية سريرية.

## التحقق

من جذر RETFound، دون تثبيت حزم:

```powershell
& "$env:USERPROFILE\.conda\envs\ml-homework\python.exe" -B eye-ai-demo/tests/test_adapter.py
node eye-ai-demo/tests/verify_frontend.cjs
```

الاختبارات تستخدم استجابات مصطنعة ولا تثبت أداء النموذج. تفاصيل التنفيذ
في `docs/PROGRESS.md`. أداة `tests/live_smoke.py --image <path>` ترسل صورة حقيقية
إلى RETFound وخدمة Jev وقد تُحتسب عليها تكلفة؛ لا تُشغّل ضمن الاختبارات المعتادة.

## Docker والأجهزة الأخرى

إعداد Docker اختياري ولم يُختبر. يلزم توفير عنوان HTTPS لخادم RETFound يمكن
للحاوية الوصول إليه وRETFOUND_API_KEY في بيئة Docker. لا تُنشأ خدمة RETFound
أو أوزان جديدة داخل الحاوية. على جهاز مستقل استخدم بيئة موجودة تحمل متطلبات
backend/requirements.txt؛ المشغلات لا تثبّت المتطلبات تلقائيًا.
