# رد بوت تلغرام المختصر

بعد إعادة تشغيل الخادم، غيّر عنوان طلب البوت إلى:

```text
POST <base_url>/api/predict/summary
Authorization: Bearer <RETFound access key>
Body: multipart/form-data, field image (File)
```

المصادقة والصورة كما في الطلب السابق. هذا مسار جديد؛ /api/predict يظل
متوافقًا مع Eye AI والموقع. يستخدم المساران الاستدلال نفسه دون تكراره.
أخطاء Jev والصورة والازدحام تبقى أخطاء ولا تتحول إلى نتيجة ناجحة.

النجاح يحتوي فقط predicted_grade وpredicted_label وclass_scores_percent.
الأخيرة خمس عناصر {grade, label, score} بترتيب 0..4 ونسب مئوية مقربة إلى
منزلتين. هذه درجات نموذج غير معايرة، وليست نسبة صحة التشخيص أو دقة النموذج.
التصنيف توقع النموذج وليس ضمانًا بأن التصنيف صحيح سريريًا.

## عرض رسالة بدل JSON

### عند رفض الصورة بواسطة Jev

يبقى رمز HTTP هو 422، لكن جسم JSON يحتوي error.code = not_retinal_fundus
ورسالة عربية في error.message، مع prediction = null. رقم 422 وحده لا
يعني رفض Jev؛ قد يكون خطأ ملف صورة أيضًا. لا تحوّل كل حالات 422 إلى رفض قاع عين.
فشل خدمة Jev يعيد 503 ولا يمثل قرارًا بأن الصورة ليست قاع عين.

على البوت قراءة جسم الرد قبل raise_for_status() أو شرط الفشل العام:

```python
def format_api_response(response):
    try:
        data = response.json()
    except ValueError:
        return "تعذر الوصول إلى خدمة التحليل. حاول لاحقًا بعد التحقق من اتصال الخادم."
    if not isinstance(data, dict):
        return "وصل رد غير متوقع من خدمة التحليل."
    if response.status_code == 200:
        return format_prediction(data)  # for /api/predict/summary
    error = data.get("error") or {}
    code = error.get("code") if isinstance(error, dict) else None
    if code == "not_retinal_fundus":
        return ("⚠️ لم يتعرّف فحص Jev على الصورة كصورة لقاع العين.\n"
                "يرجى إرسال صورة لقاع العين (Fundus).\n"
                "لم يُجرَ تحليل اعتلال الشبكية لهذه الصورة.")
    if code == "fundus_check_unavailable":
        return "خدمة التحقق من الصورة غير متاحة حاليًا؛ لم يُجرَ التحليل."
    if code == "invalid_image":
        return "تعذر قراءة الصورة. أرسل ملف صورة صالحًا."
    if response.status_code == 429:
        return "الخدمة مشغولة حاليًا. يرجى الانتظار قبل إرسال طلب جديد."
    return "تعذر إكمال التحليل. تحقق من الاتصال وإعدادات الخدمة."

# Use this text in your bot's reply instead of printing just HTTP status:
# message = format_api_response(response)
```

هذا التعديل مطلوب في كود البوت لدى زميلك؛ تحسين رسالة الـAPI لا يكفي إذا
كان البوت يتجاهل جسم الرد ويطبع Analysis failed. API returned status: 422.

على زميلك استبدال طباعة response.json() في رسالة تلغرام بتنسيق النص التالي.
هذا مثال دالة تنسيق محلية، لا ترسل رسائل ولا تنفذ طلبًا آخر:

```python
LABELS_AR = ["لا توجد علامات اعتلال شبكية سكري بحسب النموذج", "اعتلال خفيف",
             "اعتلال متوسط", "اعتلال شديد", "اعتلال تكاثري"]

def format_prediction(result):
    grade = result["predicted_grade"]
    lines = ["نتيجة تحليل الصورة", "", "التصنيف المتوقع: " + LABELS_AR[grade],
             "", "درجات التصنيف:"]
    for item in result["class_scores_percent"]:
        lines.append(f"• {LABELS_AR[item['grade']]}: {item['score']:.2f}%")
    return "\n".join(lines)
```

اعرض النص فقط عند HTTP 200؛ عند فشل الطلب اعرض رسالة الخطأ دون تصنيف.
احتفظ بتنبيه الاستخدام البحثي في وصف البوت أو شاشة البداية. لا يلزم نشر
التفاصيل التقنية أو المفتاح أو hashes في رسالة المستخدم. لا يُعد البوت
معدلًا تلقائيًا بهذا الملف؛ مصدر البوت موجود لدى زميلك.

## Dataset tests

تستخدم البطاقات thumbnail_url لنسخ JPEG لا تتجاوز 320×320 للعرض فقط.
رابط image_url يظل يعيد الأصل؛ التنبؤ يتحقق من SHA-256 ويستخدم الأصل دائمًا.
التحليل يعرض زمن Jev وزمن RETFound وإجمالي الخادم؛ الإجمالي يتضمن الانتظار
والرفع، ولا يساوي زمن رسالة تلغرام من بدايتها لنهايتها. اختبارات الكل
تبقى متسلسلة لتجنب ازدحام الجهاز؛ لا يُتجاوز Jev ولا تُعاد طلباته تلقائيًا.
