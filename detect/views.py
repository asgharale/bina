from django.shortcuts import render
from django.conf import settings
from django.core.exceptions import ValidationError
from google import genai
from google.genai import types
from .forms import ImageDetectForm


def detect_view(request):
    if request.method == 'POST':
        form = ImageDetectForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_image = request.FILES['image']
            user_prompt = form.cleaned_data['prompt'].strip()

            try:
                if uploaded_image.size > 10 * 1024 * 1024:
                    raise ValidationError("حجم فایل بیش از ۱۰ مگابایت است.")

                img_bytes = uploaded_image.read()

                # ساخت Part تصویر
                image_part = types.Part.from_bytes(
                    data=img_bytes,
                    mime_type=uploaded_image.content_type or "image/jpeg"
                )

                # ساخت متن به عنوان Part جدا
                if user_prompt:
                    text_part = types.Part.from_text(text=user_prompt)
                else:
                    default_text = (
                        "لطفاً این تصویر را با دقت و به صورت کامل و مرتب به زبان فارسی توصیف کن. "
                        "به اشیا، رنگ‌ها، متن‌های داخل تصویر، حس کلی و جزئیات مهم توجه کن و "
                        "پاسخ را روان و دوستانه بنویس."
                    )
                    text_part = types.Part.from_text(text=default_text)

                # ساختار contents: لیست از Content با role و parts
                contents = [
                    types.Content(
                        role="user",
                        parts=[text_part, image_part]
                    )
                ]

                client = genai.Client(api_key=settings.GEMINI_API_KEY)

                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=contents
                )

                ai_response = response.text.strip()

            except Exception as e:
                import traceback
                print("خطای کامل:", traceback.format_exc())
                ai_response = f"خطایی رخ داد: {str(e)}\nجزئیات در لاگ سرور."

            context = {
                'form': form,
                'response': ai_response,
                'image_preview': uploaded_image,
            }

            # حتماً نتیجه را در صفحه جدا نشون بده
            return render(request, 'detect/result.html', context)

        # فرم نامعتبر → برگشت به همان صفحه با ارورها
        return render(request, 'detect/upload.html', {'form': form})

    # GET → فرم خالی
    form = ImageDetectForm()
    return render(request, 'detect/upload.html', {'form': form})