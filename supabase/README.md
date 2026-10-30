# قاعدة بيانات دوامي

الجداول `dawami_accounts` و `dawami_records` و `dawami_exceptions` في مشروع Supabase، مغلقة بالكامل (RLS بدون سياسات).
كل القراءة والكتابة عبر دوال RPC تتحقق من رمز الدخول (يُخزَّن منه بصمة SHA-256 فقط):

| الدالة | الاستخدام |
|---|---|
| `dawami_register(p_key, p_settings)` | إنشاء حساب |
| `dawami_load(p_key)` | جلب كل البيانات |
| `dawami_save_settings(p_key, p_settings)` | حفظ الإعدادات |
| `dawami_set_record(p_key, p_day, p_in, p_out)` | حفظ/حذف يوم |
| `dawami_set_exception(p_key, p_day, p_kind)` | حفظ/حذف استثناء |
| `dawami_punch(p_key, p_kind, p_time?, p_day?)` | للاختصارات: حضور/انصراف بالوقت الحالي |
| `dawami_import(p_key, p_state, p_replace)` | استيراد نسخة |
| `dawami_wipe(p_key)` | مسح البيانات |
