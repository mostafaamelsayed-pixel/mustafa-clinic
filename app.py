# app.py
import streamlit as st
import re
import pandas as pd
from pathlib import Path

# إعدادات المنصة السحابية لعيادة د. مصطفي السيد
st.set_page_config(
    page_title="عيادة د. مصطفي السيد - إدارة المحتوى العلاجي",
    page_icon="🩺",
    layout="wide"
)

# تصميم الواجهة بالألوان الطبية والخط الاحترافي المتوافق مع شاشات اللمس
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    html, body, [data-testid="stSidebar"], .stMarkdown {
        font-family: 'Cairo', sans-serif;
        direction: RTL;
        text-align: right;
    }
    .main-title {
        color: #007A78;
        font-size: 30px;
        font-weight: 900;
        margin-bottom: 25px;
        text-align: center;
        border-bottom: 3px solid #007A78;
        padding-bottom: 15px;
    }
    .recipe-box {
        background-color: #1E1E1E;
        padding: 20px;
        border-radius: 12px;
        border-right: 5px solid #007A78;
        margin-bottom: 15px;
    }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<div class="main-title">🩺 النظام السحابي لعيادة د. مصطفي السيد لفصل وتوليد الوجبات الطبية</div>', unsafe_allow_html=True)

# القائمة الجانبية للإعدادات
with st.sidebar:
    st.markdown("### ⚙️ خيارات التصدير السحابي")
    theme = st.selectbox("قالب الهوية البصرية:", ["Medical (طبّي برميوم)", "Luxury (فاخر)"])
    img_size = st.selectbox("أبعاد الصور المطلوبة:", ["1080x1350 (سوشيال ميديا)", "A4_Portrait (طباعة للعيادة)"])
    st.write("---")
    st.markdown("✨ نظام معالجة سحابي فوري ومستقل بالكامل.")

# واجهة رفع الملفات
uploaded_file = st.file_uploader("اختر ملف الـ HTML المحتوي على الوجبات من ذاكرة التابلت:", type=["html", "htm"])

if uploaded_file is not None:
    html_content = uploaded_file.read().decode("utf-8")
    st.success("✅ تم قراءة ملف الوجبات سحابياً بنجاح!")
    
    if st.button("🚀 إطلاق المعالجة وفصل الوجبات فوراً", use_container_width=True):
        with st.spinner("جاري تحليل الوجبات واستخراج القيم الغذائية بدقة متناهية..."):
            
            # محرك فرز وتحليل دلالي سريع متوافق مع البيئة السحابية
            raw_recipes = html_content.split('<div class="recipe-card">')[1:]
            parsed_data = []
            
            for index, raw_item in enumerate(raw_recipes):
                title_match = re.search(r'<h2 class="recipe-title">(.*?)</h2>', raw_item)
                code_match = re.search(r'<span class="recipe-code">(.*?)</span>', raw_item)
                calories_match = re.search(r'السعرات:\s*(\d+)', raw_item)
                protein_match = re.search(r'البروتين:\s*(\d+)', raw_item)
                
                title = title_match.group(1).strip() if title_match else f"وجبة علاجية {index+1}"
                code = code_match.group(1).strip() if code_match else f"MD-{1000+index}"
                calories = calories_match.group(1) if calories_match else "0"
                protein = protein_match.group(1) if protein_match else "0"
                
                parsed_data.append({
                    "كود الوجبة": code,
                    "اسم الوجبة الغذائية": title,
                    "السعرات (kcal)": calories,
                    "البروتين (ج)": protein
                })
            
            if parsed_data:
                st.balloons()
                st.success(f"🎉 تم بنجاح فصل وتوليد {len(parsed_data)} وجبة طبية مستقلة!")
                
                # تحويل البيانات إلى جدول إحصائي فوري متاح للتحميل
                df = pd.DataFrame(parsed_data)
                st.markdown("### 📊 بيان الوجبات المفصولة والجاهزة للتحميل:")
                st.dataframe(df, use_container_width=True)
                
                # توليد ملف التقرير الطبي الشامل بصيغة CSV فوراً لتنزيله على التابلت
                csv_data = df.to_csv(index=False).encode('utf-8-sig')
                
                st.download_button(
                    label="📥 تحميل تقرير الوجبات الشامل للتابلت (CSV)",
                    data=csv_data,
                    file_name="تقرير_وجبات_عيادة_د_مصطفي_السيد.csv",
                    mime="text/csv",
                    use_container_width=True
                )
                
                # عرض كروت تفاعلية مخصصة للمراجعة السريعة مع المرضى داخل العيادة
                st.markdown("### 📋 معاينة نصوص الوجبات التسويقية والعلاجية:")
                for item in parsed_data:
                    with st.container():
                        st.markdown(f"""
                        <div class="recipe-box">
                            <h4 style="color: #007A78; margin-top:0;">📌 {item['اسم الوجبة الغذائية']} ({item['كود الوجبة']})</h4>
                            <p style="margin: 5px 0;">🔥 <b>السعرات الحرارية:</b> {item['السعرات (kcal)']} سعرة | 💪 <b>البروتين:</b> {item['البروتين (ج)']} جرام</p>
                            <p style="color: #bbb; font-size: 13px; margin-bottom:0;">📝 <b>النص المقترح لصفحة العيادة:</b> وجبة صحية متكاملة ومحسوبة بدقة من عيادة د. مصطفي السيد لتنظيم الوزن والدعم الغذائي. #د_مصطفي_السيد</p>
                        </div>
                        """, unsafe_allow_html=True)
            else:
                st.error("لم يتم العثور على وجبات متوافقة داخل بنية الملف المرفوع.")
